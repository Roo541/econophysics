import numpy as np
from random import randint
import random
import matplotlib.pyplot as plt
import copy
import math

#global stuff
tmax = 500000
agents = 15
Numgoods = 5
goods = np.zeros((agents,Numgoods))
Bank_Account = np.zeros((agents))
box = np.zeros((Numgoods, 3))
agentU = np.zeros((10, tmax))
box[:][:] = 10
#Filling out the arrays with initial values
for i in range(agents):
	for j in range(Numgoods):
		goods[i][j]= 1000
for i in range(agents):
	Bank_Account[i] = 100000
utility_g = np.zeros(len(goods))

def Utility1(my_id, my_goods):
	value = Bank_Account[my_id]
	#Agent Utility update
	utility_A1 = np.zeros((1,tmax))	
	for i in range(Numgoods):
		utility_g[i] = my_preferences[my_id][i]*(my_goods[i]/my_preferences[my_id][i]/np.sqrt((my_goods[i]/my_preferences[my_id][i])**2+1))

	#Instantaneous utility for Agent 1 
	utility_A1 = utility_g[0] + utility_g[1] + utility_g[2] + utility_g[3] + utility_g[4] # + np.log10(np.abs(value)+1)
	return utility_A1

def update(my_id):
	U = my_utilities[my_id]
	update = U(my_id, goods[my_id])
	return update

def send(price,good):				#Gives a reasonable price for good based on past transactions
	if box[good][0] == 0:
		box[good][1] = price
	box[good][0] = box[good][1]
	box[good][1] = price
	box[good][2] = (box[good][0]+box[good][1])/2
	reasonable_price = box[good][2]
	return reasonable_price

def shufflerange(n):
	return random.sample(range(n), k=n)

def IQ(my_id, offers, old_offers, old_transactions, my_preferences,t):
	choice = 'none'
	my_price = 0
	good = 0
	B = 0
	A = 0
	U = my_utilities[my_id]
	Org = U(my_id, goods[my_id]) 
	Mu = 0
	high_bid = 0
	low_ask = 0
	for g in range(5):
		possible_goods = 1*goods[my_id]
		possible_goods[g] += 1
		marginalU = U(my_id, possible_goods) - Org
		Mu = max(Mu, marginalU/box[g][2])
	# ~ print "Orginal Utility for SMART AGENT 2 is ", Org
		for i in range(len(offers)):		
			a,b,c = offers[i]
			if a == 'ask' and i != my_id:
				possible_goods = 1*goods[my_id]
				possible_goods[c] += 1
				BuyingU = U(my_id, possible_goods) - b*Mu
				if BuyingU > Org and BuyingU > B:
					B = BuyingU
					choice = 'bid'
					my_price = b
					good = c 
			if a == 'bid' and i != my_id:
				possible_goods = 1*goods[my_id]
				possible_goods[c] -= 1
				AskingU = U(my_id, possible_goods) + b*Mu
				if AskingU > Org and AskingU > A:
					A = AskingU
					choice1 = 'ask'
					my_price1 = b
					good1 = c
	#Look past previous 10 offers		looking for a bargain
		high = 0
		low = 1000000
		for item in old_offers[t-3:]:
			for i in range(len(my_agents)):
				a,b,c = item[i]
				if a == 'bid' and b > high:
					high = max(high, b)
					possible_goods = 1*goods[my_id]
					possible_goods[c] -= 1
					AskingU = U(my_id, possible_goods) + high*Mu	
					if AskingU > A and AskingU > Org:
						A = AskingU
						my_price1 = randint(int(high), 5*int(high))
						choice = 'ask'
						good1 = c
				if a == 'ask' and b < low:
					low = min(low, b)
					possible_goods = 1*goods[my_id]
					possible_goods[c] += 1
					BuyingU = U(my_id, possible_goods) - low*Mu	
					if BuyingU > B and BuyingU > Org:
						B = BuyingU
						my_price = randint(1,int(low))
						choice = 'bid'
						good = c
	if B > A: 
		return 'bid', my_price, good
	if A > B:
		return 'ask', my_price1, good1
	if True:							#Offers that don't beat original utility make a new bid or ask
		# Let's make a bid! 
		i = randint(0,4)			#random good
		# FUTURE: only want to bid on goods others have.
		# FUTURE: possibly use historical prices to guess what people will want to sell.
		if Bank_Account[my_id] > 0:
			possible_goods =1*goods[my_id]
			possible_goods[i] += 1
			break_even_price = (U(my_id, possible_goods) - Org)/Mu
			if break_even_price >= 1 and box[i][2] <= break_even_price:
				price = randint(1, int(break_even_price))
				return 'bid', price, i
		i = randint(0,4)
		if goods[my_id][i] >= 0:
			possible_goods = 1*goods[my_id]
			possible_goods[i] -= 1
			break_even_price = (Org - U(my_id, possible_goods))/Mu
			if break_even_price >= 1 and box[i][2] >= break_even_price:
				price = randint(int(break_even_price), 5*int(break_even_price)-1)
				return 'ask', price, i
	else:
				for i in range(5):
					possible_goods = 1*goods[my_id]
					possible_goods[c] -= 1
					AskingU = U(my_id, possible_goods) + b*Mu
					if AskingU > Org and AskingU > A:
						A = AskingU
						choice1 = 'ask'
						my_price1 = randint(int(box[i][2]), 5*int(box[i][2]))
						good1 = i
				return 'ask', my_price1, good1
	return 'none',0,0

