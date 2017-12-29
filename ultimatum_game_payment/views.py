from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    pass


class Payoff(Page):

    def vars_for_template(self):
        return {
            'payoff': self.participant.payoff
        }

page_sequence = [
    Payoff,
]
