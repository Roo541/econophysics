import numpy as np
from random import randint
import random
import matplotlib.pyplot as plt
import copy
import math

#global stuff
tmax = 500
agents = 15
Numgoods = 5
goods = np.zeros((agents,Numgoods))
Bank_Account = np.zeros((agents))
box = np.zeros((Numgoods, 3))
smartU = np.zeros(tmax)
agentU = np.zeros((6, tmax))
#Filling out the arrays with initial values
for i in range(agents):
	for j in range(Numgoods):
		goods[i][j]= 100
for i in range(agents):
	Bank_Account[i] = 10000000
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

def smart_agent(my_id, offers, old_offers, old_transactions, my_preferences):
	choice = 'none'
	my_price = 0
	good = 0
	their_good = 0
	their_price = 0
	p = 0
	g = 0
	B = 0
	A = 0
	greed = randint(-1000,1000)
	Mu = greed/(Bank_Account[my_id]+1)
	U = my_utilities[my_id]
	Org = U(my_id, goods[my_id]) 
	print "Orginal Utility smart agent is ", Org
	for i in range(5):
		possible_goods =1*goods[my_id]
		possible_goods[i] += 1										#is this the correct indexing? or is the utility being adjusted for all goods added as calculated
		BuyingU = U(my_id, possible_goods) - box[i][2]*Mu
		if BuyingU > Org and BuyingU > B:
			choice = 'bid'
			price = int(math.ceil(box[i][2]))			#Must use a relevant price for my bid
			good0 = i
			B = BuyingU 
	for i in range(5):
		possible_goods = 1*goods[my_id]
		possible_goods[i] -= 1
		AskingU = U(my_id, possible_goods) + box[i][2]*Mu
		if AskingU > Org and AskingU > A:
			choice1 = 'ask'
			price1 = int(math.ceil(box[i][2]))			#Must use relevant price for my ask
			good1 = i
			A = AskingU 
	print "Smart Agent Utility if Bid:", B
	print "Smart Agent Utility if Ask:", A
	if Org > B and Org > A:
		return 'none', 0, 0
	if B > A and B > Org:
		choice = 'bid'
		my_price = price
		good = good0
		print 'compare is recommending a bid for smart agent in good ', good 
		for i in range(len(offers)):			#Going through offers and setting them to their_good place holder
			their_good = offers[i][2]
			their_price = offers[i][1]
			if i != my_id and offers[i][0] == 'ask' and their_good == good and their_price <= my_price:
				return 'bid', their_price, their_good
		return 'bid', my_price, good0
	if A > B and A > Org:
		choice = 'ask'
		my_price = price1
		good = good1
		print 'compare is recommending an ask for smart agent', good
		for i in range(len(offers)):			#Going through offers and setting them to their_good place holder
			their_good = offers[i][2]
			their_price = offers[i][1]
			if i != my_id and offers[i][0] == 'bid' and their_good == good and their_price >= my_price:
				return 'ask', their_price, their_good
		return 'ask', my_price, good1

#only makes or takes existing offers       
def other(my_id, offers, old_offers, old_transactions, my_preferences):
	choice = 'none'
	my_price = 0
	good = 0
	BuyingU = 0
	AskingU = 0
	B = 0
	A = 0
	U = my_utilities[my_id]
	Org = U(my_id, goods[my_id]) 
	print "Orginal Utility for other is ", Org
	for i in range(len(offers)):		
		a,b,c = offers[i]
		if a == 'ask' and i != my_id:
			possible_goods = 1*goods[my_id]
			possible_goods[c] += 1
			BuyingU = U(my_id, possible_goods)
			if BuyingU > Org and BuyingU > B:
				B = BuyingU
				choice = 'bid'
				my_price = b
				good = c 
		if a == 'bid' and i != my_id:
			possible_goods = 1*goods[my_id]
			possible_goods[c] -= 1
			AskingU = U(my_id, possible_goods)
			if AskingU > Org and AskingU > A:
				A = AskingU
				choice1 = 'ask'
				my_price1 = b
				good1 = c
	if B > A: 
		return 'bid', my_price, good
	if A > B:
		return 'ask', my_price1, good1
	if Org > B and Org > A:
		return 'none', 0, 0

def stubborn_seller(my_id, offers, old_offers, old_transactions, my_preferences):
	goodnum = randint(0,4)
	for i in range(20):
		if goods[my_id][goodnum] == 0:
			goodnum = randint(0,4)
	Ask0 = randint(1,1000)
	return 'ask', Ask0, goodnum

