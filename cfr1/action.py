# -*- coding: utf-8 -*-
# author: shougang.deng@shopee.com
from enum import Enum


class PlayerAction(Enum):
	Check = 'check'
	Call = 'call'
	Bet_0_5 = 'bet 0.5'
	Bet_1 = 'bet 1'
	Bet_2 = 'bet 2'
	AllIn = 'all in'
	Fold = 'fold'

	def __hash__(self):
		return self.name.__hash__()

	def __str__(self):
		return self.name


ActionList = [action.name for action in PlayerAction]
