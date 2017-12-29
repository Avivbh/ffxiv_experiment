from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """
One player decides how to divide a certain amount between himself and the other
player.

See: Kahneman, Daniel, Jack L. Knetsch, and Richard H. Thaler. "Fairness
and the assumptions of economics." Journal of business (1986):
S285-S300.

"""


class Constants(BaseConstants):
    name_in_url = 'ffxiv experiment intro'
    players_per_group = None
    num_rounds = 1

    instructions_template = 'ultimatum_game_intro/Instructions.html'
    endowment = c(10000)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    question_1_answer = models.IntegerField(
        choices=[
            [1, 'The proposer will get 3000 gil and the responder will get 7000 gil'],
            [2, 'The proposer will get 7000 gil and the responder will get 3000'],
            [3, 'None of the above'],
        ])

    question_2_answer = models.IntegerField(
        choices=[
            [1, 'The proposer will get 3000 gil and the responder will get 7000 gil'],
            [2, 'Both players gets 0 gil'],
            [3, 'None of the above'],
        ])


class Player(BasePlayer):
    pass
