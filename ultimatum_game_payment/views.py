from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    pass


class Payoff(Page):

    def vars_for_template(self):
        return {
            'rounds_payoff': self.participant.payoff,
            'total_payoff': self.participant.payoff + self.session.config['participation_fee']
        }

page_sequence = [
    Payoff,
]
