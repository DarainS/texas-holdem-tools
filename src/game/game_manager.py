#!/usr/bin/env python3
# -*- coding=utf-8 -*-
import sys

from decimal import Decimal

from game.round_game import RoundGame
from model.deck import Deck
from model.player.player import Player

sys.path.append("..")


class GameManager(object):

    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.round_game = RoundGame()
        self.players = []
        self.living_players = []
        self.button_index = 0

    def testRoundGame(self, player_num=3):
        players = []
        for i in range(0, player_num):
            p = Player()
            p.name = str(i)
            p.current_money = Decimal('100') + i
            players.append(p)
        game = RoundGame()
        game.sb = Decimal('1')
        game.bb = Decimal('2')
        game.players = players
        game.gameBegin()

        game.goPreFlop()
        if not game.isShowDownTime():
            game.goFlop()
        game.goTurn()
        game.goRiver()
        game.makeResult()

    def nextRoundGame(self):
        self.round_game = RoundGame()
        self.round_game.dealPlayersHands()
        self.round_game.askBehaviours()


def test1():
    game = GameManager()
    game.testRoundGame()


def main():
    test1()


if __name__ == '__main__':
    main()
