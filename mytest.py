from myflame import Application, request, current_app, make_response, \
    url_for, redirect, rend_template, send_form_dictionary
from config import Config

app = Application()
app.config.from_object(Config)


@app.route('/')
def index():
    return rend_template('index.html', name='管理员')


@app.route('/index/<int:b>')
def index1(b):
    response = make_response(b)
    return response


@app.route('/inb')
def inb():
    url_for('ina', {"b": '2'})
    return "828"


@app.route('/file')
def get_file():
    return send_form_dictionary('template', 'index.html')


app.run(debug=True)
