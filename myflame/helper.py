from os.path import dirname, join, isfile, isabs
from os import walk
import sys
from werkzeug.wsgi import wrap_file
from .gobal import current_app, request
from werkzeug.exceptions import NotFound
from werkzeug.wsgi import get_host
from werkzeug.datastructures import Headers
from werkzeug.routing import redirect
from werkzeug.wrappers import BaseResponse
from collections import Iterable
import json

default_root_path = dirname(sys.path[0])


def find_file(filename, root_path=default_root_path):
    for root, folder, files in walk(root_path):
        if filename in files:
            return join(root, filename)


def find_folder(folder, root_path=default_root_path):
    for root, folders, files in walk(root_path):
        if folder in folders:
            return join(root, folder)


def send_file(path):
    if not isabs(path):
        path = join(default_root_path, path)
    print(path)
    if not isfile(path):
        raise NotFound
    file = open(path, 'rb')
    data = wrap_file(request.environ, file)
    return current_app.response_class(data, mimetype="application/octet-stream",
                                      direct_passthrough=True)
    # direct_passthrough=True 默认显示在页面上而非下载


def send_form_dictionary(root, filename):
    path = join(root, filename)
    return send_file(path)


def make_response(rv, **kwargs):
    if isinstance(rv, BaseResponse):
        return rv
    if not isinstance(rv, Iterable):
        rv = json.dumps(rv)
    elif isinstance(rv, dict) or isinstance(rv, list):
        rv = json.dumps(rv)
    return current_app.response_class(rv, **kwargs)
