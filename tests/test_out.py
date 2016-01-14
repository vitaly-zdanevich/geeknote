#!/usr/bin/env python2

import sys
import os
import time
import unittest
from cStringIO import StringIO
from geeknote.config import VERSION
from geeknote.out import printDate, printLine, printAbout,\
    separator, failureMessage, successMessage, showUser, showNote, \
    printList, SearchResult
from geeknote import out


class AccountingStub(object):
    uploadLimit = 100
    uploadLimitEnd = 1095292800000

class UserStub(object):
    username = 'testusername'
    name = 'testname'
    email = 'testemail'
    id = 111
    shardId = 222
    accounting = AccountingStub()
    timezone = None

class AttributesStub(object):
    reminderOrder = None
    reminderTime = None
    reminderDoneTime = None

class NoteStub(object):
    title = 'testnote'
    created = 1095292800000
    updated = 1095292800000
    content = '##note content'
    tagNames = ['tag1', 'tag2', 'tag3']
    guid = 12345
    attributes = AttributesStub()


class outTestsWithHackedStdout(unittest.TestCase):

    def setUp(self):
        # set fake stdout and stderr
        self.stdout, sys.stdout = sys.stdout, StringIO()
        self.stderr, sys.stderr = sys.stderr, StringIO()
        # set the timezone for the date tests to work
        # this is particularly important on Travis CI, where
        # the timezone may not be the same as our dev machine
        os.environ['TZ'] = "PST-0800"
        time.tzset()

    def tearDown(self):
        sys.stdout = self.stdout
        sys.stderr = self.stderr

    def test_print_line(self):
        printLine('test')
        sys.stdout.seek(0)
        self.assertEquals(sys.stdout.read(), 'test\n')

    def test_print_line_other_endline_success(self):
        printLine('test', endLine='\n\r')
        sys.stdout.seek(0)
        self.assertEquals(sys.stdout.read(), 'test\n\r')

    def test_print_about_success(self):
        about = '''Version: %s
Geeknote - a command line client for Evernote.
Use geeknote --help to read documentation.
And visit www.geeknote.me to check for updates.\n''' % VERSION
        printAbout()
        sys.stdout.seek(0)
        self.assertEquals(sys.stdout.read(), about)

    def test_separator_with_title_success(self):
        line = '------------------- test ------------------\n'
        separator(symbol='-', title='test')
        sys.stdout.seek(0)
        self.assertEquals(sys.stdout.read(), line)

    def test_separator_without_title_success(self):
        line = '----------------------------------------\n\n'
        separator(symbol='-')
        sys.stdout.seek(0)
        self.assertEquals(sys.stdout.read(), line)

    def test_separator_empty_args_success(self):
        separator()
        sys.stdout.seek(0)
        self.assertEquals(sys.stdout.read(), '\n\n')

    def test_failure_message_success(self):
        failureMessage('fail')
        sys.stderr.seek(0)
        self.assertEquals(sys.stderr.read(), 'fail\n')

    def test_success_message_success(self):
        successMessage('success')
        sys.stdout.seek(0)
        self.assertEquals(sys.stdout.read(), 'success\n')

    def test_show_user_without_fullinfo_success(self):
        showUser(UserStub(), {})
        info = '''################ USER INFO ################
Username         : testusername
Name             : testname
Email            : testemail\n'''
        sys.stdout.seek(0)
        self.assertEquals(sys.stdout.read(), info)

    def test_show_user_with_fullinfo_success(self):
        showUser(UserStub(), True)
        info = '''################ USER INFO ################
Username         : testusername
Name             : testname
Email            : testemail
Upload limit     : 0.00 MB
Upload limit end : 2004-09-17
Timezone         : None\n'''
        sys.stdout.seek(0)
        self.assertEquals(sys.stdout.read(), info)

    def test_show_note_success(self):
        note = '''################### URL ###################
NoteLink: https://www.evernote.com/shard/222/nl/111/12345
WebClientURL: https://www.evernote.com/Home.action?#n=12345
################## TITLE ##################
testnote
=================== META ==================
Created: 2004-09-17
Updated: 2004-09-17
|||||||||||||||| REMINDERS ||||||||||||||||
Order: None
Time: None
Done: None
----------------- CONTENT -----------------
Tags: tag1, tag2, tag3
##note content\n\n'''
        showNote(NoteStub(), UserStub().id, UserStub().shardId)
        sys.stdout.seek(0)
        self.assertEquals(sys.stdout.read(), note)

    def test_print_list_without_title_success(self):
        notes_list = '''Found 2 items
  1 : 2004-09-17        2004-09-17        testnote
  2 : 2004-09-17        2004-09-17        testnote\n'''
        printList([NoteStub() for _ in xrange(2)])
        sys.stdout.seek(0)
        self.assertEquals(sys.stdout.read(), notes_list)

    def test_print_list_with_title_success(self):
        notes_list = '''=================== test ==================
Found 2 items
  1 : 2004-09-17        2004-09-17        testnote
  2 : 2004-09-17        2004-09-17        testnote\n'''
        printList([NoteStub() for _ in xrange(2)], title='test')
        sys.stdout.seek(0)
        self.assertEquals(sys.stdout.read(), notes_list)

    def test_print_list_with_urls_success(self):
        notes_list = '''=================== test ==================
Found 2 items
  1 : 2004-09-17        2004-09-17        testnote >>> https://www.evernote.com/Home.action?#n=12345
  2 : 2004-09-17        2004-09-17        testnote >>> https://www.evernote.com/Home.action?#n=12345
'''
        printList([NoteStub() for _ in xrange(2)], title='test', showUrl=True)
        sys.stdout.seek(0)
        self.assertEquals(sys.stdout.read(), notes_list)

    def test_print_list_with_selector_success(self):
        out.rawInput = lambda x: 2
        notes_list = '''=================== test ==================
Found 2 items
  1 : 2004-09-17        2004-09-17        testnote
  2 : 2004-09-17        2004-09-17        testnote
  0 : -Cancel-\n'''
        out.printList([NoteStub() for _ in xrange(2)], title='test', showSelector=True)
        sys.stdout.seek(0)
        self.assertEquals(sys.stdout.read(), notes_list)

    def test_search_result_success(self):
        result = '''Search request: test
Found 2 items
  1 : 2004-09-17        2004-09-17        testnote
  2 : 2004-09-17        2004-09-17        testnote\n'''
        SearchResult([NoteStub() for _ in xrange(2)], 'test')
        sys.stdout.seek(0)
        self.assertEquals(sys.stdout.read(), result)

    def test_print_date(self):
        self.assertEquals(printDate(1095292800000), '2004-09-17')
