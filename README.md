# Final Fantasy XIV Behavioral Economics Experiment

This repository is a part of a project conducted in a Game Theory class in Ben Gurion University of the Negev (BGU).  
The project was meant to test the use of digital currency in behavioral economics experiments and try 
to show whether MMO can be used as a playground for such experiments.

In order to test it, an experiment was built on top of the oTree framework.  
The experiment is based on the classic Ultimatum Game, only that in this case it is played 
using the Final Fantasy XIV currency (gil) instead of real money.

## The Game
The game (app in oTree terminology) code sits under `ultimatum_game` directory.  
There is also `ultimatum_game_intro`
which include an intro to the game rules and a questionnaire.  
Finally there is `ultimatum_game_payment` app to show the game results to the participants.

## Result Analyzer
Inside `data_analyzer` directory you can find a script that analyze the CSV output from the game.  
The scripts provide basic statistical information of the results:
- Offers mean / median / standard deviation. Per experiment round.
- Rejected offers mean / median / standard deviation and the general rejects ratio.
- Payoffs mean / median / standard deviation.

# oTree

oTree is a framework based on Python and Django that lets you build:

- Multiplayer strategy games, like the prisoner's dilemma, public goods game, and auctions
- Controlled behavioral experiments in economics, psychology, and related fields
- Surveys and quizzes

## Live demo
http://demo.otree.org/

## Homepage
http://www.otree.org/

## Docs

http://otree.readthedocs.org

