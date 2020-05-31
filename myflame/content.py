from .gobal import _request_ctx_content, _app_ctx_content, has_app_ctx


class RequestContent(object):
    def __init__(self, app, environ, request_class=None, session=None):
        self.app = app
        self.request_class = request_class or self.app.request_class
        self.request = self.request_class(environ)
        self.session = session or self.app.session_interface.open_session(self.app, self.request)
        self.url_adapter = self.app.url_map.bind_to_environ(environ)

    def push(self):
        top = _app_ctx_content.top
        if top is None or top != self.app:
            self.app.application_content(self.app).push()
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
