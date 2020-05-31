from sqlalchemy.orm import create_session
import pymysql


class MySQL(object):
    def __init__(self, app=None, host=None, port=None, username=None, charset='utf-8',
                 cursors=pymysql.cursors.DictCursor):
        self.app = app
        self.Model = None
        self.cursors = cursors()

    def init_app(self, app):
        self.app = app


class Field(object):

    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type

    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)