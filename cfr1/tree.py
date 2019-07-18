# -*- coding: utf-8 -*-
# author: shougang.deng@shopee.com
import random
import time

from cfr1.strategy import PotAction, cal_total_pot

rand = random.Random()
rand.seed(int(time.time()))

tree = {
	'hands': {
		'preflop': {
			'player_num': {
				('player', 'action'): {}
			},

		}
	}
}


class ActionNode(object):
	def __init__(self, players: dict, my_index: int, player_action):
		self.players = players
		self.index = my_index
		self.player_action = player_action
		self.strategy = [1. / 13 for i in range(13)]
		self.children = {}

	def add_child(self, child):
		self.children[child.players] = child

	def choose_action(self, round_state):
		r = rand.random()
		last_choice = 0
		tp = 0
		for p in self.strategy:
			if r < tp:
				tp += p
				last_choice += 1
		return PotAction[last_choice] * cal_total_pot(round_state)


class ActionTree(object):

	def __init__(self, hands: list):
		self.hands = hands
