from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    pass


class Questions(Page):
    form_model = models.Group
    form_fields = ['question_1_answer', 'question_2_answer']

    def question_1_answer_error_message(self, question_1_answer):
        if question_1_answer != 1:
            return "Wrong answer, Please try again"

    def question_2_answer_error_message(self, question_2_answer):
        if question_2_answer != 2:
            return "Wrong answer, please try again"


class Results(Page):
    def before_next_page(self):
        self.group.set_payoffs()

    def offer(self):
        return Constants.endowment - self.group.kept

    def vars_for_template(self):
        return {
            'offer': Constants.endowment - self.group.kept,
            'accepted': self.group.offer_accepted
        }


page_sequence = [
    Introduction,
    Questions
]
