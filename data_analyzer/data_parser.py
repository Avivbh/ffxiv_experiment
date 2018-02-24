import csv
from collections import defaultdict
import numpy as np

from game import Game
from player import Player


class DataParser(object):
    def __init__(self, input_path, number_of_rounds):
        self._input_path = input_path
        self._number_of_rounds = number_of_rounds
        self._endowment = 10000

        # {player_id: player_object}
        self._players = {}

        # {round_id: {game_id: game_object}}
        self._rounds = defaultdict(lambda: {})

        # {player: payoff}
        self._payoffs = {}

        # {round_id: [offers]}
        self._offers_per_round = {}
        self._offers = []

        # {round_id: {feature: value}
        self._offers_features = {}

        self._reject_values = []
        self._reject_features = {}

    def parse_file(self):
        with open(self._input_path, 'r') as data_file:
            reader = csv.DictReader(data_file)
            for row in reader:
                player = Player(row['participant.label'])
                self._players[row['participant.label']] = player

                for round_number in range(1, self._number_of_rounds + 1):
                    game_id = row['ultimatum_game.{0}.group.id_in_subsession'.format(round_number)]

                    # check if the game was already created:
                    game = None
                    for saved_game_id, saved_game in self._rounds[round_number].items():
                        if saved_game_id == game_id:
                            game = saved_game
                            break

                    if game is None:
                        game = Game()
                        game.game_id_in_round = game_id

                        accepted_by_timeout = row['ultimatum_game.{0}.group.accepted_by_timeout'.format(round_number)]
                        game.accepted_by_timeout = True if accepted_by_timeout == '1' else False
                        offered_by_timeout = row['ultimatum_game.{0}.group.offered_by_timeout'.format(round_number)]
                        game.offered_by_timeout = True if offered_by_timeout == '1' else False
                        accepted = row['ultimatum_game.{0}.group.offer_accepted'.format(round_number)]
                        game.accepted = True if accepted == '1' else False
                        game.kept = int(row['ultimatum_game.{0}.group.kept'.format(round_number)])
                        game.round_number = round_number

                    if row['ultimatum_game.{0}.player.id_in_group'.format(round_number)] == '1':
                        game.proposer = player
                    else:
                        game.responder = player

                    self._rounds[round_number][game_id] = game
                    player.add_game(round_number, game)

    def calculate_stats(self):
        self._calculate_payoffs()
        self._calculate_offers()
        self._calculate_rejects()

    def _calculate_payoffs(self):
        for player_name, player in self._players.items():
            player_profit = 0
            for round_number, game in player.games.items():
                if not game.accepted:
                    continue
                if game.proposer.player_name == player_name:
                    player_profit += game.kept
                else:
                    player_profit += self._endowment - game.kept

            self._payoffs[player_name] = player_profit

    def _calculate_offers(self):

        # Gather data of offers per round
        for round_id, round in self._rounds.items():
            for game in round.values():
                if not game.offered_by_timeout:
                    self._offers_per_round.setdefault(round_id, []).append(self._endowment - game.kept)
                    self._offers.append(self._endowment - game.kept)

        # Calculate features for each round
        for round_id, rounds_offers in self._offers_per_round.items():
            self._offers_features[round_id] = {}
            self._offers_features[round_id]['mean'] = np.mean(rounds_offers)
            self._offers_features[round_id]['median'] = np.median(rounds_offers)
            self._offers_features[round_id]['standard_deviation'] = np.std(rounds_offers)

        # Calculate features for the entire experiment
        self._offers_features['mean'] = np.mean(self._offers)
        self._offers_features['median'] = np.median(self._offers)
        self._offers_features['standard_deviation'] = np.std(self._offers)

    def _calculate_rejects(self):

        number_of_valid_games = 0
        for round in self._rounds.values():
            for game in round.values():
                if not game.accepted:
                    self._reject_values.append(self._endowment - game.kept)
                if not game.accepted_by_timeout:
                    number_of_valid_games += 1
        self._reject_features['percentage'] = float(len(self._reject_values)) / number_of_valid_games
        self._reject_features['mean'] = np.mean(self._reject_values)
        self._reject_features['median'] = np.median(self._reject_values)
        self._reject_features['standard_deviation'] = np.std(self._offers)

    def print_results(self):

        # Print offers data
        print('---------------- Offers data ----------------\n')
        features = ['mean', 'median', 'standard_deviation']
        data = []
        for round_number in range(1, self._number_of_rounds + 1):
            data.append([self._offers_features[round_number]['mean'],
                         self._offers_features[round_number]['median'],
                         self._offers_features[round_number]['standard_deviation']])

        row_format = '{:>20}' * (len(features) + 1)
        print(row_format.format('round', *features))
        round_number = 1
        for row in data:
            print(row_format.format(round_number, *row))
            round_number += 1
        print(row_format.format('total',
                                self._offers_features['mean'],
                                self._offers_features['median'],
                                self._offers_features['standard_deviation']))

        print('\n\n')
        print('---------------- Reject data ----------------\n')
        print(row_format.format('mean', 'median', 'standard_deviation', 'percentage'))
        print(row_format.format(self._reject_features['mean'],
                                self._reject_features['median'],
                                self._reject_features['standard_deviation'],
                                self._reject_features['percentage']))

        print('\n\n')
        print('---------------- Payoff data ----------------')
        print('Does not include the participation fee')
        print('The maximum available payoff was {0}\n'.format(self._number_of_rounds * self._endowment))
        row_format = '{:>20}' * (len(features))
        print(row_format.format('mean', 'median', 'standard_deviation'))
        payoffs = list(self._payoffs.values())
        print(row_format.format(np.mean(payoffs),
                                np.median(payoffs),
                                np.std(payoffs)))


if __name__ == '__main__':
    parser = DataParser('real_data.csv', 20)
    parser.parse_file()
    parser.calculate_stats()
    parser.print_results()

