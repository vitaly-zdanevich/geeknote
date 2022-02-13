# -*- coding: utf-8 -*-

import os
import datetime
import pickle

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import logging
from . import config

db_path = os.path.join(config.APP_DIR, "database.db")
engine = create_engine("sqlite:///" + db_path)
Base = declarative_base()


class Userprop(Base):
    __tablename__ = "user_props"

    id = Column(Integer, primary_key=True)
    key = Column(String(255))
    value = Column(PickleType())

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return "<Userprop('{0}','{1})>".format(self.key, self.value)


class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True)
    key = Column(String(255))
    value = Column(String(1000))

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return "<Setting('{0}','{1})>".format(self.key, self.value)


class Notebook(Base):
    __tablename__ = "notebooks"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    guid = Column(String(1000))
    timestamp = Column(DateTime(), nullable=False)

    def __init__(self, guid, name):
        self.guid = guid
        self.name = name
        self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return "<Notebook('{0}')>".format(self.name)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    tag = Column(String(255))
    guid = Column(String(1000))
    timestamp = Column(DateTime(), nullable=False)

    def __init__(self, guid, tag):
        self.guid = guid
        self.tag = tag
        self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return "<Tag('{0}')>".format(self.tag)


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    guid = Column(String(1000))
    obj = Column(PickleType())
    timestamp = Column(DateTime(), nullable=False)

    def __init__(self, guid, obj):
        self.guid = guid
        self.obj = obj
        self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return "<Note('{0}')>".format(self.timestamp)


class Search(Base):
    __tablename__ = "search"

    id = Column(Integer, primary_key=True)
    search_obj = Column(PickleType())
    timestamp = Column(DateTime(), nullable=False)

    def __init__(self, search_obj):
        self.search_obj = search_obj
        self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return "<Search('{0}')>".format(self.timestamp)


