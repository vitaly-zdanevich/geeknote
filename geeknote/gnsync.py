#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import glob
import logging
import string
import unicodedata, re
import hashlib, binascii, mimetypes

import evernote.edam.type.ttypes as Types
from bs4 import BeautifulSoup

from geeknote import GeekNote
from storage import Storage
from editor import Editor
import tools


# set default logger (write log to file)
def_logpath = os.path.join(os.getenv('USERPROFILE') or os.getenv('HOME'),  'GeekNoteSync.log')
formatter = logging.Formatter('%(asctime)-15s : %(message)s')
handler = logging.FileHandler(def_logpath)
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

# http://stackoverflow.com/a/93029
CONTROL_CHARS = ''.join(c for c in (unichr(i) for i in xrange(0x110000)) \
                        if c not in string.printable and unicodedata.category(c) == 'Cc')
CONTROL_CHARS_RE = re.compile('[%s]' % re.escape(CONTROL_CHARS))
def remove_control_characters(s):
    return CONTROL_CHARS_RE.sub('', s)

def log(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception, e:
            logger.error("%s", str(e))
    return wrapper


@log
def reset_logpath(logpath):
    """
    Reset logpath to path from command line
    """
    global logger

    if not logpath:
        return

    # remove temporary log file if it's empty
    if os.path.isfile(def_logpath):
        if os.path.getsize(def_logpath) == 0:
            os.remove(def_logpath)

    # save previous handlers
    handlers = logger.handlers

    # remove old handlers
    for handler in handlers:
        logger.removeHandler(handler)

    # try to set new file handler
    handler = logging.FileHandler(logpath)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class GNSync:

    notebook_name = None
    path = None
    mask = None
    twoway = None

    notebook_guid = None
    all_set = False

    @log
    def __init__(self, notebook_name, path, mask, format, twoway=False):
        # check auth
        if not Storage().getUserToken():
            raise Exception("Auth error. There is not any oAuthToken.")

        #set path
        if not path:
            raise Exception("Path to sync directories does not select.")

        if not os.path.exists(path):
            raise Exception("Path to sync directories does not exist.")

        self.path = path

        #set mask
        if not mask:
            mask = "*.*"

        self.mask = mask

        #set format
        if not format:
            format = "plain"

        self.format = format

        if format == "markdown":
            self.extension = ".md"
        elif format == "html":
            self.extension = ".html"
        else:
            self.extension = ".txt"

        self.twoway = twoway

        logger.info('Sync Start')

        #set notebook
        self.notebook_guid,\
        self.notebook_name = self._get_notebook(notebook_name, path)

        # all is Ok
        self.all_set = True

    @log
    def sync(self):
        """
        Synchronize files to notes
        TODO: add two way sync with meta support
        TODO: add specific notebook support
        """
        if not self.all_set:
            return

        files = self._get_files()
        notes = self._get_notes()

        for f in files:
            has_note = False
            meta = self._parse_meta(self._get_file_content(f['path']))
            title = f['name'] if 'title' not in meta else meta['title'].strip()
            tags = None if 'tags' not in meta else meta['tags'] \
                   .replace('[', '').replace(']','').split(',')
            tags = None if tags == '' else map(lambda x:x.strip(), tags)
            note = None
            if self.format == 'html':
                meta['mtime'] = f['mtime']
                note = self._html2note(meta)
                
            for n in notes:
                if title == n.title:
                    has_note = True
                    if f['mtime'] > n.updated:
                        if self.format == 'html':
                            gn = GeekNote()
                            note.guid = n.guid
                            gn.getNoteStore().updateNote(gn.authToken, note)                            
                            logger.info('Note "{0}" was updated'.format(note.title))
                        else:
                            self._update_note(f, n, title, meta['content'], tags)
                        break

            if not has_note:
                if self.format == 'html':
                    gn = GeekNote()
                    gn.getNoteStore().createNote(gn.authToken, note)
                    logger.info('Note "{0}" was created'.format(note.title))
                else:
                    self._create_note(f, title, meta['content'], tags)

        if self.twoway:
            for n in notes:
                has_file = False
                for f in files:
                    if f['name'] == n.title:
                        has_file = True
                        if f['mtime'] < n.updated:
                            self._update_file(f, n)
                            break

                if not has_file:
                    self._create_file(n)

        logger.info('Sync Complete')

    @log
    def _parse_meta(self, content):
        """
        Parse jekyll metadata of note, eg:
        ---
        layout: post
        title: draw uml with emacs
        tags: [uml, emacs]
        categories: [dev]
        ---
        and substitute meta from content.

        Caution: meta data will only work in one way
        mode! And I will never use two way mode, so
        two way sync will need your additional work!
        """
        metaBlock = re.compile("---(.*?)---", re.DOTALL)
        metaInfo = re.compile("(\w+):\s*?(.*)")
        block = metaBlock.search(content)
        if block is not None:
            info = metaInfo.findall(block.group(0))
            ret = dict(info)
            ret['content'] = metaBlock.sub('', content)
            return ret
            
    @log        
    def _html2note(self, meta):
        """
        parse html to note
        TODO: check if evernote need upload media evertime when update
        """
        note = Types.Note()
        note.title = meta['title'].strip() if 'title' in meta else None
        tags = None if 'tags' not in meta else meta['tags'] \
                   .replace('[', '').replace(']','').split(',')
        tags = None if tags == '' else map(lambda x:x.strip(), tags)
        note.tagNames = tags
        note.created = meta['mtime']
        note.resources = []
        soup = BeautifulSoup(meta['content'], 'html.parser')
        for tag in soup.findAll('img'): #image support is enough
            if 'src' in tag.attrs and len(tag.attrs['src']) > 0:
                img = None
                with open(tag.attrs['src'], 'rb') as f:
                    img = f.read()    
                md5 = hashlib.md5()
                md5.update(img)
                hash = md5.digest()
                hexHash = binascii.hexlify(hash)
                mime = mimetypes.guess_type(tag['src'])[0]

                data = Types.Data()
                data.size = len(img)
                data.bodyHash = hash
                data.body = img

                resource = Types.Resource()
                resource.mime = mime
                resource.data = data
                
                tag.name = 'en-media'
                tag.attrs['type'] = mime
                tag.attrs['hash'] = hexHash
                tag.attrs.pop('src', None)

                note.resources.append(resource)
        note.notebookGuid = self.notebook_guid
        note.content = str(soup)
        return note
                
        
    @log
    def _update_note(self, file_note, note, title = None, content = None, tags = None):
        """
        Updates note from file
        """
        #content = self._get_file_content(file_note['path']) if content is None else content
        
        result = GeekNote().updateNote(
            guid=note.guid,
            title=title or note.title,
            content=content or self._get_file_content(file_note['path']),
            tags = tags or note.tagNames,
            notebook=self.notebook_guid)

        if result:
            logger.info('Note "{0}" was updated'.format(note.title))
        else:
            raise Exception('Note "{0}" was not updated'.format(note.title))

        return result

    @log
    def _update_file(self, file_note, note):
        """
        Updates file from note
        """
        GeekNote().loadNoteContent(note)
        content = Editor.ENMLtoText(note.content)
        open(file_note['path'], "w").write(content)

    @log
    def _create_note(self, file_note, title = None, content = None, tags = None):
        """
        Creates note from file
        """

        content = content or self._get_file_content(file_note['path'])

        if content is None:
            return

        result = GeekNote().createNote(
            title=title or file_note['name'],
            content=content, 
            notebook=self.notebook_guid,
            tags = tags or None,
            created=file_note['mtime'])

        if result:
            logger.info('Note "{0}" was created'.format(title or file_note['name']))
        else:
            raise Exception('Note "{0}" was not' \
                            ' created'.format(title or file_note['name']))

        return result

    @log
    def _create_file(self, note):
        """
        Creates file from note
        """
        GeekNote().loadNoteContent(note)
        content = Editor.ENMLtoText(note.content)
        path = os.path.join(self.path, note.title + self.extension)
        open(path, "w").write(content)
        return True

    @log
    def _get_file_content(self, path):
        """
        Get file content.
        """
        content = open(path, "r").read()

        # strip unprintable characters
        content = remove_control_characters(content.decode('utf-8')).encode('utf-8')
        content = Editor.textToENML(content=content, raise_ex=True, format=self.format)
        
        if content is None:
            logger.warning("File {0}. Content must be " \
                           "an UTF-8 encode.".format(path))
            return None

        return content

    @log
    def _get_notebook(self, notebook_name, path):
        """
        Get notebook guid and name.
        Takes default notebook if notebook's name does not select.
        """
        notebooks = GeekNote().findNotebooks()

        if not notebook_name:
            notebook_name = os.path.basename(os.path.realpath(path))

        notebook = [item for item in notebooks if item.name == notebook_name]
        guid = None
        if notebook:
            guid = notebook[0].guid

        if not guid:
            notebook = GeekNote().createNotebook(notebook_name)

            if(notebook):
                logger.info('Notebook "{0}" was' \
                            ' created'.format(notebook_name))
            else:
                raise Exception('Notebook "{0}" was' \
                                ' not created'.format(notebook_name))

            guid = notebook.guid

        return (guid, notebook_name)

    @log
    def _get_files(self):
        """
        Get files by self.mask from self.path dir.
        """

        file_paths = glob.glob(os.path.join(self.path, self.mask))

        files = []
        for f in file_paths:
            if os.path.isfile(f):
                file_name = os.path.basename(f)
                file_name = os.path.splitext(file_name)[0]

                mtime = int(os.path.getmtime(f) * 1000)

                files.append({'path': f, 'name': file_name, 'mtime': mtime})

        return files

    @log
    def _get_notes(self):
        """
        Get notes from evernote.
        """
        keywords = 'notebook:"{0}"'.format(tools.strip(self.notebook_name))
        return GeekNote().findNotes(keywords, 10000).notes


def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--path', '-p', action='store', help='Path to synchronize directory')
        parser.add_argument('--mask', '-m', action='store', help='Mask of files to synchronize. Default is "*.*"')
        parser.add_argument('--format', '-f', action='store', default='plain', choices=['plain', 'markdown', 'html'], help='The format of the file contents. Default is "plain". Valid values are "plain" "html" and "markdown"')
        parser.add_argument('--notebook', '-n', action='store', help='Notebook name for synchronize. Default is default notebook')
        parser.add_argument('--logpath', '-l', action='store', help='Path to log file. Default is GeekNoteSync in home dir')
        parser.add_argument('--two-way', '-t', action='store', help='Two-way sync')

        args = parser.parse_args()

        path = args.path if args.path else None
        mask = args.mask if args.mask else None
        format = args.format if args.format else None
        notebook = args.notebook if args.notebook else None
        logpath = args.logpath if args.logpath else None
        twoway = True if args.two_way else False

        reset_logpath(logpath)

        GNS = GNSync(notebook, path, mask, format, twoway)
        GNS.sync()

    except (KeyboardInterrupt, SystemExit, tools.ExitException):
        pass

    except Exception, e:
        logger.error(str(e))

if __name__ == "__main__":
    main()
