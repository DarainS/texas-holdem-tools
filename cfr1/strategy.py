# -*- coding: utf-8 -*-
# author: shougang.deng@shopee.com
import json
import time
from random import Random

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
		m = {}
		with open('result.json') as f:
			m = json.loads(f.read())
		if m.get(name) is None:
			m[name] = {}
		self.values = m[name]

	#  we define the logic to make an action through this method. (so this method would be the core of your AI)
	def declare_action(self, valid_actions, hole_card, round_state):
		# valid_actions format => [raise_action_info, call_action_info, fold_action_info]
		hands = hole_card[0] + hole_card[1]
		vals = self.values.get(hands, {})
		cal_total_pot(round_state)

		pre_flop = vals.get('preflop-5', {})

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
