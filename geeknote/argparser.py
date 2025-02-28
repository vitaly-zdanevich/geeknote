# -*- coding: utf-8 -*-

from .log import logging
from . import out


COMMANDS_DICT = {
    # User
    "user": {
        "help": "Show information about active user.",
        "flags": {
            "--full": {
                "help": "Show full information.",
                "value": True,
                "default": False,
            }
        },
    },
    "login": {"help": "Authorize in Evernote."},
    "logout": {
        "help": "Logout from Evernote.",
        "flags": {
            "--force": {
                "help": "Don't ask about logging out.",
                "value": True,
                "default": False,
            }
        },
    },
    "settings": {
        "help": "Show and edit current settings.",
        "arguments": {
            "--editor": {
                "help": "Set the editor, which use to edit and create notes.",
                "emptyValue": "#GET#",
            },
            "--note_ext": {
                "help": "Set default note's extension for markdown "
                "and raw formats."
                "\n             Defaults to '.markdown, .org'",
                "emptyValue": "#GET#",
            },
            "--extras": {
                "help": "Set the markdown2 extra syntax, which use "
                "to convert markdown text to HTML.  "
                "\n             Please visit "
                "http://tinyurl.com/q459lur "
                "to get detail.",
                "emptyValue": "#GET#",
            },
        },
    },
    # Notes
    "create": {
        "help": "Create note in Evernote.",
        "arguments": {
            "--title": {"altName": "-t", "help": "The note title.", "required": True},
            "--content": {
                "altName": "-c",
                "help": "The note content.",
                "value": True,
                "default": "WRITE",
            },
            "--tag": {
                "altName": "-tg",
                "help": "Tag to be added to the note.",
                "repetitive": True,
            },
            "--created": {
                "altName": "-cr",
                "help": "Set local creation time in 'yyyy-mm-dd'"
                " or 'yyyy-mm-dd HH:MM' format.",
            },
            "--resource": {
                "altName": "-rs",
                "help": "Add a resource to the note.",
                "repetitive": True,
            },
            "--notebook": {
                "altName": "-nb",
                "help": "Set the notebook where to save note.",
            },
            "--reminder": {
                "altName": "-r",
                "help": "Set local reminder date and time in 'yyyy-mm-dd'"
                " or 'yyyy-mm-dd HH:MM' format."
                "\n             Alternatively use TOMORROW "
                "and WEEK for 24 hours and a week ahead "
                "respectively,"
                "\n             NONE for a reminder "
                "without a time. Use DONE to mark a "
                "reminder as completed.",
            },
            "--url": {"altname": "-u", "help": "Set the URL for the note."},
        },
        "flags": {
            "--raw": {
                "altName": "-r",
                "help": "Edit note with raw ENML",
                "value": True,
                "default": False,
            },
            "--rawmd": {
                "altName": "-rm",
                "help": "Edit note with raw markdown",
                "value": True,
                "default": False,
            },
        },
    },
    "create-linked": {
        "help": "Create Linked note in Evernote",
        "firstArg": "--notebook",
        "arguments": {
            "--title": {"altName": "-t", "help": "The note title.", "required": True},
            "--notebook": {
                "alt-name": "-nb",
                "help": "Name of the linked notebook in which to create this note.",
                "required": True,
            },
        },
    },
    "find": {
        "help": "Search notes in Evernote.",
        "firstArg": "--search",
        "arguments": {
            "--search": {"altName": "-s", "help": "Text to search.", "emptyValue": "*"},
            "--tag": {
                "altName": "-tg",
                "help": "Tag sought on the notes.",
                "repetitive": True,
            },
            "--notebook": {"altName": "-nb", "help": "Notebook containing the notes."},
            "--date": {
                "altName": "-d",
                "help": "Set date in 'yyyy-mm-dd' format or "
                "date range 'yyyy-mm-dd/yyyy-mm-dd' format.",
            },
            "--count": {
                "altName": "-cn",
                "help": "How many notes to show in the result list.",
                "type": int,
            },
        },
        "flags": {
            "--content-search": {
                "altName": "-cs",
                "help": "Search by content, not by title.",
                "value": True,
                "default": False,
            },
            "--exact-entry": {
                "altName": "-ee",
                "help": "Search for exact entry of the request.",
                "value": True,
                "default": False,
            },
            "--guid": {
                "altName": "-id",
                "help": "Replace ID with GUID of each note in results.",
                "value": True,
                "default": False,
            },
            "--ignore-completed": {
                "altName": "-C",
                "help": "Include only unfinished reminders",
                "value": True,
                "default": False,
            },
            "--reminders-only": {
                "altName": "-R",
                "help": "Include only notes with a reminder.",
                "value": True,
                "default": False,
            },
            "--deleted-only": {
                "altName": "-D",
                "help": "Include only notes that have been deleted.",
                "value": True,
                "default": False,
            },
            "--with-notebook": {
                "altName": "-wn",
                "help": "Add notebook of each note in results.",
                "value": True,
                "default": False,
            },
            "--with-tags": {
                "altName": "-wt",
                "help": "Add tag list of each note in results.",
                "value": True,
                "default": False,
            },
            "--with-url": {
                "altName": "-wu",
                "help": "Add direct url of each note "
                "in results to Evernote web-version.",
                "value": True,
                "default": False,
            },
        },
    },
    "edit": {
        "help": "Edit note in Evernote.",
        "firstArg": "--note",
        "arguments": {
            "--note": {
                "altName": "-n",
                "help": "The name or GUID or ID from the "
                "previous search of a note to edit.",
                "required": True,
            },
            "--title": {"altName": "-t", "help": "Set new title of the note."},
            "--content": {"altName": "-c", "help": "Set new content of the note."},
            "--resource": {
                "altName": "-rs",
                "help": "Add a resource to the note.",
                "repetitive": True,
            },
            "--tag": {
                "altName": "-tg",
                "help": "Set new tag for the note.",
                "repetitive": True,
            },
            "--created": {
                "altName": "-cr",
                "help": "Set local creation time in 'yyyy-mm-dd'"
                " or 'yyyy-mm-dd HH:MM' format.",
            },
            "--notebook": {
                "altName": "-nb",
                "help": "Assign new notebook for the note.",
            },
            "--reminder": {
                "altName": "-r",
                "help": "Set local reminder date and time in 'yyyy-mm-dd'"
                " or 'yyyy-mm-dd HH:MM' format."
                "\n             Alternatively use TOMORROW "
                "and WEEK for 24 hours and a week ahead "
                "respectively,"
                "\n             NONE for a reminder "
                "without a time. Use DONE to mark a "
                "reminder as completed."
                "\n             Use DELETE to remove "
                "reminder from a note.",
            },
            "--url": {"altname": "-u", "help": "Set the URL for the note."},
        },
        "flags": {
            "--raw": {
                "altName": "-r",
                "help": "Edit note with raw ENML",
                "value": True,
                "default": False,
            },
            "--rawmd": {
                "altName": "-rm",
                "help": "Edit note with raw markdown",
                "value": True,
                "default": False,
            },
        },
    },
    "edit-linked": {
        "help": "Edit linked note in a shared notebook.",
        "firstArg": "--notebook",
        "arguments": {
            "--notebook": {
                "altName": "-nb",
                "help": "Name of the linked Notebook in which the note resides.",
                "required": True,
            },
            "--note": {
                "altName": "-n",
                "help": "Title of the Note you want to edit.",
                "required": True,
            },
        },
    },
    "show": {
        "help": "Output note in the terminal.",
        "firstArg": "--note",
        "arguments": {
            "--note": {
                "altName": "-n",
                "help": "The name or GUID or ID from the previous "
                "search of a note to show.",
                "required": True,
            }
        },
        "flags": {
            "--raw": {
                "altName": "-w",
                "help": "Show the raw note body",
                "value": True,
                "default": False,
            }
        },
    },
    "remove": {
        "help": "Remove note from Evernote.",
        "firstArg": "--note",
        "arguments": {
            "--note": {
                "altName": "-n",
                "help": "The name or GUID or ID from the previous "
                "search of a note to remove.",
                "required": True,
            }
        },
        "flags": {
            "--force": {
                "altName": "-f",
                "help": "Don't ask about removing.",
                "value": True,
                "default": False,
            }
        },
    },
    "dedup": {
        "help": "Find and remove duplicate notes in Evernote.",
        "arguments": {
            "--notebook": {
                "altName": "-nb",
                "help": "In which notebook search for duplicates.",
            }
        },
    },
    # Notebooks
    "notebook-list": {
        "help": "Show the list of existing notebooks in your Evernote.",
        "flags": {
            "--guid": {
                "altName": "-id",
                "help": "Replace ID with GUID of each notebook in results.",
                "value": True,
                "default": False,
            }
        },
    },
    "notebook-create": {
        "help": "Create new notebook.",
        "arguments": {
            "--title": {
                "altName": "-t",
                "help": "Set the title of new notebook.",
                "required": True,
            },
            "--stack": {"help": "Specify notebook stack container."},
        },
    },
    "notebook-edit": {
        "help": "Edit/rename notebook.",
        "firstArg": "--notebook",
        "arguments": {
            "--notebook": {
                "altName": "-nb",
                "help": "The name of a notebook to rename.",
                "required": True,
            },
            "--title": {"altName": "-t", "help": "Set the new name of notebook."},
        },
    },
    "notebook-remove": {
        "help": "Remove notebook.",
        "firstArg": "--notebook",
        "arguments": {
            "--notebook": {
                "altName": "-nb",
                "help": "The name of a notebook to remove.",
                "required": True,
            }
        },
        "flags": {
            "--force": {
                "help": "Don't ask about removing notebook.",
                "value": True,
                "default": False,
            }
        },
    },
    # Tags
    "tag-list": {
        "help": "Show the list of existing tags in your Evernote.",
        "flags": {
            "--guid": {
                "altName": "-id",
                "help": "Replace ID with GUID of each note in results.",
                "value": True,
                "default": False,
            }
        },
    },
    "tag-create": {
        "help": "Create new tag.",
        "arguments": {
            "--title": {
                "altName": "-t",
                "help": "Set the title of new tag.",
                "required": True,
            }
        },
    },
    "tag-edit": {
        "help": "Edit/rename tag.",
        "firstArg": "--tagname",
        "arguments": {
            "--tagname": {
                "altName": "-tgn",
                "help": "The name of a tag to rename.",
                "required": True,
            },
            "--title": {"altName": "-t", "help": "Set the new name of tag."},
        },
    },
}
"""
    "tag-remove": {
        "help": "Remove tag.",
        "firstArg": "--tagname",
        "arguments": {
            "--tagname": {"help": "The name of a tag to remove.",
                          "required": True},
        },
        "flags": {
            "--force": {"help": "Don't ask about removing.",
                        "value": True,
                        "default": False},
        }
    },
"""


