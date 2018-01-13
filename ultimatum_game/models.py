from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


doc = """
One player (the proposer) decides how to divide a certain amount between himself and the other
player. The other player (the responder) decides whether to accept or reject the offer.
Accept: amount is divided according to the offer.
Reject: No one gets anything.

"""


class Constants(BaseConstants):
    name_in_url = 'ffxiv experiment'
    players_per_group = 2
    num_rounds = 4

    instructions_template = 'ultimatum_game/Instructions.html'

    # Initial amount allocated to the dictator
    endowment = c(10000)


class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()


class Group(BaseGroup):
    kept = models.CurrencyField(
        doc="""Amount proposer decided to keep for himself""",
        min=0, max=Constants.endowment,
    )
    offer_accepted = models.BooleanField()
    accepted_by_timeout = models.BooleanField()
    offered_by_timeout = models.BooleanField()

    def set_payoffs(self):
        proposer = self.get_player_by_role('proposer')
        responder = self.get_player_by_role('responder')

        if self.offer_accepted:
            proposer.payoff = self.kept
            responder.payoff = Constants.endowment - self.kept
        else:
            proposer.payoff = 0
            responder.payoff = 0


class Player(BasePlayer):

    def role(self):

        if self.id_in_group == 1:
            return 'proposer'
        if self.id_in_group == 2:
            return 'responder'
