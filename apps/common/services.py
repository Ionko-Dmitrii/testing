import random

from bs4 import BeautifulSoup
import requests

from apps.common.models import Question, TestGroup, AnswerToQuestion


class ParseAnswerAndQuestionsPage:
    url = 'https://centrevraz.ru/dlya-rvp-vnzh'

    @classmethod
    def parse_questions_from_url(cls) -> (str, dict):
        page = requests.get(cls.url)
        soup = BeautifulSoup(page.text, "html.parser")
        allQuestions = soup.findAll('div', class_='test_t')
        title_test = soup.find('h1').text
        data_dict = {}
        for data_html in allQuestions:
            question_html = data_html.find('b')
            answer_list_html = data_html.findAll('span')
            if question_html:
                question = question_html.text.split('. ')[1]
                data_dict[question] = []
                for answer_html in answer_list_html:
                    if answer_html:
                        answer = answer_html.text
                        data_dict[question].append(answer)

        return title_test, data_dict

    @classmethod
    def save_questions_in_database(cls):
        title_test, data_questions = cls.parse_questions_from_url()
        test_obj, created = TestGroup.objects.get_or_create(title=title_test)
        for title, answers in data_questions.items():
            question, created = Question.objects.get_or_create(text=title, test=test_obj)
            if created:
                answer_list = []
                for answer in answers:
                    answer_obj = AnswerToQuestion(
                        question=question,
                        text=answer
                    )
                    answer_list.append(answer_obj)
                number = random.randrange(len(answers))
                answer_list[number].is_right = True
                AnswerToQuestion.objects.bulk_create(answer_list)
                break
