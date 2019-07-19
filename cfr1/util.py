# -*- coding: utf-8 -*-
# author: shougang.deng@shopee.com


def cal_total_pot(round_state):
	pot = round_state['pot']
	pot_total = pot['main']['amount']
	for p in pot['side']:
		pot_total += p['amount']
