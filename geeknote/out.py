# -*- coding: utf-8 -*-

import getpass
import threading
import _thread
import time
import datetime
import sys
import os.path

from .__init__ import __version__
from . import tools
from . import config


def preloaderPause(fn, *args, **kwargs):
    def wrapped(*args, **kwargs):
        if not preloader.isLaunch:
            return fn(*args, **kwargs)

        preloader.stop()
        result = fn(*args, **kwargs)
        preloader.launch()

        return result

    return wrapped


def preloaderStop(fn, *args, **kwargs):
    def wrapped(*args, **kwargs):
        if not preloader.isLaunch:
            return fn(*args, **kwargs)

        preloader.stop()
        result = fn(*args, **kwargs)
        return result

    return wrapped


class preloader(object):
    progress = (">  ", ">> ", ">>>", " >>", "  >", "   ")
    clearLine = "\r" + " " * 40 + "\r"
    message = None
    isLaunch = False
    counter = 0

    @staticmethod
    def setMessage(message, needLaunch=True):
        preloader.message = message
        if not preloader.isLaunch and needLaunch:
            preloader.launch()

    @staticmethod
    def launch():
        if not config.IS_OUT_TERMINAL:
            return
        preloader.counter = 0
        preloader.isLaunch = True
        _thread.start_new_thread(preloader.draw, ())

    @staticmethod
    def stop():
        if not config.IS_OUT_TERMINAL:
            return
        preloader.counter = -1
        printLine(preloader.clearLine, "")
        preloader.isLaunch = False

    @staticmethod
    def exit(code=0):
        preloader.stop()

        if threading.current_thread().__class__.__name__ == "_MainThread":
            sys.exit(code)
        else:
            _thread.exit()

    @staticmethod
    def draw():
        try:
            if not preloader.isLaunch:
                return

            while preloader.counter >= 0:
                printLine(preloader.clearLine, "")
                preloader.counter += 1
                printLine(
                    "%s : %s"
                    % (
                        preloader.progress[preloader.counter % len(preloader.progress)],
                        preloader.message,
                    ),
                    "",
                )

                time.sleep(0.3)
        except:
            pass


def _getCredentialsFromFile():
    # Get evernote credentials from file APP_DIR/credentials
    # This is used only for sandbox mode (DEV_MODE=True) for security reasons
    if config.DEV_MODE:
        creds = os.path.join(config.APP_DIR, "credentials")
        if os.path.exists(creds):
            credentials = None
            # execfile doesn't work reliably for assignments, see python docs
            with open(creds, "r") as f:
                # this sets "credentials" if correctly formatted
                exec(f.read())
            try:
                return credentials.split(":")
            except:
                sys.stderr.write(
                    """Error reading credentials from %s.
Format should be:
credentials="<username>:<password>:<two-factor auth code>"

"""
                    % creds
                )
    return None


@preloaderPause
def GetUserCredentials():
    """Prompts the user for a username and password."""
    creds = _getCredentialsFromFile()
    if creds is not None:
        return creds[:2]

    try:
        login = None
        password = None
        if login is None:
            login = rawInput("Login: ")

        if password is None:
            password = rawInput("Password: ", True)
    except (KeyboardInterrupt, SystemExit) as e:
        if e.message:
            tools.exit(e.message)
        else:
            tools.exit

    return (login, password)


@preloaderPause
def GetUserAuthCode():
    """Prompts the user for a two factor auth code."""
    creds = _getCredentialsFromFile()
    if creds is not None:
        return creds[2]

    try:
        code = None
        if code is None:
            code = rawInput("Two-Factor Authentication Code: ")
    except (KeyboardInterrupt, SystemExit) as e:
        if e.message:
            tools.exit(e.message)
        else:
            tools.exit

    return code


@preloaderStop
def SearchResult(listItems, request, **kwargs):
    """Print search results."""
    printLine("Search request: %s" % request)
    printList(listItems, **kwargs)


@preloaderStop
def SelectSearchResult(listItems, **kwargs):
    """Select a search result."""
    return printList(listItems, showSelector=True, **kwargs)


@preloaderStop
def confirm(message):
    printLine(message)
    try:
        while True:
            answer = rawInput("Yes/No: ")
            if answer.lower() in ["yes", "ye", "y"]:
                return True
            if answer.lower() in ["no", "n"]:
                return False
            failureMessage('Incorrect answer "%s", ' "please try again:\n" % answer)
    except (KeyboardInterrupt, SystemExit) as e:
        if e.message:
            tools.exit(e.message)
        else:
            tools.exit


