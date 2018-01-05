from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    pass


class Offer(Page):
    """
    If the user timeout on this page he will automatically offer 5000
    """
    form_model = models.Group
    form_fields = ['kept']

    timeout_submission = {'kept': 5000}

    def get_timeout_seconds(self):
        return self.session.config['offer_and_respond_pages_times']

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        return {
            'round_number': self.round_number
        }

    def before_next_page(self):
        """
        In case of timeout: Set default values and mark if it was by timeout
        """
        if self.timeout_happened:
            for field_name, value in self.timeout_submission.items():
                setattr(self.player, field_name, value)
            self.group.offered_by_timeout = True
        else:
            self.group.offered_by_timeout = False


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
    """
    If the user timeout on this page he will automatically accept.
    """
    form_model = models.Group
    form_fields = ['offer_accepted']

    timeout_submission = {'offer_accepted': True}

    def get_timeout_seconds(self):
        return self.session.config['offer_and_respond_pages_times']

    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        return {
            'responder_gil': Constants.endowment - self.group.kept,
            'proposer_gil': self.group.kept,
            'round_number': self.round_number
        }

    def before_next_page(self):
        """
        In case of timeout: Set default values and mark if it was by timeout
        """
        if self.timeout_happened:
            for field_name, value in self.timeout_submission.items():
                setattr(self.player, field_name, value)

            self.group.accepted_by_timeout = True
        else:
            self.group.accepted_by_timeout = False


class ResponseWaitPage(WaitPage):
    def vars_for_template(self):
        body_text = "Please wait while the other player decides whether to accept your offer"
        return {'body_text': body_text}

    def is_displayed(self):
        return self.player.id_in_group == 1


class Results(Page):
    def get_timeout_seconds(self):
        return self.session.config['results_page_timeout']

    def before_next_page(self):
        self.group.set_payoffs()

    def offer(self):
        return Constants.endowment - self.group.kept

    def vars_for_template(self):
        return {
            'offer': Constants.endowment - self.group.kept,
            'accepted': self.group.offer_accepted,
            'round_number': self.round_number,
            'accepted_by_timeout': self.group.accepted_by_timeout,
        }


page_sequence = [
    # Introduction,
    Offer,
    OfferWaitPage,
    Respond,
    ResponseWaitPage,
    Results
]
