# -*- coding: utf-8 -*-
# author: shougang.deng@shopee.com
import json
import os
import time
from random import Random

from cfr1.tree import ActionNode, build_tree_from_dict
from cfr1.util import cal_total_pot
from pypokerengine.players import BasePokerPlayer

rand = Random()
rand.seed(int(time.time()))

ChoiceAction = [i for i in range(1, 13)]

PotAction = {
	1: 0,
	2: 0.2,
	3: 0.33,
	4: 0.45,
	5: 0.65,
	6: 0.8,
	7: 1.0,
	8: 1.4,
	9: 1.8,
	10: 2.4,
	11: 3,
	12: 5
}


class FishPlayer(BasePokerPlayer):  # Do not forget to make parent class as "BasePokerPlayer"

	def __init__(self, name):
		BasePokerPlayer.__init__(self)
		self.name = name
		self.strategy_tree: ActionNode = None
		self.hands = ''
		self.player_num = 0
		self.index = 0

	#  we define the logic to make an action through this method. (so this method would be the core of your AI)
	def declare_action(self, valid_actions, hole_card, round_state):
		# valid_actions format => [raise_action_info, call_action_info, fold_action_info]
		round_state['total_pot'] = cal_total_pot(round_state)

		if self.strategy_tree == None:
			file_name = 'data/{}/{}.json'.format(self.name, self.hands)
			node = None
			if not os.path.exists(file_name):
				with open(file_name, 'w') as f:
					node = ActionNode(2, 0, None)
					content = json.dumps(node.dict())
					f.write(content)
			else:
				with open(file_name, 'w') as f:
					content = f.read()
					data = json.loads(content)
					node = build_tree_from_dict(data)
			self.strategy_tree = node

		self.strategy_tree.choose_action(round_state, valid_actions)
		call_action_info = valid_actions[1]
		action, amount = call_action_info["action"], call_action_info["amount"]
		return action, amount  # action returned here is sent to the poker engine

	def receive_game_start_message(self, game_info):
		self.player_num = game_info['player_num']
		i = 0
		for p in game_info['seats']:
			if p['name'] == self.name:
				self.index = i
			i += 1

	def receive_round_start_message(self, round_count, hole_card, seats):
		self.hands = hole_card[0] + hole_card[1]

	def receive_street_start_message(self, street, round_state):
		pass

	def receive_game_update_message(self, action, round_state):
		pass

	def receive_round_result_message(self, winners, hand_info, round_state):
		pass


class FishPlayer2(BasePokerPlayer):  # Do not forget to make parent class as "BasePokerPlayer"

	#  we define the logic to make an action through this method. (so this method would be the core of your AI)
	def declare_action(self, valid_actions: dict, hole_card: list, round_state: dict):
		# valid_actions format => [raise_action_info, call_action_info, fold_action_info]

		call_action_info = valid_actions[1]
		action, amount = call_action_info["action"], call_action_info["amount"]
		return action, amount  # action returned here is sent to the poker engine

	def receive_game_start_message(self, game_info):
		pass

	def receive_round_start_message(self, round_count, hole_card, seats):
		pass

	def receive_street_start_message(self, street, round_state):
		pass

	def receive_game_update_message(self, action, round_state):
		pass

	def receive_round_result_message(self, winners, hand_info, round_state):
		pass
