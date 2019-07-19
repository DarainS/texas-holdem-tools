# -*- coding: utf-8 -*-
# author: shougang.deng@shopee.com
import random
import time

from cfr1.action import PlayerAction, ActionList

rand = random.Random()
rand.seed(int(time.time()))


def build_tree_from_dict(data: dict):
	player_num = data.get('player_num', 2)
	my_index = data.get('my_index', 0)
	root = ActionNode(player_num, my_index, None)
	root.__dict__ = data.get('data')
	return root


class ActionNode(object):
	def __init__(self, player_num, my_index, player_action: PlayerAction):
		self.player_num = player_num
		self.index = my_index
		self.player_action = player_action
		self.children = {}
		self.action_regret = {k: 1. / len(ActionList) for k in ActionList}

	def dict(self):
		mydict = self.__dict__
		for key in mydict.keys():
			if type(key) is not str:
				try:
					mydict[str(key)] = mydict[key]
				except:
					try:
						mydict[repr(key)] = mydict[key]
					except:
						pass
		return mydict

	def add_child(self, child):
		self.children[child.player_action] = child
		return child

	def choose_action(self, round_state: dict, valid_action: dict) -> (str, int):
		m = 0
		ac = PlayerAction.Call
		total_pot = round_state['total_pot']
		call_num = 99999
		actions = {i['action']: i for i in valid_action}
		valid_action = actions
		if valid_action.get('call'):
			call_num = valid_action['call']['amount']
		raise_num = 99999
		max_num = 99999
		if valid_action.get('raise'):
			raise_num = valid_action['raise']['amount']['min']
			max_num = valid_action['raise']['amount']['max']
		result = ()
		for k, v in self.action_regret.items():
			if v <= m:
				if ac == PlayerAction.Check:
					if 'check' in valid_action:
						result = 'check', 0
				if ac == PlayerAction.Call:
					if 'call' in valid_action:
						result = 'call', call_num
				if ac == PlayerAction.AllIn:
					stack = round_state['seats'][self.index]
					if stack >= raise_num:
						return 'raise', stack
					else:
						return 'call', stack
				factor = 0
				if ac == PlayerAction.Bet_0_5:
					factor = 0.5
				elif ac == PlayerAction.Bet_1:
					factor = 1.0
				elif ac == PlayerAction.Bet_2:
					factor = 2.0
				if factor > 0:
					if total_pot * factor >= raise_num:
						result = 'raise', total_pot * 0.5
					elif total_pot * factor >= call_num:
						result = 'call', call_num

		return result
