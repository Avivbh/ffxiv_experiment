from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    def get_timeout_seconds(self):
        return self.session.config['instructions_page_timeout']


class Questions(Page):
    form_model = models.Group
    form_fields = ['question_1_answer', 'question_2_answer']

    def get_timeout_seconds(self):
        return self.session.config['questions_page_timeout']

    def question_1_answer_error_message(self, question_1_answer):
        if question_1_answer != 1:
            return "Wrong answer, Please try again"

    def question_2_answer_error_message(self, question_2_answer):
        if question_2_answer != 2:
            return "Wrong answer, please try again"


page_sequence = [
    Introduction,
    Questions
]