def Smart_Agent_2(my_id, offers, old_offers, old_transactions, my_preferences):
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
	print "Orginal Utility for SMART AGENT 2 is ", Org
	if randint(0,3) == 1 or True:
		print 'compare is recommending take an existing offer ###########'			#Going through offers
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
		if randint(0,1) == 1 and Bank_Account[my_id] > 0:							#Offers that don't beat original utility make a new bid or ask
		# Let's make a bid! 
			i = randint(0,4)			#random good
		# FUTURE: only want to bid on goods others have.
		# FUTURE: possibly use historical prices to guess what people will want to sell.
			possible_goods =1*goods[my_id]
			possible_goods[i] += 1
			break_even_price = (U(my_id, possible_goods) - Org)/Mu
			if break_even_price >= 1:
				price = randint(1, int(break_even_price)) # FIXME we should be smarter/ use historical prices for better bid
				return 'bid', price, i
			i = randint(0,4)
		# FUTURE: only want to ask on goods we have.
		# FUTURE: possibly use historical prices to guess what people will want to buy?
			possible_goods = 1*goods[my_id]
			possible_goods[i] -= 1
			break_even_price = (Org - U(my_id, possible_goods))/Mu
			if break_even_price >= 1:
				price = randint(int(break_even_price), int(1.25*break_even_price))
				return 'ask', price, i
	return 'none',0,0

#Only Buys good 0 and Sells good 4
def picky_agent(my_id, offers, old_offers, old_transactions, my_preferences):
	for i in range(len(offers)):
		if i != my_id and offers[i][0] == 'ask' and offers[i][2] == 0:
			price = offers[i][1]
			good = offers[i][2]
			return 'bid', price, good
		if i != my_id and offers[i][0] == 'bid' and offers[i][2] == 4:
			price = offers[i][1]
			good = offers[i][2]
			return 'ask', price, good
	price = randint(1,10)
	good = 4
	return 'ask', price, good

#Shopping addict
def shopping_addict(my_id, offers, old_offers, old_transactions, my_preferences):
	for i in range(len(offers)):
		if i != my_id and offers[i][0] == 'ask':
			return 'bid', offers[i][1], offers[i][2] 	#shopping addict just returns a. Wants to buy anything
	print "  &&&&&   NOTHING TO BUY, I'm SO SAD!", offers
	return 0,0,0

def Market(agents):
	t = 0
	old_offers = []
	old_transactions = []
	offers = [('none',0,0)]*len(agents)
	while t < tmax:
		print 'offers are', offers
		print 'IT IS NOW ROUND', t
		for i in shufflerange(len(agents)):
			#the following sends agent i his own id and returns: choice, price, good
			agentU[i][t] = update(i)
			choice, price, good = agents[i](i, offers, old_offers, old_transactions, my_preferences)
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
				print '   *** ', agent_names[i], i, 'makes no offer##################################################**********************'
		t = t + 1
		old_offers.append(copy.copy(offers))
	return t

agent_names = ["Smart_Agent_2", "picky_agent", "stubborn_seller", "smart_agent", "shopping_addict", "other"]
#my_agents = [Smart_Agent_2, Smart_Agent_2, stubborn_seller, smart_agent, shopping_addict, other]
my_agents = [Smart_Agent_2, Smart_Agent_2, stubborn_seller, smart_agent, shopping_addict, Smart_Agent_2]
my_utilities = [Utility1, Utility1, Utility1, Utility1, Utility1, Utility1]
my_preferences = [
	[20,5,5,5,5],		#Smart_Agent_2
	[5,20,5,5,5],			#picky_agent
	[5,5,20,5,5],			#stubborn Seller
	[5,5,5,20,5],		#smart Agent
	[20,5,5,5,5],			#Shopping Addict
	[5,5,5,5,20],			#other
		]
old_offers = Market(my_agents)

for i in range(len(my_agents)):
	print '  -- ', goods[i], agent_names[i], i
print Bank_Account[:len(my_agents)]
a0 = 0
a1 = 0
a2= 0
a3 = 0
a4=0
a5=0
A = [a0, a1, a2, a3, a4, a5]

#graphing smart agents utility 
for i in range(len(my_agents)):
	A[i], = plt.plot(agentU[i][:], label = agent_names[i]) 
	plt.title('smart agents utility')
	plt.xlabel('time')
	plt.ylabel('utils')
plt.legend(handles = [A[0], A[1], A[2], A[3], A[4], A[5]])


for g in range(5):
	plt.figure('Utility vs. good')
	gmax = tmax
	g0 = np.arange(0.0, gmax, 1.0)
	u0 = np.zeros_like(g0)
	agent_to_plot = 3
	for i in range(len(g0)):
		goods[agent_to_plot][:] = 0
		goods[agent_to_plot][g] = g0[i]
		u0[i] = Utility1(agent_to_plot, goods[agent_to_plot])

	plt.plot(g0, u0, label='$U(g_%d)$' % g)
	plt.legend(loc='best')
	plt.xlabel('amount of good')
	plt.ylabel('utility')

	plt.figure('Marginal utility')
	plt.plot(g0[1:], np.diff(u0), label=r'$\frac{\partial U}{\partial g_%d}$' % g)
	plt.xlabel('amount of good %d' % g)
	plt.legend(loc='best')
	plt.ylabel(r'marginal utility $\frac{\partial U}{\partial g_i}$')

# ~ print box        
plt.show()
print agentU[0][tmax-2],agentU[0][tmax-20]
print box
