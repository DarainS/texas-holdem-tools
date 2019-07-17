#!/usr/bin/env python3
# -*- coding=utf-8 -*-
import sys

from game.player import Player
from game.round_game import RoundGame
from model.deck import Deck

sys.path.append("..")


class GameManager(object):

	def __init__(self):
		self.deck = Deck()
		self.deck.shuffle()
		self.roundGame = RoundGame()
		self.players = []
		self.livingPlayers = []
		self.buttonIndex = 0

	def testRoundGame(self, player_num: int = 6) -> None:
		self.players = []
		for i in range(0, player_num):
			p = Player('player ' + str(i))
			p.name = str(i)
			p.currentMoney = 200
			if i == 0:
				p.is_human = True
			self.players.append(p)
		game = RoundGame()
		game.sb = 1
		game.bb = 2
		game.players = self.players
		game.begin()

	def nextRoundGame(self):
		self.roundGame = RoundGame()
		self.roundGame.dealPlayersHands()
		self.roundGame.askBehaviours()


def test1():
	game = GameManager()
	game.testRoundGame()


def main():
	test1()


if __name__ == '__main__':
	main()
