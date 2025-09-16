from flask import Flask, render_template
import os

# BASE_DIR = os.getcwd()
BASE_DIR = os.path.dirname(__name__) # так работает если проект открыт из любого места

app = Flask(__name__)

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


users=['user1', 'user22', 'user333', 'suer4', 'user55', 'user6666']


@app.route("/")
def index():
    return render_template('1.html', admin=True, q=22222222)

   
@app.route("/test/<int:num>/")
def test(num):    
    # return 'test ' * num
    return render_template('test.html', num=num)

@app.route("/users/")
def users_():
    return render_template('users.html', users=users, len=len)

@app.route("/message/<login>/<mes>/")
def message(login, mes):
    return render_template("mes.html", user=login, mes=mes)


# Сработает если ошибка 404 - т.е. любой другой путь который выше не предусмотрен
@app.errorhandler(404)
def page_not_found(error):
    return '<h1 style="color:red">такой страницы не существует</h1>'


app.run(debug=True)