class Storage(object):
    """
    Class for using database
    """

    session = None

    def __init__(self):
        logging.debug("Storage engine : %s", engine)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def logging(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.error("%s : %s", func.__name__, str(e))
                return False

        return wrapper

    @logging
    def createUser(self, oAuthToken, info_obj):
        """
        Create a user
        oAuthToken must be not empty string
        info_obj must be not empty string
        Previous user and user's properties will be removed
        returns True if all done
        """
        if not oAuthToken:
            raise Exception("Empty oAuth token")

        if not info_obj:
            raise Exception("Empty user info")

        for item in self.session.query(Userprop).all():
            self.session.delete(item)

        self.setUserprop("oAuthToken", oAuthToken)
        self.setUserprop("info", info_obj)

        return True

    @logging
    def removeUser(self):
        """
        Remove user
        returns True if all done
        """
        for item in self.session.query(Userprop).all():
            self.session.delete(item)
        self.session.commit()
        return True

    @logging
    def getUserToken(self):
        """
        Get user's oAuth token
        returns oAuth token if it exists
        returns None if there is no oAuth token yet
        """
        return self.getUserprop("oAuthToken")

    @logging
    def getUserInfo(self):
        """
        Get user's "info" property value
        returns info property value if it exists
        returns None if there is no info property
        """
        return self.getUserprop("info")

    @logging
    def getUserprops(self):
        """
        Get all user properties
        returns list of dict if all done
        returns [] if there are not any user properties yet
        """
        props = self.session.query(Userprop).all()
        return [{item.key: pickle.loads(item.value)} for item in props]

    @logging
    def getUserprop(self, key):
        """
        Get user property by key
        returns property's value if it the property exists
        returns None if the property doesn't exist
        """
        instance = self.session.query(Userprop).filter_by(key=key).first()
        if instance:
            return pickle.loads(instance.value)
        else:
            return None

    @logging
    def setUserprop(self, key, value):
        """
        Set a single user property
        User's property must have key and value
        returns True if all done
        """
        value = pickle.dumps(value)

        instance = self.session.query(Userprop).filter_by(key=key).first()
        if instance:
            instance.value = value
        else:
            instance = Userprop(key, value)
            self.session.add(instance)

        self.session.commit()
        return True

    @logging
    def delUserprop(self, key):
        """
        Delete a single user property
        User property must have key
        returns True if all done
        returns False if property didn't exist
        """
        instance = self.session.query(Userprop).filter_by(key=key).first()
        if instance:
            self.session.delete(instance)
            return True
        return False

    @logging
    def setSettings(self, settings):
        """
        Set multiple settings
        Settings must be an instance dict
        returns True if all done
        """
        if not isinstance(settings, dict):
            raise Exception("Wrong settings")

        for key in list(settings.keys()):
            if not settings[key]:
                raise Exception("Wrong setting's item")

            instance = self.session.query(Setting).filter_by(key=key).first()
            if instance:
                instance.value = pickle.dumps(settings[key])
            else:
                instance = Setting(key, pickle.dumps(settings[key]))
                self.session.add(instance)

        self.session.commit()
        return True

    @logging
    def getSettings(self):
        """
        Get all settings
        returns list of dict if all done
        returns {} there are not any settings yet
        """
        settings = self.session.query(Setting).all()
        result = {}
        for item in settings:
            result[item.key] = pickle.loads(item.value)
        return result

    @logging
    def setSetting(self, key, value):
        """
        Set single setting
        Setting must have key and value
        returns True if all done
        """
        instance = self.session.query(Setting).filter_by(key=key).first()
        if instance:
            instance.value = value
        else:
            instance = Setting(key, value)
            self.session.add(instance)

        self.session.commit()
        return True

    @logging
    def getSetting(self, key):
        """
        Get a setting by key
        returns setting's value if setting exists
        returns None if setting doesn't exist
        """
        instance = self.session.query(Setting).filter_by(key=key).first()
        if instance:
            return instance.value
        else:
            return None

    @logging
    def setTags(self, tags):
        """
        Set tags
        Tags must be an instance of dict
        Previous tags items will be removed
        returns True if all done
        """
        if not isinstance(tags, dict):
            raise Exception("Wrong tags")

        for item in self.session.query(Tag).all():
            self.session.delete(item)

        for key in list(tags.keys()):
            if not tags[key]:
                raise Exception("Wrong tag's item")

            instance = Tag(key, tags[key])
            self.session.add(instance)

        self.session.commit()
        return True

    @logging
    def getTags(self):
        """
        Get all tags
        returns list of dicts of tags if all done
        returns {} if there are not any tags yet
        """
        tags = self.session.query(Tag).all()
        result = {}
        for item in tags:
            result[item.guid] = item.tag
        return result

    @logging
    def setNotebooks(self, notebooks):
        """
        Set notebooks
        Notebooks must be an instance of dict
        Previous notebooks items will be removed
        returns True if all done
        """
        if not isinstance(notebooks, dict):
            raise Exception("Wrong notebooks")

        for item in self.session.query(Notebook).all():
            self.session.delete(item)

        for key in list(notebooks.keys()):
            if not notebooks[key]:
                raise Exception("Wrong notebook's item")

            instance = Notebook(key, notebooks[key])
            self.session.add(instance)

        self.session.commit()
        return True

    @logging
    def getNotebooks(self):
        """
        Get all notebooks
        returns list of notebooks if all done
        returns {} there are not any notebooks yet
        """
        notebooks = self.session.query(Notebook).all()
        result = {}
        for item in notebooks:
            result[item.guid] = item.name
        return result

    @logging
    def setNote(self, obj):
        """
        Remembers a note, indexed by GUID
        Note can be retrieved by GUID later
        returns True
        """
        for item in self.session.query(Note).filter(Note.guid == obj.guid).all():
            self.session.delete(item)

        note = pickle.dumps(obj)
        instance = Note(obj.guid, note)
        self.session.add(instance)

        self.session.commit()
        return True

    @logging
    def getNote(self, guid):
        """
        Get note by GUID
        returns note if found by GUID
        returns None if note is not found
        """
        note = self.session.query(Note).filter(Note.guid == guid).first()
        if note:
            return pickle.loads(note.obj)
        else:
            return None

    @logging
    def setSearch(self, search_obj):
        """
        Remembers a search
        Previous searching items will be removed
        return True if all done
        """
        for item in self.session.query(Search).all():
            self.session.delete(item)

        search = pickle.dumps(search_obj)
        instance = Search(search)
        self.session.add(instance)

        self.session.commit()
        return True

    @logging
    def getSearch(self):
        """
        Get last search
        return last search if it exists
        return None there are not any searches yet
        """
        search = self.session.query(Search).first()
        if search:
            return pickle.loads(search.search_obj)
        else:
            return None
