from jinja2 import Environment, FileSystemLoader
from os.path import join
from .helper import find_folder, make_response
from .gobal import current_app, request, session, g
from .content import _request_ctx_content


def guess_auto_escape(template_name):
    if template_name is None or '.' not in template_name:
        return False
    ext = template_name.rsplit('.', 1)[1]
    return ext in ('html', 'htm', 'xml')


def build_env(template_path='template', root_path=None):
    if root_path is None:
        template_path = find_folder(template_path)
    else:
        template_path = join(root_path, template_path)
    env = Environment(loader=FileSystemLoader(template_path),
                      autoescape=guess_auto_escape,
                      extensions=['jinja2.ext.autoescape'])
    env.globals.update(
        url_for=url_for,
        g=g,
        session=session,
        request=request,
    )
    return env
 

def rend_template(template_name, **context):
    t = current_app.jinja_env.get_template(template_name)
    return make_response(t.render(context), mimetype='text/html')


def url_for(endpoint, value=None, **kwargs):
    return _request_ctx_content.top.url_adapter.build(
        endpoint=endpoint, values=value, **kwargs)
