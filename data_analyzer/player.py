class Player(object):
    def __init__(self, player_name):
        self._player_name = player_name

        # {round_number: game_object}
        self._games = {}

    @property
    def games(self):
        return self._games

    @property
    def player_name(self):
        return self._player_name

    def add_game(self, round_number, game):
        if round_number in self._games:
            raise RuntimeError('Game already added for this round number')
        self._games[round_number] = game
