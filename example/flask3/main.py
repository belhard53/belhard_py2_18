#pip install flask-sqlalchemy

from flask import Flask, redirect, render_template, request, session, url_for, jsonify
import os
from models import db, Quiz, Question, db_add_new_data, User
from random import shuffle
import sys

BASE_DIR = os.path.dirname(__file__)
DB_DIR = os.path.join(BASE_DIR, 'db')

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

DB_PATH = os.path.join(DB_DIR, 'db_quiz.db')

app = Flask(__name__, 
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SECRET_KEY'] = 'secretkeysecretkeysecretkey1212121'

db.init_app(app)

html_config = {
    'admin':True,
    'debug':False
}

with app.app_context():
    db_add_new_data()
    
    # quizes = Quiz.query.one() 
    # quizes = Quiz.query.all()     
    # print(quizes)
    # quiz = quizes[0]
    # q = quiz.question # все вопросы - список
    # print(111, q)
    # print(222, q[0], q[0].quiz) # посмотреть в какие квизы входит 1ый вопрос
    
    # for q in quizes[1].question:
    #     print(q)
        
    # print(quizes[1], quizes[1].user.name)


@app.route('/', methods = ['GET'])
def index():
    return render_template('base.html', html_config = html_config)

@app.route('/quiz/', methods = ['POST', 'GET'])
def view_quiz():
    if request.method == 'GET':
        session['quiz_id'] = -1
        quizes = Quiz.query.all()
        print(quizes)
        return render_template('start.html', quizes=quizes, html_config = html_config)
    session['quiz_id'] = request.form.get('quiz')
    session['question_n'] = 0
    session['question_id'] = 0
    session['right_answers'] = 0
    return redirect(url_for('view_question'))


@app.route('/question/', methods = ['POST', 'GET'])
def view_question():
    
    if not session['quiz_id'] or session['quiz_id'] == -1:
        return redirect(url_for('view_quiz'))

    # если пост значит ответ на вопрос        
    if request.method == 'POST':        
        question = Question.query.filter_by(id=session['question_id']).all()[0]        
        # если ответ ы сходятся значит +1
        if question.answer == request.form.get('ans_text'):
            session['right_answers'] += 1
        # следующий вопрос
        session['question_n'] += 1


    quiz = Quiz.query.filter_by(id = session['quiz_id']).all()
    if int(session['question_n']) >= len(quiz[0].question):
        session['quiz_id'] = -1 # чтобы больше не работала страница question
        return redirect(url_for('view_result'))
    
    else:
        question = quiz[0].question[session['question_n']]
        session['question_id'] = question.id
        answers = [question.answer, question.wrong1, question.wrong2, question.wrong3 ]
        shuffle(answers)

        return render_template('question.html', 
                               answers=answers, 
                               question=question, 
                               html_config = html_config)



@app.route('/result/')
def view_result():
    return render_template('result.html', 
                    right=session['right_answers'], 
                    total = session['question_n'],
                    html_config = html_config)

@app.route('/quizes_view/', methods = ['POST', 'GET'])
def view_quiz_edit():
    if request.method == 'POST':
        quiz = request.form.get('quiz')
        if quiz and len(quiz) > 3:
            user = db.session.query(User).get(1)
            quiz = Quiz(quiz, user)
            db.session.add(quiz)
            db.session.commit()
        else:
            question = request.form.get('question')
            answer = request.form.get('answer')
            wrong1 = request.form.get('wrong1')
            wrong2 = request.form.get('wrong2')
            wrong3 = request.form.get('wrong3')
            if all([question, answer, wrong1, wrong2, wrong3]):
                q = Question(question, answer, wrong1, wrong2, wrong3)
                db.session.add(q)
                db.session.commit()
        

        
        return redirect(url_for('view_quiz_edit', qqq='123'))
    
    # если GET
    quizes = Quiz.query.all()    
    questions = Question.query.all()
    return render_template('quizes_view.html', 
                           html_config = html_config,
                           quizes = quizes,
                           questions = questions,
                           len = len)





@app.errorhandler(404)
def page_not_found(e):
    #snip
    return '<h1 style="color:red; text-align:center"> Упс..... </h1>'





# ---------------- API 
@app.route('/api/quizes/', methods = ['GET'])
def api_get():
    quizes = Quiz.query.all()
    json = [{'name':q.name, 'id':q.id, 'user_id':q.user_id}  for q in quizes]    
    return jsonify(json)



@app.route('/api/quizes/', methods = ['POST'])
def api_post():
    quiz = Quiz('Quiz123', db.session.query(User).get(1))
    db.session.add(quiz)
    db.session.commit()
    return jsonify({"id":quiz.id})


    
@app.route('/api/quizes/<int:id>/', methods = ['GET'])
def api_get_id(id):    
    quiz = db.session.query(Quiz).get(id)    
    return jsonify(dict(name=quiz.name, user_ud=quiz.user_id))
    





app.run(debug=True, host='0.0.0.0', port=5555)