def stubborn_seller(my_id, offers, old_offers, old_transactions, my_preferences,t):
	goodnum = randint(0,4)
	for i in range(20):
		if goods[my_id][goodnum] == 0:
			goodnum = randint(0,4)
	price = randint(1,50)
	return 'ask', price, goodnum

def Smart_Agent_2(my_id, offers, old_offers, old_transactions, my_preferences,t):
	choice = 'none'
	my_price = 0
	good = 0
	B = 0
	A = 0
	U = my_utilities[my_id]
	Org = U(my_id, goods[my_id]) 
	Mu = 0
	for g in range(5):
		possible_goods = 1*goods[my_id]
		possible_goods[g] += 1
		marginalU = U(my_id, possible_goods) - Org
		Mu = max(Mu, marginalU/box[g][2])
	# ~ print "Orginal Utility for SMART AGENT 2 is ", Org
		for i in range(len(offers)):		
			a,b,c = offers[i]
			if a == 'ask' and i != my_id:
				possible_goods = 1*goods[my_id]
				possible_goods[c] += 1
				BuyingU = U(my_id, possible_goods) - b*Mu
				if BuyingU > Org and BuyingU > B:
					B = BuyingU
					choice = 'bid'
					my_price = b
					good = c 
			if a == 'bid' and i != my_id:
				possible_goods = 1*goods[my_id]
				possible_goods[c] -= 1
				AskingU = U(my_id, possible_goods) + b*Mu
				if AskingU > Org and AskingU > A:
					A = AskingU
					choice1 = 'ask'
					my_price1 = b
					good1 = c
		if B > A: 
			return 'bid', my_price, good
		if A > B:
			return 'ask', my_price1, good1
		if Bank_Account[my_id] > 0:							#Offers that don't beat original utility make a new bid or ask
		# Let's make a bid! 
			i = randint(0,4)			#random good
		# FUTURE: only want to bid on goods others have.
		# FUTURE: possibly use historical prices to guess what people will want to sell.
			possible_goods =1*goods[my_id]
			possible_goods[i] += 1
			break_even_price = (U(my_id, possible_goods) - Org)/Mu
			if break_even_price >= 1 and box[i][2] <= break_even_price:
				price = randint(1, int(break_even_price))
				return 'bid', price, i
			i = randint(0,4)
			if goods[my_id][i] >= 0:
				possible_goods = 1*goods[my_id]
				possible_goods[i] -= 1
				break_even_price = (Org - U(my_id, possible_goods))/Mu
				if break_even_price >= 1 and box[i][2] >= break_even_price:
					price = randint(int(break_even_price), 5*int(break_even_price))
					return 'ask', price, i
	return 'none',0,0

