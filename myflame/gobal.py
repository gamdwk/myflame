from werkzeug.local import LocalProxy, LocalStack
from functools import partial

request_error_msg = "no request content"
app_ctx_error_msg = "no application content"


def get_request_obj(name):
    top = _request_ctx_content.top
    if top is None:
        raise RuntimeError(request_error_msg)
    if name is 'session':
        if current_app.config["SECRET_KEY"] is None:
            raise RuntimeError("No SECRET_KEY in current_app's config")

    return getattr(top, name)


def get_app_ctx_obj(name):
    top = _app_ctx_content.top
    if top is None:
        raise RuntimeError(app_ctx_error_msg)
    return getattr(top, name)


def get_current_app():
    top = _app_ctx_content.top
    if top is None:
        raise RuntimeError(app_ctx_error_msg)
    return top.app


def has_app_ctx():
    return _app_ctx_content.top is not None


def has_request_ctx():
    return _request_ctx_content.top is not None


_request_ctx_content = LocalStack()
_app_ctx_content = LocalStack()
request = LocalProxy(partial(get_request_obj, 'request'))
session = LocalProxy(partial(get_request_obj, 'session'))
g = LocalProxy(partial(get_app_ctx_obj, 'g'))
current_app = LocalProxy(get_current_app)
