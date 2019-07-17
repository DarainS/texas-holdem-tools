# -*- coding: utf-8 -*-
# author: shougang.deng@shopee.com
from enum import Enum

from game.round_game import RoundGame


class PlayerAction(Enum):
	Check = 1
	Bet = 2
	Raise = 3
	AllIn = 4
	Fold = 9


class Player(object):

	def __init__(self, name: str):
		self.hands = []
		self.handsValue = 0
		self.winRate = 0
		self.currentMoney = 0
		self.name = name
		self.is_human = False

	def __str__(self):
		return self.name + " " + str(self.hands[0]) + str(self.hands[1]) + " money:" + str(self.currentMoney)

	def __repr__(self):
		return self.name + " " + str(self.hands[0]) + str(self.hands[1]) + " money:" + str(self.currentMoney)

	def sortHands(self):
		self.hands.sort(key=lambda card: card.num, reverse=True)

	def simpleHandsString(self):
		assert len(self.hands) == 2
		self.sortHands()
		suit = 'o'
		if self.hands[0].tag == self.hands[1].tag:
			suit = 's'
		if self.hands[0].num == self.hands[1].num:
			suit = ''
		return self.hands[0].symbol + self.hands[1].symbol + suit

	def handsString(self):
		assert len(self.hands) == 2
		self.sortHands()
		return str(self.hands[0]) + str(self.hands[1])

	def ask_action(self, game: RoundGame):
		return

	def action(self, game: RoundGame):
		if self.is_human:
			return self.ask_action(game)
		else:

