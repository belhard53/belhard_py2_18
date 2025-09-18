from flask import Flask, render_template, redirect, request, url_for, session
import os

# BASE_DIR = os.getcwd()
BASE_DIR = os.path.dirname(__name__) # так работает если проект открыт из любого места

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my secret key 12334 dslkfj dlskjf lsdkjf sdlkjflsdkjf'

# app = Flask(__name__,
#             static_folder=os.path.join(BASE_DIR, 'static'),
#             template_folder=os.path.join(BASE_DIR, 'templates'))


# модель MVC
    # model - модель данных из базы данных(будет позже)
    # view
    # controller
    
# @app.route("/")
# def index():
#     return "<h1>Hello Python 1234</h1>"

r_num = 0

users=['user1', 'user22', 'user333', 'suer4', 'user55', 'user6666']

# session['num'] = 0 #  так нельзя

@app.route("/")
def index():
    
    return render_template('index.html', admin=True, q=22222222)


@app.route("/count/")
def count():
    # global r_num
    if not 'num' in session:
        session['num'] = 0
        
    
    session['num'] += 1
    return render_template('count.html', num=session['num'])

   
@app.route("/test/<int:num>/")
def test(num):    
    # return 'test ' * num
    return render_template('test.html', num=num)

@app.route("/users/")
def users_():
    return render_template('users.html', users=users, len=len)


@app.route("/form1/", methods=['GET', 'POST'])
def form1():
    err = ''
    login = ''
    if request.method == 'POST':
        # query = request.args.get('q', '')  # args из get
        login = request.form.get('login')
        if login == 'qqq':
            return redirect(url_for('index'))
        else:
            err='Пароль err'
    #     return render_template('form1.html', err='Пароль err')
    # else:
    return render_template('form1.html', err=err, login=login)

@app.route("/message/<login>/<mes>/")
def message(login, mes):
    return render_template("mes.html", user=login, mes=mes)


# Сработает если ошибка 404 - т.е. любой другой путь который выше не предусмотрен
@app.errorhandler(404)
def page_not_found(error):
    return '<h1 style="color:red">такой страницы не существует</h1>'





app.run(debug=True)