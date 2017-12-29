from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    pass


class Offer(Page):
    form_model = models.Group
    form_fields = ['kept']

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        return {
            'round_number': self.round_number
        }


class OfferWaitPage(WaitPage):
    def vars_for_template(self):
        if self.player.id_in_group == 2:
            body_text = "You are the responder. Waiting for proposer to give offer."
        else:
            body_text = 'Please wait'
        return {
            'body_text': body_text,
            'round_number': self.round_number
        }


class Respond(Page):
    form_model = models.Group
    form_fields = ['offer_accepted']

    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        return {
            'responder_gil': Constants.endowment - self.group.kept,
            'proposer_gil': self.group.kept,
            'round_number': self.round_number
        }


class ResponseWaitPage(WaitPage):
    def vars_for_template(self):
        body_text = "Please wait while the the other player decide whether to accept your offer"
        return {'body_text': body_text}

    def is_displayed(self):
        return self.player.id_in_group == 1


class Results(Page):
    def before_next_page(self):
        self.group.set_payoffs()

    def offer(self):
        return Constants.endowment - self.group.kept

    def vars_for_template(self):
        return {
            'offer': Constants.endowment - self.group.kept,
            'accepted': self.group.offer_accepted,
            'round_number': self.round_number
        }


page_sequence = [
    # Introduction,
    Offer,
    OfferWaitPage,
    Respond,
    ResponseWaitPage,
    Results
]
