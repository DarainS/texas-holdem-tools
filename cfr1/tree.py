# -*- coding: utf-8 -*-
# author: shougang.deng@shopee.com
import json
import random
import time
from enum import Enum

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


class PlayerAction(Enum):
	Check = 0
	Call = 1
	Bet_0_5 = 11
	Bet_1 = 12
	Bet_Over = 13
	Raise_0_5 = 21
	Raise_1 = 22
	Raise_Over = 23
	Fold = 2


ActionList = [action for action in PlayerAction]

file_name = 'result.json'


def build_tree_from_file():
	with open(file_name) as f:
		d = json.loads(f.read())
		tree = ActionNode()
		tree.__dict__ = d
		return tree


class ActionNode(object):
	def __init__(self, players: dict, my_index: int, player_action):
		self.players = players
		self.index = my_index
		self.player_action = player_action
		self.children = {}
		self.action_regret = {k: 0 for k in ActionList}

	def add_child(self, child):
		self.children[child.players] = child

	def choose_action(self, round_state):
		m = 0
		ac = PlayerAction.Call
		for k, v in self.action_regret:
			if v <= m:
				ac = k
		return ac


class ActionTree(object):

	def __init__(self, hands: list):
		self.hands = hands
