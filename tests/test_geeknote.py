# -*- coding: utf-8 -*-

import unittest
from geeknote.geeknote import *
from geeknote import tools
from geeknote.editor import Editor


class GeekNoteOver(GeekNote):
    def __init__(self):
        pass

    def loadNoteContent(self, note):
        note.content = "note content"


class NotesOver(Notes):
    def connectToEvernote(self):
        self.evernote = GeekNoteOver()


class testNotes(unittest.TestCase):

    def setUp(self):
        self.notes = NotesOver()
        self.testNote = tools.Struct(title="note title")
        # set the timezone for the date tests to work
        # this is particularly important on Travis CI, where
        # the timezone may not be the same as our dev machine
        os.environ['TZ'] = "PST-0800"
        time.tzset()

    def test_parseInput1(self):
        testData = self.notes._parseInput("title", "test body", "tag1", None, None, ["res 1", "res 2"])
        self.assertTrue(isinstance(testData, dict))
        if not isinstance(testData, dict):
            return

        self.assertEqual(testData['title'], "title")
        self.assertEqual(testData['content'], Editor.textToENML("test body"))
        self.assertEqual(testData["tags"], ["tag1", ])
        self.assertEqual(testData["resources"], ["res 1", "res 2"])

    def test_parseInput2(self):
        testData = self.notes._parseInput("title", "WRITE", "tag1, tag2", None, None, self.testNote)
        self.assertTrue(isinstance(testData, dict))
        if not isinstance(testData, dict):
            return

        self.assertEqual(testData['title'], "title")
        self.assertEqual(
            testData['content'],
            "WRITE"
        )
        self.assertEqual(testData["tags"], ["tag1", "tag2"])

    # Disable this test
    #   It blocks, and while it can be overriden by defining EDITOR=/bin/cat, for example,
    #   it's challenging to make those arrangements in all CI systems
    # def test_editWithEditorInThread(self):
    #     testData = self.notes._parseInput("title", "WRITE", "tag1, tag2", None, None, self.testNote)
    #     print ('')
    #     print ('')
    #     print (testData)
    #     print ('')
    #     print ('')
    #     self.notes._editWithEditorInThread(testData)

    def test_createSearchRequest1(self):
        testRequest = self.notes._createSearchRequest(
            search="test text",
            tags="tag1",
            notebooks="test notebook",
            date="2000-01-01",
            exact_entry=True,
            content_search=True
        )
        response = 'notebook:"test notebook" tag:tag1' \
                   ' created:19991231T000000Z "test text"'
        self.assertEqual(testRequest, response)

    def test_createSearchRequest2(self):
        testRequest = self.notes._createSearchRequest(
            search="test text",
            tags="tag1, tag2",
            notebooks="notebook1, notebook2",
            date="1999-12-31/2000-12-31",
            exact_entry=False,
            content_search=False
        )
        response = 'notebook:notebook1 notebook:notebook2 tag:tag1' \
                   ' tag:tag2 created:19991230T000000Z -created:20001231T000000Z' \
                   ' intitle:test text'
        self.assertEqual(testRequest, response)

    def testError_createSearchRequest1(self):
        sys.exit = lambda code: code

        with self.assertRaises(tools.ExitException):
            self.notes._createSearchRequest(search="test text",
                                            date="12-31-1999")
