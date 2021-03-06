import numpy as np
from random import randint
import matplotlib.pyplot as plt
import copy

#global stuff
agents = 15
Numgoods = 5
goods = np.zeros((agents,Numgoods))
Calories = np.zeros((Numgoods,1))
Bank_Account = np.zeros((agents))
Umax0 = 5
Umax1 = 50000
Q0 = 500 #minimum calories needed
alpha0 = 10000
alpha1 = 1
#Filling out the arrays with initial values
for i in range(agents):
	for j in range(Numgoods):
		goods[i][j]= 10
for i in range(Numgoods):
	Calories[i][0] = 100
for i in range(agents):
	Bank_Account[i] = 1000
Ua0 = [0 for i in range (10)]
Ua1 = [0 for i in range (10)]

def Utility0():
	#Agent 0 Utility update
	utility_A0 = np.zeros((1,100))
	utility_Calories = 0
	g = np.arange(0.0, 750, 0.5)	
	utilityNew0 = 0
	j = 0
	g1 = 5							#specific good happiness for agent 1 
	g2 = 7
	g3 = 9
	g4 = 11
	g5 = 13
	while (j < 10):
		#Calculates utility value at given point in time
		utility_g1 = 100*(goods[0][0]/g1)/((goods[0][0]/g1)**2+1)
		utility_g2 = 100*(goods[0][1]/g2)/((goods[0][1]/g2)**2+1)
		utility_g3 = 100*(goods[0][2]/g3)/((goods[0][2]/g3)**2+1)
		utility_g4 = 100*(goods[0][3]/g4)/((goods[0][3]/g4)**2+1)
		utility_g5 = 100*(goods[0][4]/g5)/((goods[0][4]/g5)**2+1)

		for i in range(goods):
			utility_Calories = utility_Calories + 100*(goods[0][i]*Calories[i][0]/Q0)/(goods[0][i]*Calories[i][0]/Q0+1)

		#Instantaneous utility for Agent 0 
		utility_A0 = utility_g1 + utility_g2 + utility_g3 + utility_g4 + utility_g5 + utility_Calories
		Ua0[j] = utility_A0
		j = j+1
	for i in range(10):
		if Ua0[i] == 0 and Ua0[i-1] != 0:
			utilityNew0 = Ua0[i-1]
		else: i = i + 1
	return utilityNew0

def Utility1():
	#Agent 1 Utility update
	utility_A1 = np.zeros((1,100))
	utility_Calories = 0
	g = np.arange(0.0, 750, 0.5)	
	utilityNew1 =0
	j = 0
	g1 = 1							#specific good happiness for agent 1 
	g2 = 2
	g3 = 3
	g4 = 4
	g5 = 5
	while (j < 10):
		#Calculates utility value at given point in time
		utility_g1 = 100*(goods[1][0]/g1)/((goods[1][0]/g1)**2+1)
		utility_g2 = 100*(goods[1][1]/g2)/((goods[1][1]/g2)**2+1)
		utility_g3 = 100*(goods[1][2]/g3)/((goods[1][2]/g3)**2+1)
		utility_g4 = 100*(goods[1][3]/g4)/((goods[1][3]/g4)**2+1)
		utility_g5 = 100*(goods[1][4]/g5)/((goods[1][4]/g5)**2+1)

		for i in range(goods):
			utility_Calories = utility_Calories + 100*(goods[1][i]*Calories[i][0]/Q0)/(goods[1][i]*Calories[i][0]/Q0+1)

		#Instantaneous utility for Agent 1 
		utility_A1 = utility_g1 + utility_g2 + utility_g3 + utility_g4 + utility_g5 + utility_Calories
		Ua1[j] = utility_A1
		j = j+1
		
	for i in range(10):
		if Ua1[i] == 0 and Ua1[i-1] != 0:
			utilityNew1 = Ua1[i-1]
		else: i = i + 1
	return utilityNew1