@preloaderStop
def showNote(note, id, shardId):
    separator("#", "URL")
    printLine("NoteLink: " + (config.NOTE_LINK % (shardId, id, note.guid)))
    printLine("WebClientURL: " + (config.NOTE_WEBCLIENT_URL % note.guid))
    separator("#", "TITLE")
    printLine(note.title)
    separator("=", "META")
    printLine("Notebook: %s" % note.notebookName)
    printLine("Created: %s" % printDate(note.created))
    printLine("Updated: %s" % printDate(note.updated))
    for key, value in list(note.attributes.__dict__.items()):
        if value and key not in ("reminderOrder", "reminderTime", "reminderDoneTime"):
            printLine("%s: %s" % (key, value))
    separator("|", "REMINDERS")
    printLine("Order: %s" % str(note.attributes.reminderOrder))
    printLine("Time: %s" % printDate(note.attributes.reminderTime))
    printLine("Done: %s" % printDate(note.attributes.reminderDoneTime))
    separator("-", "CONTENT")
    if note.tagNames:
        printLine("Tags: %s" % ", ".join(note.tagNames))

    from .editor import Editor

    printLine(Editor.ENMLtoText(note.content))


@preloaderStop
def showNoteRaw(note):
    from .editor import Editor

    printLine(Editor.ENMLtoText(note.content, "pre"))


@preloaderStop
def showUser(user, fullInfo):
    separator("#", "USER INFO")
    colWidth = 17
    printLine("%s: %s" % ("Username".ljust(colWidth, " "), user.username))
    printLine("%s: %s" % ("Name".ljust(colWidth, " "), user.name))
    printLine("%s: %s" % ("Email".ljust(colWidth, " "), user.email))

    if fullInfo:
        printLine(
            "%s: %.2f MB"
            % (
                "Upload limit".ljust(colWidth, " "),
                (int(user.accounting.uploadLimit) / 1024 / 1024),
            )
        )
        printLine(
            "%s: %s"
            % (
                "Upload limit end".ljust(colWidth, " "),
                printDate(user.accounting.uploadLimitEnd),
            )
        )
        printLine("%s: %s" % ("Timezone".ljust(colWidth, " "), user.timezone))


@preloaderStop
def successMessage(message):
    """ Displaying a message. """
    printLine(message, "\n")


@preloaderStop
def failureMessage(message):
    """ Displaying a message."""
    printLine(message, "\n", sys.stderr)


def separator(symbol="", title=""):
    size = 40
    if title:
        sw = int((size - len(title) + 2) / 2)
        printLine(
            "%s %s %s" % (symbol * sw, title, symbol * (sw - (len(title) + 1) % 2))
        )

    else:
        printLine(symbol * size + "\n")


@preloaderStop
def printList(
    listItems,
    title="",
    showSelector=False,
    showByStep=0,
    showUrl=False,
    showTags=False,
    showNotebook=False,
    showGUID=False,
):

    if title:
        separator("=", title)

    total = len(listItems)
    printLine("Found %d item%s" % (total, ("s" if total != 1 else "")))
    for key, item in enumerate(listItems):
        key += 1

        printLine(
            "%s : %s%s%s%s%s%s"
            % (
                item.guid
                if showGUID and hasattr(item, "guid")
                else str(key).rjust(3, " "),
                printDate(item.created).ljust(11, " ")
                if hasattr(item, "created")
                else "",
                printDate(item.updated).ljust(11, " ")
                if hasattr(item, "updated")
                else "",
                item.notebookName.ljust(18, " ")
                if showNotebook and hasattr(item, "notebookName")
                else "",
                item.title
                if hasattr(item, "title")
                else item.name
                if hasattr(item, "name")
                else item.shareName,
                "".join([" #" + s for s in item.tagGuids])
                if showTags and hasattr(item, "tagGuids") and item.tagGuids
                else "",
                " " + (">>> " + config.NOTE_WEBCLIENT_URL % item.guid)
                if showUrl
                else "",
            )
        )

        if showByStep != 0 and key % showByStep == 0 and key < total:
            printLine("-- More --", "\r")
            tools.getch()
            printLine(" " * 12, "\r")

    if showSelector:
        printLine("  0 : -Cancel-")
        while True:
            num = rawInput(": ")
            if tools.checkIsInt(num) and 1 <= int(num) <= total:
                return listItems[int(num) - 1]
            if num == "0" or num == "q":
                exit(1)
            failureMessage('Incorrect number "%s", ' "please try again:\n" % num)

def rawInput(message, isPass=False):
    if isPass:
        data = getpass.getpass(message)
    else:
        data = input(message)
    return tools.stdinEncode(data)


# return a timezone-localized formatted representation of a UTC timestamp
def printDate(timestamp):
    if timestamp is None:
        return "None"
    else:
        return datetime.datetime.fromtimestamp(timestamp / 1000).strftime(
            config.DEF_DATE_FORMAT
        )


def printLine(line, endLine="\n", out=None):
    # "out = sys.stdout" makes it hard to mock
    if out is None:
        out = sys.stdout

    try:
        line = line.decode()
    except (UnicodeDecodeError, AttributeError):
        pass

    message = line + endLine
    message = tools.stdoutEncode(message)
    try:
        out.write(message)
    except:
        pass
    out.flush()


def printAbout():
    printLine("Version: %s" % __version__)
    printLine("Geeknote - a command line client for Evernote.")
    printLine("Use geeknote --help to read documentation.")
