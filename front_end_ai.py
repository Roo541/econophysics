import numpy as np
from random import randint
import random
import matplotlib.pyplot as plt
import copy
import math
import csv

import agents

#global stuff
tmax = int(1e4)

i_g = 100
i_ba = 10000

agents.my_preferences = np.array([
	[200.,5,5,5,5],
	[200,5,5,5,5],
	[5,200,5,5,5],
	[5,200,5,5,5],
	[5,5,200,5,5],
	[5,5,200,5,5],
	[5,5,5,200,5],
	[5,5,5,200,5],
	[5,5,5,200,5],
	[5,5,5,200,5],
])
num_agents = len(agents.my_preferences)

agents.my_preferences *= 1
agents.goods[:] = i_g
agents.Bank_Account[:] = i_ba

agent_names = num_agents*["ia"]

t, old, agentU = agents.Market(agent_names, tmax)

for i in range(num_agents):
	print '  -- ', agents.goods[i], agents.marginal_utilities(i, agents.goods[i]), agent_names[i], i, agents.Bank_Account[i], agents.my_utilities[i](i, agents.goods[i])
print agents.Bank_Account[:num_agents]

for i in range(num_agents):
        marginal = agents.marginal_utilities(i, agents.goods[i])
        for g in range(agents.Numgoods):
                print 'agent', i, 'good', g, 'mu', marginal[g]/agents.box[g][3]

filename_base = 'test'
#Saves Data onto Excel file
myFile = open(filename_base+'.csv', 'w')
with myFile:
        writer = csv.writer(myFile, lineterminator='\n')
        writer.writerow(('Initial Conditions', 'goods = %d' %i_g, 'Bank_Account = %d' %i_ba,))
        writer.writerow(())
        writer.writerow(('Initial Preferences',))
        for i in range(num_agents):
			writer.writerow(('Agent_%d' %i, agents.my_preferences[i]))
        writer.writerow(())
        writer.writerow(('Goods for each Agent', 'g_0', 'g_1', 'g_2', 'g_3', 'g_4',))
        for i in range(num_agents):
                writer.writerow(('Agent_%d' %i,  agents.goods[i][0],agents.goods[i][1], agents.goods[i][2], agents.goods[i][3], agents.goods[i][4]))
        writer.writerow(())
        writer.writerow(('Bank Accounts', 'Dollars',))
        for i in range(num_agents):
                writer.writerow(('Agent_%d' %i, agents.Bank_Account[i]))
        writer.writerow(())
        writer.writerow(('Prices of Goods', 't-2', 't-1', 't', 'Avg',))
        for i in range(agents.Numgoods):
                writer.writerow(('good_%d' %i, agents.box[i][0], agents.box[i][1], agents.box[i][2], agents.box[i][3]))
        writer.writerow(())
        writer.writerow(('Money Utility', 'g_0', 'g_1', 'g_2', 'g_3', 'g_4',))
        for i in range(num_agents):
                marginal = agents.marginal_utilities(i, agents.goods[i])
                writer.writerow(('Agent_%d' %i, marginal[0]/agents.box[0][3], marginal[1]/agents.box[1][3], marginal[2]/agents.box[2][3], marginal[3]/agents.box[3][3], marginal[4]/agents.box[4][3],))
        writer.writerow(())
        writer.writerow(('Marginal Utility', 'g_0', 'g_1', 'g_2', 'g_3', 'g_4',))
        for i in range(num_agents):
                marginal = agents.marginal_utilities(i, agents.goods[i])
                writer.writerow(('Agent_%d' %i, marginal[0], marginal[1], marginal[2], marginal[3], marginal[4]))

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
plt.savefig(filename_base+'.svg')
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
