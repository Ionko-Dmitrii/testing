from apps.common.services import ParseAnswerAndQuestionsPage
from core.celery import app


@app.task
def save_questions():
    ParseAnswerAndQuestionsPage.save_questions_in_database()
    print('run task>>>>>>>>>>>>>>>>>>>>>')
