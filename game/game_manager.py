#!/usr/bin/env python3
# -*- coding=utf-8 -*-
import sys

from game.round_game import RoundGame
from model.deck import Deck
from model.player import Player

sys.path.append("..")


class GameManager():

	def __init__(self):
		self.deck = Deck()
		self.deck.shuffle()
		self.roundGame = RoundGame()
		self.players = []
		self.livingPlayers = []
		self.buttonIndex = 0

	def testRoundGame(self, player_num: int = 3) -> None:
		self.players = []
		for i in range(0, player_num):
			p = Player()
			p.name = str(i)
			p.currentMoney = 100 + i
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
