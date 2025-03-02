from geeknote.editor import Editor
import unittest


class testEditor(unittest.TestCase):

    def setUp(self):
        self.MD_TEXT = """# Header 1

## Header 2

Line 1

_Line 2_

**Line 3**

"""
        self.HTML_TEXT = """<h1>Header 1</h1>
<h2>Header 2</h2>
<p>Line 1</p>
<p><em>Line 2</em></p>
<p><strong>Line 3</strong></p>
"""

    def test_TextToENML(self):
        self.assertEqual(Editor.textToENML(self.MD_TEXT),
                         Editor.wrapENML(self.HTML_TEXT))

    def test_ENMLToText(self):
        wrapped = Editor.wrapENML(self.HTML_TEXT)
        self.assertEqual(Editor.ENMLtoText(wrapped), self.MD_TEXT)

    def test_TODO(self):
        MD_TODO = "\n* [ ]item 1\n\n* [x]item 2\n\n* [ ]item 3\n\n"
        HTML_TODO = "<div><en-todo></en-todo>item 1</div><div><en-todo checked=\"true\"></en-todo>item 2</div><div><en-todo></en-todo>item 3</div>\n"
        self.assertEqual(Editor.textToENML(MD_TODO),
                         Editor.wrapENML(HTML_TODO))

        wrapped = Editor.wrapENML(HTML_TODO)
        text = Editor.ENMLtoText(wrapped)
        self.assertEqual(text, MD_TODO)

    def test_htmlEscape(self):
        wrapped = Editor.textToENML(content="<what ever>", format="markdown")
        self.assertEqual(wrapped, """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
<en-note><p>&lt;what ever&gt;</p>
</en-note>""")

    def test_not_checklist(self):
        wrapped = Editor.textToENML(content=" Item head[0]; ", format="markdown")
        self.assertEqual(wrapped, """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
<en-note><p>Item head[0]; </p>
</en-note>""")

    def test_wrapENML_success(self):
        text = "test"
        result = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
<en-note>test</en-note>'''
        self.assertEqual(Editor.wrapENML(text), result)

    def test_wrapENML_without_argument_fail(self):
        self.assertRaises(TypeError, Editor.wrapENML)
