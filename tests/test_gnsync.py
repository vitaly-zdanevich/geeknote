# -*- encoding: utf-8 -*-
from mock import patch, ANY, Mock
import os
import unittest
import shutil
from helpers import AnyStringWith
from geeknote.gnsync import remove_control_characters, GNSync


class testGnsync(unittest.TestCase):
    def setUp(self):
        self.test_dir = '/tmp/test_gnsync'
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

        self.given_eng = '\0This is an english\1 sentence. Is it ok?'
        self.expected_eng = 'This is an english sentence. Is it ok?'
        self.given_kor = '한국\2어입니\3다. 잘 되나요?'
        self.expected_kor = '한국어입니다. 잘 되나요?'
        self.given_chn = '中\4国的输入。我令\5您着迷？'
        self.expected_chn = '中国的输入。我令您着迷？'
        self.given_combined = self.expected_combined = """# 제목

## 제 1 장

_한국어 입력입니다. 잘 되나요?_

## 第 2 章

*中国的输入。我令您着迷？*

## Chapter 3

- May the force be with you!

"""

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_strip_eng(self):
        self.assertEqual(remove_control_characters(self.given_eng.decode('utf-8')).encode('utf-8'),
                         self.expected_eng)

    def test_strip_kor(self):
        self.assertEqual(remove_control_characters(self.given_kor.decode('utf-8')).encode('utf-8'),
                         self.expected_kor)

    def test_strip_chn(self):
        self.assertEqual(remove_control_characters(self.given_chn.decode('utf-8')).encode('utf-8'),
                         self.expected_chn)

    def test_strip_nochange(self):
        self.assertEqual(remove_control_characters(self.given_combined.decode('utf-8')).encode('utf-8'),
                         self.expected_combined)

    @patch('geeknote.gnsync.logger', autospec=True)
    @patch('geeknote.gnsync.GeekNote', autospec=True)
    @patch('geeknote.gnsync.Storage', autospec=True)
    def test_create_file_with_non_ascii_chars(self, mock_storage, mock_geeknote, mock_logger):

        # Mock GeekNote#loadNoteContent to provide some content with non-ascii
        def mock_note_load(note):
            with open('tests/fixtures/Test Note with non-ascii.xml', 'r') as f:
                note.content = f.read()
            note.notebookName = 'testNotebook'
        mock_geeknote.return_value.loadNoteContent.side_effect = mock_note_load

        # Mock Storage().getUserToken() so the GNSync constructor doesn't throw
        # an exception
        mock_storage.return_value.getUserToken.return_value = True

        subject = GNSync('test_notebook', self.test_dir, '*.*',
                         'plain', download_only=True)

        mock_note = Mock()
        mock_note.guid = '123abc'
        mock_note.title = 'Test Note'

        subject._create_file(mock_note)

        # Verify that a file could be created with non-ascii content
        mock_logger.exception.assert_not_called_with(
            ANY,
            AnyStringWith("codec can't decode byte")
        )

        with open(self.test_dir + "/Test Note.txt", 'r') as f:
            self.assertIn("œ ž © µ ¶ å õ ý þ ß Ü", f.read())
