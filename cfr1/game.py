# -*- coding: utf-8 -*-
# author: shougang.deng@shopee.com


from pypokerengine.api.game import setup_config, start_poker

from cfr1.strategy import FishPlayer

config = setup_config(max_round=10, initial_stack=100, small_blind_amount=1)
config.register_player(name="p1", algorithm=FishPlayer('p1'))
config.register_player(name="p2", algorithm=FishPlayer('p2'))
config.register_player(name="p3", algorithm=FishPlayer('p3'))
game_result = start_poker(config, verbose=2)
print(game_result)
