from werkzeug.datastructures import CallbackDict
from uuid import uuid4
import base64
from datetime import timedelta
from .gobal import current_app, session


class Session(CallbackDict):
    changed = False

    def __init__(self, sid, data=None, permanent=None):
        self.sid = sid

        def on_update(self):
            self.changed = True

        if permanent:
            # permanent=timedelta(days=7)
            self.permanent = permanent.total_seconds()
        super(Session, self).__init__(data, on_update)


class SessionInterface(object):
    session_class = Session
    __session_map = {}

    @staticmethod
    def create_sid():
        return str(uuid4())

    def make_null_session(self, app):
        return self.session_class(self.create_sid(), permanent=app.config["session_life_time"])

    @staticmethod
    def get_sid(app, request):
        return request.cookies.get(app.config['SESSION_NAME'])

    @staticmethod
    def is_http_only(app):
        return app.config.get('SESSION_HTTP_ONLY')

    @property
    def session_map(self):
        return self.__session_map

    def open_session(self, app, request):
        sid = request.cookies.get(app.config['SESSION_NAME'])
        if sid is not None:
            sid = byte_to_str(base64.b64decode(sid))
        if sid is None or sid not in self.session_map.keys():
            sid = self.create_sid()
            s = self.session_class(sid, permanent=app.config["session_life_time"])
            self.session_map[sid] = s
            return s
        else:
            return self.session_map[sid]

    def save_session(self, response, app, sess=session):
        sid = str_to_byte(sess.sid)
        sid = base64.b64encode(sid)
        max_age = session.get('permanent') or timedelta(days=31).total_seconds()
        response.set_cookie(app.config['SESSION_NAME'], sid, max_age=max_age,
                            httponly=self.is_http_only(app))
        return response


def str_to_byte(uu):
    return uu.encode('utf-8')


def byte_to_str(by):
    return by.decode('utf-8')