def Smart_Agent_3(my_id, offers, old_offers, old_transactions, my_preferences,t):
	choice = 'none'
	my_price = 0
	good = 0
	B = 0
	A = 0
	U = my_utilities[my_id]
	Org = U(my_id, goods[my_id]) 
	Mu = 0
	for g in range(5):
		possible_goods = 1*goods[my_id]
		possible_goods[g] += 1
		marginalU = U(my_id, possible_goods) - Org
		Mu = max(Mu, marginalU/box[g][2])
	# ~ print "Orginal Utility for SMART AGENT 2 is ", Org
	if randint(0,3) == 1 or True:
		# ~ print 'compare is recommending take an existing offer ###########'			#Going through offers
		for i in range(len(offers)):		
			a,b,c = offers[i]
			if a == 'ask' and i != my_id:
				possible_goods = 1*goods[my_id]
				possible_goods[c] += 1
				BuyingU = U(my_id, possible_goods) - b*Mu
				if BuyingU > Org and BuyingU > B:
					B = BuyingU
					choice = 'bid'
					my_price = b
					good = c 
			if a == 'bid' and i != my_id:
				possible_goods = 1*goods[my_id]
				possible_goods[c] -= 1
				AskingU = U(my_id, possible_goods) + b*Mu
				if AskingU > Org and AskingU > A:
					A = AskingU
					choice1 = 'ask'
					my_price1 = b
					good1 = c
		if B > A: 
			return 'bid', my_price, good
		if A > B:
			return 'ask', my_price1, good1
		if Bank_Account[my_id] > 0:							#Offers that don't beat original utility make a new bid or ask
		# Let's make a bid! 
			i = randint(0,4)			#random good
		# FUTURE: only want to bid on goods others have.
		# FUTURE: possibly use historical prices to guess what people will want to sell.
			possible_goods =1*goods[my_id]
			possible_goods[i] += 1
			break_even_price = (U(my_id, possible_goods) - Org)/Mu
			if break_even_price >= 1 and box[i][2] <= break_even_price:
				price = randint(1, int(break_even_price))
				return 'bid', price, i
			i = randint(0,4)
			if goods[my_id][i] >= 0:
				possible_goods = 1*goods[my_id]
				possible_goods[i] -= 1
				break_even_price = (Org - U(my_id, possible_goods))/Mu
				if break_even_price >= 1 and box[i][2] >= break_even_price:
					price = randint(int(break_even_price), 5*int(break_even_price))
					return 'ask', price, i
			else:
				for i in range(5):
					possible_goods = 1*goods[my_id]
					possible_goods[c] -= 1
					AskingU = U(my_id, possible_goods) + b*Mu
					if AskingU > Org and AskingU > A:
						A = AskingU
						choice1 = 'ask'
						my_price1 = randint(int(box[i][2]), 5*int(box[i][2]))
						good1 = i
				return 'ask', my_price1, good1
	return 'none',0,0

#Shopping addict
def shopping_addict(my_id, offers, old_offers, old_transactions, my_preferences,t):
	for i in range(len(offers)):
		if i != my_id and offers[i][0] == 'ask':
                        return 'bid', offers[i][1], offers[i][2] 	#shopping addict just returns a. Wants to buy anything
	# ~ print "  &&&&&   NOTHING TO BUY, I'm SO SAD!"
	return 0,0,0

