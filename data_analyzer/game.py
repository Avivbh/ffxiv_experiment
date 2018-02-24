class Game(object):
    def __init__(self):
        self._round_number = None
        self._game_id_in_round = None
        self._proposer = None
        self._responder = None
        self._offered_by_timeout = None
        self._accepted_by_timeout = None
        self._kept = None
        self._accepted = None

    @property
    def round_number(self):
        return self._round_number

    @round_number.setter
    def round_number(self, value):
        if self._round_number is not None:
            raise RuntimeError('round_number already set')
        self._round_number = value

    @property
    def game_id_in_round(self):
        return self._game_id_in_round

    @game_id_in_round.setter
    def game_id_in_round(self, value):
        if self._game_id_in_round is not None:
            raise RuntimeError('game_id_in_round number already set')
        self._game_id_in_round = value

    @property
    def proposer(self):
        return self._proposer

    @proposer.setter
    def proposer(self, value):
        if self._proposer is not None:
            raise RuntimeError('proposer already set')
        self._proposer = value

    @property
    def responder(self):
        return self._responder

    @responder.setter
    def responder(self, value):
        if self._responder is not None:
            raise RuntimeError('responder number already set')
        self._responder = value

    @property
    def offered_by_timeout(self):
        return self._offered_by_timeout

    @offered_by_timeout.setter
    def offered_by_timeout(self, value):
        if self._offered_by_timeout is not None:
            raise RuntimeError('offered_by_timeout number already set')
        self._offered_by_timeout = value

    @property
    def accepted_by_timeout(self):
        return self._accepted_by_timeout

    @accepted_by_timeout.setter
    def accepted_by_timeout(self, value):
        if self._accepted_by_timeout is not None:
            raise RuntimeError('accepted_by_timeout number already set')
        self._accepted_by_timeout = value

    @property
    def kept(self):
        return self._kept

    @kept.setter
    def kept(self, value):
        if self._kept is not None:
            raise RuntimeError('kept number already set')
        self._kept = value

    @property
    def accepted(self):
        return self._accepted

    @accepted.setter
    def accepted(self, value):
        if self._accepted is not None:
            raise RuntimeError('accepted number already set')
        self._accepted = value
