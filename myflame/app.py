from werkzeug import run_simple
from werkzeug.exceptions import HTTPException, default_exceptions, InternalServerError
from werkzeug.utils import cached_property
from werkzeug.routing import Map, Rule, RuleFactory
from werkzeug.wrappers import BaseResponse
from os.path import join, dirname
import sys
from .wrappers import Request, Response
from .config import Config
from .content import RequestContent, ApplicationContent
from .gobal import has_app_ctx, current_app, request
from .template import build_env
from .helper import send_form_dictionary


class Application(object):
    request_class = Request
    response_class = Response
    url_rule_class = Rule
    url_map_class = Map
    config_class = Config
    request_content = RequestContent
    application_content = ApplicationContent
    exceptions = default_exceptions
    error_handlers = {}
    view_functions = {}
    root_path = None
    template_path = None
    static_folder = None
    before_request_funcs = []
    after_request_funcs = []

    def __init__(self, template_path='template', static_folder='static', root_path=None):
        self.url_map = self.url_map_class()
        self.static_folder = static_folder
        """endpoint和函数之间的映射{
            endpoint<string>:view_func<function>
        }"""
        self.template_path = template_path
        self.config = self.config_class()
        self.root_path = root_path or sys.argv[0]
        self.config.make_config(root_path=root_path)
        self.jinja_env = build_env(template_path=self.template_path, root_path=self.root_path)
        self.add_url_rule('/static/<path:filename>', view_func=self.get_static_file,
                          endpoint='static', methods=['GET'])
        self.application_content(self).push()

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def wsgi_app(self, environ, start_response):
        ctx = self.request_content(self, environ)
        ctx.push()
        try:
            response = self.dispatch_request(environ)
            response = self.process_response(response)
            return response(environ, start_response)
        finally:
            ctx.pop()

    def dispatch_request(self, environ):
        try:
            rv = self.preprocess_response()
            if rv is not None:
                return self.response_class(rv)
            adapter = self.url_map.bind_to_environ(environ)
            rv = adapter.dispatch(lambda e, v: self.view_functions[e](**v))
            if isinstance(rv, int):
                rv = str(rv)
            if isinstance(rv, BaseResponse):
                return rv
            return self.response_class(rv)
        except Exception as ex:
            return self.handler_error(ex)

    def run(self, host=None, port=None, debug=False, **options):
        _host = 'localhost'
        _port = 5000
        cn_host = host or self.config["host"] or _host
        cn_port = port or self.config["port"] or _port
        reload = debug = bool(debug)
        options.setdefault('threaded', True)
        self.config.make_config(debug=debug, host=cn_host, port=cn_port)
        try:
            run_simple(cn_host, cn_port, self, use_debugger=debug,
                       use_reloader=reload, **options)
        except Exception as e:
            raise e

    def route(self, url_rule, endpoint=None, **kwargs):
        def decorator(f):
            self.add_url_rule(url_rule, f, endpoint, **kwargs)
            return f

        return decorator

    def add_url_rule(self, url_rule, view_func=None, endpoint=None, **kwargs):
        endpoint = endpoint or view_func.__name__
        if endpoint in self.view_functions.keys():
            raise
        rule = Rule(url_rule, endpoint=endpoint, **kwargs)
        self.url_map.add(rule)
        if view_func is not None:
            self.view_functions[endpoint] = view_func

    def handler_error(self, e):
        if e in self.error_handlers.keys():
            return self.error_handlers[e]()
        elif isinstance(e, HTTPException):
            return e
        else:
            try:
                if not self.config.debug:
                    return InternalServerError()
            finally:
                raise e

    # error_handler,when catch exception, return handel()
    def register_error_handler(self, status_or_error, handler):
        if isinstance(status_or_error, int):
            if status_or_error in self.exceptions:
                status_or_error = self.exceptions[status_or_error]
            else:
                raise KeyError("status not in exceptions")
        self.error_handlers[status_or_error] = handler

    # exceptions,when abort(status),raise error
    def register_exceptions(self, status, error):
        self.exceptions[status] = error

    def build_adapter(self, environ=None):
        environ = environ or request.environ
        return self.url_map.bind_to_environ(environ)

    @cached_property
    def static_root(self):
        return join(self.root_path, self.static_folder)

    def get_static_file(self, filename):
        return send_form_dictionary(self.static_root, filename)

    def before_request(self):
        def decorate(f):
            self.before_request_funcs.append(f)
            return f

        return decorate

    def after_request(self):
        def decorate(f):
            self.after_request_funcs.append(f)
            return f

        return decorate

    def preprocess_response(self):
        for f in self.before_request_funcs:
            rv = f()
            if rv is not None:
                return rv

    def process_response(self, response):
        for f in self.before_request_funcs:
            response = f(response)
        return response

    def add_global_template_context(self, **context):
        self.jinja_env.globals.update(**context)

    def test_client(self):
        from werkzeug.test import Client
        return Client(self, self.response_class)