def Market(agents):
	t = 0
	old_offers = []
	old_transactions = []
	offers = [('none',0,0)]*len(agents)
	while t < tmax:
		# ~ print 'offers are', offers
		print 'IT IS NOW ROUND', t
		for i in shufflerange(len(agents)):
			#the following sends agent i his own id and returns: choice, price, good
			agentU[i][t] = update(i)
			choice, price, good = agents[i](i, offers, old_offers, old_transactions, my_preferences,t)
			offers[i] = (choice, price, good)											#starts with agent0
			if choice == 'ask':
				print '   *** ', agent_names[i], i, 'asks $%d' % price, 'for good', good
				if goods[i][good] <= 0:												#checking if seller has that quantity of good
					print 'SILLY AGENT', i, "you don't have enough of good", good, '!!!!!'
					offers[i] = ('none',0,0)
				else:
					for j in shufflerange(len(agents)):
						if j != i:											#checking for any buyers other than selling agent
							if offers[j] == ('bid', price, good) and Bank_Account[j] >= price:	#checks if buyer has enough money to purchase good
								print 'We MATCH!!!'
								goods[i][good] = goods[i][good] - 1
								goods[j][good] = goods[j][good] + 1
								Bank_Account[i] = Bank_Account[i] + price
								Bank_Account[j] = Bank_Account[j] - price
								old_transactions.append((price,good))
								offers[i] = ('none',0,0)
								offers[j] = ('none',0,0)
								send(price,good)
								break
			if choice == 'bid':
				print '   *** ', agent_names[i], i, 'bids $%d' % price, 'for good', good
				if Bank_Account[i] < price:
					print 'SILLY AGENT', i, "you don't have $%d" % price, '!!!!!'
					offers[i] = ('none',0,0)
				else:
					for j in shufflerange(len(agents)):
						if j != i:
							if offers[j] == ('ask', price, good) and goods[j][good] > 1:
								print 'We MATCH!!!'
								goods[i][good] = goods[i][good] + 1
								goods[j][good] = goods[j][good] - 1
								Bank_Account[i] = Bank_Account[i] - price
								Bank_Account[j] = Bank_Account[j] + price
								old_transactions.append((price,good))
								offers[i] = ('none',0,0)
								offers[j] = ('none',0,0)
								send(price,good)
								break
			if choice == 'none':
				print '   *** ', agent_names[i], i, 'makes no offer'
		t = t + 1
		old_offers.append(copy.copy(offers))
	return t, old_offers

agent_by_name =	{
				"IQ": IQ,
				"S2": Smart_Agent_2,
				"S3": Smart_Agent_3,
				"Shopping Addict": shopping_addict,
				"Stubborn Seller": stubborn_seller,
				}
agent_names = ["IQ",
               "IQ",
               "Stubborn Seller",
               "Shopping Addict",
               "S2",
               "S2",
               "S2",
               "S3",
               "S3",
               "S3"]
my_agents = [agent_by_name[i] for i in agent_names]
my_utilities = [Utility1,
				Utility1,
				Utility1,
				Utility1, 
				Utility1, 
				Utility1, 
				Utility1, 
				Utility1, 
				Utility1, 
				Utility1]
my_preferences = [
	[200,5,5,5,5],			#IQ
	[5,200,5,5,5],			#IQ
	[5,5,200,5,5],			#IQ
	[5,5,5,200,5],			#Shoppint addict
	[5,5,5,5,200],			#S2
	[200,5,5,5,5],			#S2
	[5,200,5,5,5],			#S2
	[5,5,200,5,5],			#S3
	[5,5,5,200,5],			#S3
	[5,5,5,5,200]			#S3
		]
t, old = Market(my_agents)

for i in range(len(my_agents)):
	print '  -- ', goods[i], agent_names[i], i, Bank_Account[i], my_utilities[i](i, goods[i])
print Bank_Account[:len(my_agents)]
a0 = 0
a1 = 0
a2= 0
a3 = 0
a4= 0
a5= 0
a6 = 0
a7 = 0
a8 = 0
a9 = 0
A = [a0, a1, a2, a3, a4, a5, a6, a7, a8, a9]

#graphing smart agents utility 
for i in range(len(my_agents)):
                style = ':'
                if agent_names[i] == 'intelligent_agent':
                        style = 'k-'
                if agent_names[i] == 'S1':
                        style = 'r--'
                if agent_names[i] == 'S1':
                        style = 'r--'
                if agent_names[i] == 'S2':
                        style = 'g--'
                if agent_names[i] == 'S3':
                        style = 'b-.'
		A[i], = plt.plot(agentU[i][:], style, label = agent_names[i]) 
		plt.title('smart agents utility')
		plt.xlabel('time')
		plt.ylabel('utils')
plt.legend(handles = [A[0], A[1], A[2], A[3], A[4], A[5], A[6], A[7], A[8], A[9]])

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

# ~ print box   
print box     
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
