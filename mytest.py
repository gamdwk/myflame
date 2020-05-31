from myflame import Application, request, current_app, make_response, \
    url_for, redirect, rend_template, send_form_dictionary, g, session
from config import Config

app = Application()
app.config.from_object(Config)


@app.route('/index')
def index():
    return rend_template('index.html')


@app.route('/register')
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        global_dict = app.global_dict
        if username in global_dict:
            return '用户已存在'
        global_dict[username] = password
        return "注册成功"
    return redirect(url_for('login'))


@app.route('/login')
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        global_dict = app.global_dict
        if username in global_dict:
            if global_dict[username] == password:
                session['name'] = username
                return redirect('index')
            return '密码错误'
        return '用户不存在'
    return rend_template('login.html')


app.run(debug=True)
