from werkzeug.test import run_wsgi_app
from werkzeug.test import create_environ


def run_test_client(app, environ=None):
    environ = environ or create_test_environ()
    run_wsgi_app(app, environ=environ)


def create_test_environ(*args, **kwargs):
    create_environ(*args, **kwargs)


if __name__ == '__main__':
    from myflame.app import Application

    my_app = Application()
    client = my_app.test_client()
