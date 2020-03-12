from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys, personality_quiz, satisfaction_survey
app = Flask(__name__)

app.config['SECRET_KEY'] = 'agooddaytodie@tacobell'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
RESPONSES_KEY = "responses"
CURRENT_SURVEY = "curr_survey"

responses = []

@app.route('/')
def show_choose_survey_form():
    """Show list of surveys"""
    session[RESPONSES_KEY] = []
    return render_template('index.html',
    surveys=surveys.values())

@app.route('/', methods=["POST"])
def choose_survey():
    """Select a Survey"""
    survey_title = request.form['survey_title']

    survey = surveys[survey_title]
    session[CURRENT_SURVEY] = survey_title

    return render_template('start-survey.html', survey=survey)

@app.route('/begin', methods=["POST"])
def begin():
    """my understanding is that you want to eat the initial POST REQ so show_questions 
    only recieves redirect GET requests from /answer, this feels bad, unless i do an initialization here"""
    return redirect('/questions/0')


@app.route('/questions/<int:que_num>')
def show_question(que_num):
    """Show question and show answers if needed"""
    responses = session.get(RESPONSES_KEY)
    survey_title = session[CURRENT_SURVEY]
    survey = surveys[survey_title]

    choices = survey.questions[que_num].choices
    question = survey.questions[que_num]

    if (responses is None):
        return redirect("/")
    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("thankyou.html")
    if que_num != len(responses):
        flash("You are trying to access questions out of order. Heres the next question")
        return redirect(f'/questions/{len(responses)}')

    return render_template('question.html',
    question=question,
    que_num=que_num,
    choices=choices)

@app.route('/answer', methods=["POST"])
def answer():
    """Add answer to responses and push back to question, add 1 to que_num"""
    responses = session[RESPONSES_KEY]
    survey_title = session[CURRENT_SURVEY]
    survey = surveys[survey_title]
    responses.append(request.form['answer'])
    session[RESPONSES_KEY] = responses

    que_num = request.form['que_num']
    que_num = int(que_num)+1
    
    if (len(responses) == len(survey.questions)):
        return render_template('thankyou.html')
    else: 
        return redirect(f'/questions/{str(que_num)}')

# ***********************************OTHER CODE FOR LEARNING SESSIONS STUFF ******************************************

@app.route('/party')
def show_invite():
    if session.get("entered-pin", False):
        return render_template('secret.html')
    else:
        return redirect('/login-form')

@app.route('/login-form')
def log_in_form():
    return render_template('log-in.html')

@app.route('/login')
def login():
    SECRET = 'ilikedogs'
    code = request.args['secret_code']
    if code == SECRET:
        session["entered-pin"] = True
        return redirect("/party")
    else:
        return redirect("/login-form")