# TODO
#
# 1. Implement another agent.
#
# 2. Increase number of agents.
#
# 3. Add output in case of things that aren't bids or asks.
#
# 4. THINK about how to start making a practical agent (using utility, etc).
#
# 5. Fix bug where a given offer is taken up twice! (need to reset offers value)

#Stubborn Seller
def Agent0(my_id, offers, old_offers):
	Ask0 = randint(1,10)
	return 'ask', Ask0, randint(0,4)

#Stubborn Buyer
def Agent1(my_id, offers, old_offers):
	price = randint(0,10)
        good = randint(0,4)
	return 'bid', price, good

#Shopping addict
def shopping_addict(my_id, offers, old_offers):
        for i in range(len(offers)):
                if i != my_id and offers[i][0] == 'ask':
                        return 'bid', offers[i][1], offers[i][2]
	price = randint(0,10)
        good = randint(0,4)
	return 'bid', price, good

def Market(agents):
        t = 0
        old_offers = []
        offers = [('none',0,0)]*len(agents)
        while t < 10:
                print '                             offers are', offers
                print 'IT IS NOW ROUND', t
                for i in range(len(agents)):
                        choice, price, good = agents[i](i, offers, old_offers)
                        offers[i] = (choice, price, good)
                        if choice == 'ask':
                                print '   agent', i, 'asks $%d' % price, 'for good', good
                                if goods[i][good] < 1:
                                        print 'SILLY AGENT', i, 'you have no', good, '!!!!!'
                                else:
                                        for j in range(len(agents)):
                                                if j != i:
                                                        if offers[j] == ('bid', price, good) and Bank_Account[j] >= price:
                                                                print 'We MATCH!!!'
                                                                goods[i][good] = goods[i][good] - 1
                                                                goods[j][good] = goods[j][good] + 1
                                                                Bank_Account[i] = Bank_Account[i] + price
                                                                Bank_Account[j] = Bank_Account[j] - price
                        elif choice == 'bid':
                                print '   agent', i, 'bids $%d' % price, 'for good', good
                                if Bank_Account[i] < price:
                                        print 'SILLY AGENT', i, "you don't have $%d" % price, '!!!!!'
                                else:
                                        for j in range(len(agents)):
                                                if j != i:
                                                        if offers[j] == ('ask', price, good) and goods[j][good] > 1:
                                                                print 'We MATCH!!!'
                                                                goods[i][good] = goods[i][good] + 1
                                                                goods[j][good] = goods[j][good] - 1
                                                                Bank_Account[i] = Bank_Account[i] - price
                                                                Bank_Account[j] = Bank_Account[j] + price
                        else:
                                pass

	        # A0,gRand = Agent0()			#Updates Utility and makes Trade proposals
	        # B1 = Agent1(A0)
	        # Market(A0, B1, gRand)				#Makes Trades and Updates goods and bank account
	        t = t + 1
                old_offers.append(copy.copy(offers))

my_agents = [Agent0, shopping_addict, shopping_addict]
Market(my_agents)

print goods[:len(my_agents)]
print Bank_Account[:len(my_agents)]






















#creating utility function depending on calories
Q = np.arange(0.0, 5000.0, 0.5)
utility_Calories = 100*(Q / Q0) / ((Q / Q0) + 1) 
#creating utility function for goods 1-5
#~ g = np.arange(0.0, 750, 1)
#~ utility_g1 = 100*(g/5)/((g/5)**2+1)

#~ plt.plot(g,utility_g1)
#~ plt.title('Utility as a Function of good1')
#~ plt.xlabel('Quantity of good')
#~ plt.ylabel('Utils')
#~ plt.show()

#~ #graphing Calorie Utility
#~ plt.plot(Q,utility_Calories)
#~ plt.title('Utility as a Function of Calories')
#~ plt.xlabel('Calories')
#~ plt.ylabel('Utils')
#~ plt.show()

