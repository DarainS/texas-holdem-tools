# -*- coding: utf-8 -*-
# author: shougang.deng@shopee.com


from pypokerengine.api.game import setup_config, start_poker

from cfr1.strategy import FishPlayer

config = setup_config(max_round=10, initial_stack=100, small_blind_amount=1)
config.register_player(name="p1", algorithm=FishPlayer())
config.register_player(name="p2", algorithm=FishPlayer())
config.register_player(name="p3", algorithm=FishPlayer())
game_result = start_poker(config, verbose=1)
print(game_result)
