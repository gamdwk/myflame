from .gobal import _request_ctx_content, _app_ctx_content, has_app_ctx
from .session import SessionInterface


class RequestContent(object):
    def __init__(self, app, environ, request_class=None, session=None):
        self.app = app
        self.request_class = request_class or self.app.request_class
        self.request = self.request_class(environ)
        self.session = session
        self.url_adapter = self.app.url_map.bind_to_environ(environ)

    def push(self):
        top = _app_ctx_content.top
        if top is None or top != self.app:
            self.app.application_content(self.app).push()
        self.session = SessionInterface().open_session()
        if self.session is None:
            self.session = SessionInterface().make_null_session()
        _request_ctx_content.push(self)

    def pop(self):
        _request_ctx_content.pop()
        if _app_ctx_content.top is not None:
            self.app.application_content.pop()


class ApplicationContent(object):
    def __init__(self, app):
        self.app = app
        self.g = dict()

    def push(self):
        _app_ctx_content.push(self)

    @staticmethod
    def pop():
        _app_ctx_content.pop()


class Session(object):
    def open_session(self):
        pass

    def save_session(self):
        pass
