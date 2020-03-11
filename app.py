from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys, personality_quiz, satisfaction_survey
app = Flask(__name__)

app.config['SECRET_KEY'] = 'agooddaytodie@tacobell'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
RESPONSES_KEY = "responses"

responses = []

@app.route('/')
def index():
    """Show list of stories"""
    session[RESPONSES_KEY] = []
    return render_template('index.html',
    title=satisfaction_survey.title,
    instructions=satisfaction_survey.instructions,
    surveys=surveys.values())

@app.route('/questions/<int:que_num>')
def show_question(que_num):
    """Show question and show answers if needed"""
    responses = session.get(RESPONSES_KEY)

    choices = satisfaction_survey.questions[que_num].choices
    question = satisfaction_survey.questions[que_num]

    if (responses is None):
        return redirect("/")
    if (len(responses) == len(satisfaction_survey.questions)):
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
    responses.append(request.form['answer'])
    session[RESPONSES_KEY] = responses
    que_num = request.form['que_num']
    que_num = int(que_num)+1
    
    if (len(responses) == len(satisfaction_survey.questions)):
        return render_template('thankyou.html')
    else: 
        return redirect(f'/questions/{str(que_num)}')
