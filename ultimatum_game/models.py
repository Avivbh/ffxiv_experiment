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
    name_in_url = 'ffxiv experiment'
    players_per_group = 2
    num_rounds = 2

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

        # TODO change the way this is assigned
        if self.id_in_group == 1:
            return 'proposer'
        if self.id_in_group == 2:
            return 'responder'
