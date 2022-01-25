# -*- coding: utf-8 -*-

import sys
import time
import unittest
from io import StringIO
from geeknote.geeknote import *
from geeknote import tools
from geeknote.editor import Editor
from geeknote.storage import Storage


class GeekNoteOver(GeekNote):
    def __init__(self):
        pass

    def loadNoteContent(self, note):
        if "content" not in note.__dict__:
            note.content = "note content"

    def updateNote(self, guid=None, **inputData):
        # HACK for testing: this assumes that the guid represents a "note" itself
        # see check_editWithEditorInThread below
        guid.content = inputData["content"]


class NotesOver(Notes):
    def connectToEvernote(self):
        self.evernote = GeekNoteOver()


class testNotes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Use our trivial "pseudoedit" program as editor to avoid user interaction
        cls.storage = Storage()
        cls.saved_editor = cls.storage.getUserprop('editor')
        cls.storage.setUserprop('editor', sys.executable + " " +
                                os.path.join(os.path.dirname(os.path.abspath(__file__)), "pseudoedit.py"))

    @classmethod
    def tearDownClass(cls):
        if cls.saved_editor:
            cls.storage.setUserprop('editor', cls.saved_editor)

    def setUp(self):
        self.notes = NotesOver()
        self.testNote = tools.Struct(title="note title")
        # set the timezone for the date tests to work
        # this is particularly important on Travis CI, where
        # the timezone may not be the same as our dev machine
        os.environ['TZ'] = "PST-0800"
        time.tzset()

    def test_parseInput1(self):
        testData = self.notes._parseInput("title", "test body", ["tag1"], None, None, ["res 1", "res 2"])
        self.assertTrue(isinstance(testData, dict))
        if not isinstance(testData, dict):
            return

        self.assertEqual(testData['title'], "title")
        self.assertEqual(testData['content'], Editor.textToENML("test body"))
        self.assertEqual(testData["tags"], ["tag1"])
        self.assertEqual(testData["resources"], ["res 1", "res 2"])

    def test_parseInput2(self):
        testData = self.notes._parseInput("title", "WRITE", ["tag1", "tag2"], None, None, self.testNote)
        self.assertTrue(isinstance(testData, dict))
        if not isinstance(testData, dict):
            return

        self.assertEqual(testData['title'], "title")
        self.assertEqual(
            testData['content'],
            "WRITE"
        )
        self.assertEqual(testData["tags"], ["tag1", "tag2"])

    def check_editWithEditorInThread(self, txt, expected):
        testNote = tools.Struct(title="note title",
                                content=txt)
        # hack to make updateNote work - see above
        testNote.guid = testNote
        testData = self.notes._parseInput("title",
                                          txt,
                                          ["tag1", "tag2"],
                                          None, None, testNote)
        result = self.notes._editWithEditorInThread(testData, testNote)
        self.assertEqual(Editor.ENMLtoText(testNote.content), expected)

    # def test_editWithEditorInThread(self):
    #     txt = "Please do not change this file"
    #     self.check_editWithEditorInThread(txt, txt + '\n')

    def test_editWithEditorInThread2(self):
        txt = "Please delete this line, save, and quit the editor"
        self.check_editWithEditorInThread(txt, "\n\n")

    def test_createSearchRequest1(self):
        testRequest = self.notes._createSearchRequest(
            search="test text",
            tags=["tag1"],
            notebook="test notebook",
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
            tags=["tag1", "tag2"],
            notebook="notebook1",
            date="1999-12-31/2000-12-31",
            exact_entry=False,
            content_search=False
        )
        response = 'notebook:notebook1 tag:tag1' \
                   ' tag:tag2 created:19991230T000000Z -created:20001231T000000Z' \
                   ' intitle:test text'
        self.assertEqual(testRequest, response)

    def testError_createSearchRequest1(self):
        # set fake stdout and stderr
        self.stdout, sys.stdout = sys.stdout, StringIO()
        self.stderr, sys.stderr = sys.stderr, StringIO()
        sys.exit = lambda code: code
        with self.assertRaises(tools.ExitException):
            self.notes._createSearchRequest(search="test text",
                                            date="12-31-1999")