class argparser(object):

    COMMANDS = COMMANDS_DICT
    sys_argv = None

    def __init__(self, sys_argv):
        self.sys_argv = sys_argv
        self.LVL = len(sys_argv)
        self.INPUT = sys_argv

        # list of commands
        self.CMD_LIST = list(self.COMMANDS.keys())
        # command
        self.CMD = None if self.LVL == 0 else self.INPUT[0]
        # list of possible arguments of the command line
        self.CMD_ARGS = (
            self.COMMANDS[self.CMD]["arguments"]
            if self.LVL > 0
            and self.CMD in self.COMMANDS
            and "arguments" in self.COMMANDS[self.CMD]
            else {}
        )
        # list of possible flags of the command line
        self.CMD_FLAGS = (
            self.COMMANDS[self.CMD]["flags"]
            if self.LVL > 0
            and self.CMD in self.COMMANDS
            and "flags" in self.COMMANDS[self.CMD]
            else {}
        )
        # list of entered arguments and their values
        self.INP = [] if self.LVL <= 1 else self.INPUT[1:]

        logging.debug("CMD_LIST : %s", str(self.CMD_LIST))
        logging.debug("CMD: %s", str(self.CMD))
        logging.debug("CMD_ARGS : %s", str(self.CMD_ARGS))
        logging.debug("CMD_FLAGS : %s", str(self.CMD_FLAGS))
        logging.debug("INP : %s", str(self.INP))

    def parse(self):
        self.INP_DATA = {}

        if self.CMD is None:
            out.printAbout()
            return False

        if self.CMD == "autocomplete":
            # substitute arguments for AutoComplete
            # 1 offset to make the argument as 1 is autocomplete
            self.__init__(self.sys_argv[1:])
            self.printAutocomplete()
            return False

        if self.CMD == "--help":
            self.printHelp()
            return False

        if self.CMD not in self.COMMANDS:
            self.printErrorCommand()
            return False

        if "--help" in self.INP:
            self.printHelp()
            return False

        # prepare data
        for arg, params in list(self.CMD_ARGS.items()) + list(self.CMD_FLAGS.items()):
            # set values by default
            if "default" in params:
                self.INP_DATA[arg] = params["default"]

            # replace `altName` entered arguments on full
            if "altName" in params and params["altName"] in self.INP:
                self.INP[self.INP.index(params["altName"])] = arg

        activeArg = None
        ACTIVE_CMD = None
        # check and insert first argument by default
        if "firstArg" in self.COMMANDS[self.CMD]:
            firstArg = self.COMMANDS[self.CMD]["firstArg"]
            if len(self.INP) > 0:
                # Check that first argument is a default argument
                # and another argument.
                if self.INP[0] not in (list(self.CMD_ARGS.keys()) + list(self.CMD_FLAGS.keys())):
                    self.INP = [firstArg] + self.INP
            else:
                self.INP = [firstArg]

        for item in self.INP:
            # check what are waiting the argument
            if activeArg is None:
                # actions for the argument
                if item in self.CMD_ARGS:
                    activeArg = item
                    ACTIVE_CMD = self.CMD_ARGS[activeArg]

                # actions for the flag
                elif item in self.CMD_FLAGS:
                    self.INP_DATA[item] = self.CMD_FLAGS[item]["value"]

                # error. parameter is not found
                else:
                    self.printErrorArgument(item)
                    return False

            else:
                activeArgTmp = None
                # values it is parameter
                if item in self.CMD_ARGS or item in self.CMD_FLAGS:
                    # active argument is "emptyValue"
                    if "emptyValue" in ACTIVE_CMD:
                        activeArgTmp = item  # remember the new "active" argument
                        item = ACTIVE_CMD[
                            "emptyValue"
                        ]  # set the active argument to emptyValue
                    # Error, "active" argument has no values
                    else:
                        self.printErrorArgument(activeArg, item)
                        return False

                if "type" in ACTIVE_CMD:
                    convType = ACTIVE_CMD["type"]
                    if convType not in (int, str):
                        logging.error("Unsupported argument type: %s", convType)
                        return False
                    try:
                        item = convType(item)
                    except:
                        self.printErrorArgument(activeArg, item)
                        return False

                if activeArg in self.INP_DATA:
                    if "repetitive" in ACTIVE_CMD and (ACTIVE_CMD["repetitive"]):
                        """ append """
                        self.INP_DATA[activeArg] += [item]
                    else:
                        """ replace """
                        self.INP_DATA[activeArg] = item
                else:
                    """ set """
                    if "repetitive" in ACTIVE_CMD and (ACTIVE_CMD["repetitive"]):
                        self.INP_DATA[activeArg] = [item]
                    else:
                        self.INP_DATA[activeArg] = item

                activeArg = (
                    activeArgTmp
                )  # this is either a new "active" argument or emptyValue.

        # if there are still active arguments
        if activeArg is not None:
            # if the active argument is emptyValue
            if "emptyValue" in ACTIVE_CMD:
                self.INP_DATA[activeArg] = ACTIVE_CMD["emptyValue"]

            # An error argument
            else:
                self.printErrorArgument(activeArg, "")
                return False

        # check whether there is a necessary argument request
        for arg, params in list(self.CMD_ARGS.items()) + list(self.CMD_FLAGS.items()):
            if "required" in params and arg not in self.INP:
                self.printErrorReqArgument(arg)
                return False

        # trim -- and ->_
        self.INP_DATA = dict(
            [key.lstrip("-").replace("-", "_"), val]
            for key, val in list(self.INP_DATA.items())
        )
        return self.INP_DATA

    def printAutocomplete(self):
        # checking later values
        LAST_VAL = self.INP[-1] if self.LVL > 1 else None
        PREV_LAST_VAL = self.INP[-2] if self.LVL > 2 else None
        ARGS_FLAGS_LIST = list(self.CMD_ARGS.keys()) + list(self.CMD_FLAGS.keys())

        # print root grid
        if self.CMD is None:
            self.printGrid(self.CMD_LIST)

        # work with root commands
        elif not self.INP:

            # print arguments if a root command is found
            if self.CMD in self.CMD_LIST:
                self.printGrid(ARGS_FLAGS_LIST)

            # autocomplete for sub-commands
            else:
                # filter out irrelevant commands
                self.printGrid(
                    [item for item in self.CMD_LIST if item.startswith(self.CMD)]
                )

        # processing arguments
        else:

            # filter out arguments that have not been input
            if PREV_LAST_VAL in self.CMD_ARGS or LAST_VAL in self.CMD_FLAGS:
                self.printGrid(
                    [item for item in ARGS_FLAGS_LIST if item not in self.INP]
                )

            # autocomplete for part of the command
            elif PREV_LAST_VAL not in self.CMD_ARGS:
                self.printGrid(
                    [
                        item
                        for item in ARGS_FLAGS_LIST
                        if item not in self.INP and item.startswith(LAST_VAL)
                    ]
                )

            # processing of the arguments
            else:
                print("")  # "Please_input_%s" % INP_ARG.replace('-', '')

    def printGrid(self, list):
        out.printLine(" ".join(list))

    def printErrorCommand(self):
        out.printLine('Unexpected command "%s"' % (self.CMD))
        self.printHelp()

    def printErrorReqArgument(self, errorArg):
        out.printLine(
            'Not found required argument "%s" '
            'for command "%s" ' % (errorArg, self.CMD)
        )
        self.printHelp()

    def printErrorArgument(self, errorArg, errorVal=None):
        if errorVal is None:
            out.printLine(
                'Unexpected argument "%s" ' 'for command "%s"' % (errorArg, self.CMD)
            )
        else:
            out.printLine(
                'Unexpected value "%s" ' 'for argument "%s"' % (errorVal, errorArg)
            )
        self.printHelp()

    def printHelp(self):
        if self.CMD is None or self.CMD not in self.COMMANDS:
            tab = len(max(list(self.COMMANDS.keys()), key=len))
            out.printLine("Available commands:")
            for cmd in sorted(self.COMMANDS):
                out.printLine(
                    "%s : %s" % (cmd.rjust(tab, " "), self.COMMANDS[cmd]["help"])
                )

        else:

            tab = len(max(list(self.CMD_ARGS.keys()) + list(self.CMD_FLAGS.keys()), key=len))

            out.printLine("Options for: %s" % self.CMD)
            out.printLine("Available arguments:")
            for arg in self.CMD_ARGS:
                out.printLine(
                    "%s : %s%s"
                    % (
                        arg.rjust(tab, " "),
                        "[default] "
                        if "firstArg" in self.COMMANDS[self.CMD]
                        and self.COMMANDS[self.CMD]["firstArg"] == arg
                        else "",
                        self.CMD_ARGS[arg]["help"],
                    )
                )

            if self.CMD_FLAGS:
                out.printLine("Available flags:")
                for flag in self.CMD_FLAGS:
                    out.printLine(
                        "%s : %s" % (flag.rjust(tab, " "), self.CMD_FLAGS[flag]["help"])
                    )
