# -*- coding: utf-8 -*-
# author: shougang.deng@shopee.com

from pycfr.pycfr.pokergames import *
from pycfr.pycfr.pokerstrategy import *

rules = leduc_rules()

# load first player strategy
s0 = Strategy(0)
s0.load_from_file('pycfr/strategies/leduc/0.strat')

# load second player strategy
s1 = Strategy(1)
s1.load_from_file('pycfr/strategies/leduc/1.strat')

# Create a strategy profile for this game
profile = StrategyProfile(rules, [s0, s1])

# Calculates the best response for every agent and the value of that response
brev = profile.best_response()

# The first element is a StrategyProfile of all the best responses
best_response = brev[0]

# The second element is a list of expected values of the responses vs. the original strategy profile
expected_values = brev[1]

# Get the rules of the game
hskuhn = half_street_kuhn_rules()

# Create the CFR minimizer
from pycfr.pycfr.pokercfr import CounterfactualRegretMinimizer

cfr = CounterfactualRegretMinimizer(hskuhn)

# Run a number of iterations, determining the exploitability of the agents periodically
iterations_per_block = 1000
blocks = 10
for block in range(blocks):
	print('Iterations: {0}'.format(block * iterations_per_block))
	cfr.run(iterations_per_block)
	result = cfr.profile.best_response()
	print('Best response EV: {0}'.format(result[1]))
	print('Total exploitability: {0}'.format(sum(result[1])))

# The final result is a strategy profile of epsilon-optimal agents
nash_strategies = cfr.profile
