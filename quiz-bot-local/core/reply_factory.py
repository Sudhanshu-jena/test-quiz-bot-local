
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST
from django.shortcuts import render,redirect

score = 0
def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if current_question_id is None:
        session["current_question_id"] = 0
        session["score"] = 0
        current_question = PYTHON_QUESTION_LIST[0]
        bot_responses.append(current_question)
        return bot_responses

    record_current_answer(message, current_question_id, session)
    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
        session["current_question_id"] = next_question_id
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)
        reset_quiz(session)

    session.modified = True
    return bot_responses

def get_next_question(current_question_id):
    total_questions = len(PYTHON_QUESTION_LIST)
    if current_question_id is not None and current_question_id < total_questions - 1:
        return PYTHON_QUESTION_LIST[current_question_id + 1], current_question_id + 1
    return None, None

def record_current_answer(answer, current_question_id, session):
    global score
    current_question = PYTHON_QUESTION_LIST[current_question_id]
    if answer == current_question['answer']:
        score = session.get('score', 0)
        score += 1
        session['score'] = score
    # print(score)
    session.modified = True

def generate_final_response(session):
    global score
    # print(f'final: {score}')
    # score = session.get('score', 0)
    total_questions = len(PYTHON_QUESTION_LIST)
    return f"Quiz completed! Your score is {score}/{total_questions}."

def reset_quiz(session):
    session.flush()



def quiz_page(request):
    global score
    if request.method == 'POST':
        message = request.POST.get('user_answer')
        bot_responses = generate_bot_responses(message, request.session)
    else:
        bot_responses = generate_bot_responses(None, request.session)

    current_question_id = request.session.get('current_question_id')
    if current_question_id is not None and current_question_id < len(PYTHON_QUESTION_LIST):
        current_question = PYTHON_QUESTION_LIST[current_question_id]
        return render(request, 'quiz.html', {
            'question': current_question,
            'finished': False
        })
    else:
        # score = request.session.get('score', 0)
        total_questions = len(PYTHON_QUESTION_LIST)
        return render(request, 'quiz.html', {
            'score': score,
            'total_questions': total_questions,
            'finished': True
        })

def reset_quiz_view(request):
    global score
    score = 0
    reset_quiz(request.session)
    return redirect('quiz_page')


