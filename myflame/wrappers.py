from werkzeug.wrappers import Response as ResponseBase, Request as RequestBase
from werkzeug.wrappers.json import JSONMixin


class Request(RequestBase, JSONMixin):
    pass


class Response(ResponseBase, JSONMixin):
    default_mimetype = 'text/html'
