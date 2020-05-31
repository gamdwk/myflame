from werkzeug.exceptions import MethodNotAllowed


class View(object):
    def __int__(self):
        self.route = {
            "GET": self.GET,
            "POST": self.POST,
            "PUT": self.PUT,
            "DELETE": self.DELETE
        }

    def GET(self):
        raise MethodNotAllowed

    POST = PUT = DELETE = GET

