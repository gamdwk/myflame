from werkzeug.datastructures import CallbackDict
from uuid import uuid4
import base64
from .gobal import request, current_app, session
from .wrappers import Request, Response

response = Response()

request = Request()


class Session(CallbackDict):

    def __init__(self, sid, data=None, permanent=None, salt=None):
        def on_update(self):
            pass
        self.sid = sid
        if permanent:
            self.permanent = permanent
        super(Session, self).__init__(data, on_update)


class SessionInterface(object):
    session_class = Session
    __session_map = None

    @staticmethod
    def create_sid():
        return uuid4()

    def make_null_session(self,app=current_app):
        return self.session_class(self.create_sid(app))

    @property
    def session_map(self):
        return self.__session_map

    @staticmethod
    def get_sid(app=current_app):
        return request.cookies.get(app.config['SESSION_NAME'])

    @staticmethod
    def is_http_only(app=current_app):
        return app.config.get('SESSION_HTTP_ONLY')

    @staticmethod
    def get_secret_key(app=current_app):
        return app.config.get("SECRET_KEY")

    def open_session(self):
        sid = request.cookies.get(current_app.config['SESSION_NAME'])
        return self.session_class(sid)

    def save_session(self, response):
        sid =
        if sid is None:
            sid = self.create_sid()
        base64.b64decode()
        response.set_cookie()
