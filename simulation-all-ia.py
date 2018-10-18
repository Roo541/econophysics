import numpy as np
from random import randint
import random
import matplotlib.pyplot as plt
import copy
import math

import agents

#global stuff
tmax = int(1e4)

agents.my_preferences = [
	[200,5,5,5,5],
	[200,5,5,5,5],
	[5,200,5,5,5],
	[5,200,5,5,5],
	[5,5,200,5,5],
	[5,5,200,5,5],
	[5,5,5,200,5],
	[5,5,5,200,5],
	[5,5,5,200,5],
	[5,5,5,200,5],
]
num_agents = len(agents.my_preferences)

agents.goods[:] = 100
agents.Bank_Account[:] = 100

agent_names = num_agents*["ia"]

t, old, agentU = agents.Market(agent_names, tmax)

for i in range(num_agents):
	print '  -- ', agents.goods[i], agent_names[i], i, agents.Bank_Account[i], agents.my_utilities[i](i, agents.goods[i])
print agents.Bank_Account[:num_agents]

#graphing smart agents utility
for i in range(num_agents):
                style = ':'
                if agent_names[i] == 'intelligent_agent' or agent_names[i] == 'ia':
                        style = 'k-'
                if agent_names[i] == 'IQ':
                        style = 'r--'
                if agent_names[i] == 'S2':
                        style = 'g--'
                if agent_names[i] == 'S3':
                        style = 'b-.'
		plt.plot(agentU[i][:], style, label = agent_names[i]) 
		plt.title('smart agents utility')
		plt.xlabel('time')
		plt.ylabel('utils')
plt.legend()

# ~ for g in range(5):
	# ~ plt.figure('Utility vs. good')
	# ~ gmax = tmax
	# ~ g0 = np.arange(0.0, gmax, 1.0)
	# ~ u0 = np.zeros_like(g0)
	# ~ agent_to_plot = 3
	# ~ for i in range(len(g0)):
		# ~ goods[agent_to_plot][:] = 0
		# ~ goods[agent_to_plot][g] = g0[i]
		# ~ u0[i] = Utility1(agent_to_plot, goods[agent_to_plot])

	# ~ plt.plot(g0, u0, label='$U(g_%d)$' % g)
	# ~ plt.legend(loc='best')
	# ~ plt.xlabel('amount of good')
	# ~ plt.ylabel('utility')

	# ~ plt.figure('Marginal utility')
	# ~ plt.plot(g0[1:], np.diff(u0), label=r'$\frac{\partial U}{\partial g_%d}$' % g)
	# ~ plt.xlabel('amount of good %d' % g)
	# ~ plt.legend(loc='best')
	# ~ plt.ylabel(r'marginal utility $\frac{\partial U}{\partial g_i}$')

print agents.box
plt.show()
#search past 10 rounds for highest bid and lowest ask of all goods
# ~ hi = 0
# ~ low = 1000000
# ~ for item in old[t-2:]:
	# ~ for i in range(len(my_agents)):
		# ~ a,b,c = item[i]
		# ~ if a == 'bid' and b > hi:
			# ~ hi = max(hi, b)
		# ~ if a == 'ask' and b < low:
			# ~ low = min(low, b)
# ~ print hi, low, old[t-2:]
