import numpy as np
from random import randint
import random
import matplotlib.pyplot as plt
import copy

#global stuff
agents = 15
Numgoods = 5
goods = np.zeros((agents,Numgoods))
Calories = np.zeros((Numgoods,1))
Bank_Account = np.zeros((agents))
Q0 = 500 #minimum calories needed
smartU = np.zeros(100)
agentU = np.zeros((6, 100))
aSavings = [10000,25000,30000,40000,500000,10000]
#Filling out the arrays with initial values
for i in range(agents):
	for j in range(Numgoods):
		goods[i][j]= 10
for i in range(Numgoods):
	Calories[i][0] = 100
for i in range(agents):
	Bank_Account[i] = 1000
utility_g = np.zeros(len(goods))
utility_s = np.zeros(agents)

def Utility1(my_id, my_goods, other):
	#Agent 1 Utility update
	utility_A1 = np.zeros((1,100))
	if other == 'a' :
	    for i in range(Numgoods):
		    utility_g[i] = my_preferences[my_id][i]*(my_goods[i]/my_preferences[my_id][i]/np.sqrt((my_goods[i]/my_preferences[my_id][i])**2+1))
		    utility_s[my_id] = aSavings[my_id]*(Bank_Account[my_id]/aSavings[my_id]/np.sqrt((Bank_Account[my_id]/aSavings[my_id])**2+1))
	if other == 1:
	    for i in range(Numgoods):
		    utility_g[i] = my_preferences[my_id][i]*(my_goods[i]/my_preferences[my_id][i]/np.sqrt((my_goods[i]/my_preferences[my_id][i])**2+1))
		    utility_s[my_id] = aSavings[my_id]*(Bank_Account[my_id]/aSavings[my_id]/np.sqrt((Bank_Account[my_id]/aSavings[my_id])**2+1))
	#Instantaneous utility for Agent 1 
	utility_A1 = utility_g[0] + utility_g[1] + utility_g[2] + utility_g[3] + utility_g[4] # + utility_s[my_id]
        return utility_A1

# TODO
#
# 1. Try to make smart_agent use offers and prices to buy and sell. check but still no monetary_desperation because I am confused
#    (monetary_desperation = mu?).
#
# 2. Make utility function use arrays as inputs, maybe also have different asymptotes. Check

def update(my_id):
        U = my_utilities[my_id]
        update = U(my_id, goods[my_id], 'a')
        return update

def shufflerange(n):
        return random.sample(range(n), k=n)
        
def smart_agent(my_id, offers, old_offers, old_transaction, my_preferences):
        # ~ choice, my_price, good = compare(my_id)
        print old_transaction
        choice = 'none'
        my_price = 0
        good = 0
	current_good = 0
        B = 0
        A = 0
	BestDeal = 0
        U = my_utilities[my_id]
        OriginalU = U(my_id, goods[my_id], 'a')
        print "Orginal Utility is ", OriginalU
	#existing Ask offers
	for i in range(5):
	    if offers[i][0] == 'ask':
		other = offers[i][2]
		possible_goods =1*goods[my_id]
                possible_goods[other] += 1
		Current_Ask_U = U(my_id, possible_goods, 1)
		print "buying from existing offers is", Current_Ask_U
		if Current_Ask_U > OriginalU and Current_Ask_U > BestDeal:
		    BestDeal = Current_Ask_U
		    choiceBestDeal = 'bid'
		    priceBestDeal = offers[i][1]
		    goodBestDeal = other
	#existing Bid offers
	for i in range(5):
	    if offers[i][0] == 'bid':
		print "############################"
		other = offers[i][2]
		possible_goods =1*goods[my_id]
                possible_goods[other] -= 1
		Current_Bid_U = U(my_id, possible_goods, 1)
		print "buying from existing offers is", Current_Bid_U
		if Current_Bid_U > OriginalU and Current_Bid_U > BestDeal:
		    print "############################"
		    BestDeal = Current_Bid_U
		    choiceBestDeal = 'ask'
		    priceBestDeal = offers[i][1]
		    goodBestDeal = other
	for i in range(5):
                possible_goods =1*goods[my_id]
                possible_goods[i] += 1
                BuyingU = U(my_id, possible_goods, 'a')
                if BuyingU > OriginalU and BuyingU > B:
                        B = BuyingU
                        choiceB = 'bid'
                        my_priceB = randint(1,10)
                        goodB = i
	for i in range(5):
                possible_goods = 1*goods[my_id]
                possible_goods[i] -= 1
                AskingU = U(my_id, possible_goods, 'a')
                if AskingU > OriginalU and AskingU > A:
                        A = AskingU
                        choice1 = 'ask'
                        price1 = randint(1,10)
                        good1 = i
	print "Smart Agent Utility if Bid:", B
	print "Smart Agent Utility if Ask:", A
        # Let's default to accepting any offer that seems to benefit
        # us.  Yes, we might do better by holding out for something
        # even more lucrative, but someone else might also snap up
        # this offer.
        if BestDeal > OriginalU:
            choice = choiceBestDeal
	    my_price = priceBestDeal
	    good = goodBestDeal
	    print "########################################################################################################"
	elif A > B:
	    choice = 'ask'
	    my_price = price1
	    good = good1
            print 'compare is recommending an ask'
	else:
	    choice = choiceB
	    my_price = my_priceB
	    good = goodB
        for i in range(len(offers)):
                their_good = offers[i][2]
                their_price = offers[i][1]
		if i != my_id and choice == 'bid' and offers[i][0] == 'ask' and their_good == good and their_price <= my_price:
                        return 'bid', their_price, good
        for i in range(len(offers)):
                their_good = offers[i][2]
                their_price = offers[i][1]
		if i != my_id and choice == 'ask' and offers[i][0] == 'bid' and their_good == good and their_price >= my_price:
                        return 'ask', their_price, good
        return choice, my_price, good
        
def other(my_id, offers, old_offers, old_transactions, my_preferences):
        # ~ choice, my_price, good = compare(my_id)
        choice = 'none'
        my_price = 0
        good = 0
        for i in range(len(offers)):
                their_good = offers[i][2]
                their_price = offers[i][1]
		if i != my_id and choice == 'bid' and offers[i][0] == 'ask' and their_good == good and their_price <= my_price:
                        return 'bid', their_price, good
        for i in range(len(offers)):
                their_good = offers[i][2]
                their_price = offers[i][1]
		if i != my_id and choice == 'ask' and offers[i][0] == 'bid' and their_good == good and their_price >= my_price:
                        return 'ask', their_price, good
        return choice, my_price, good

def stubborn_seller(my_id, offers, old_offers, old_transactions, my_preferences):
        goodnum = randint(0,4)
        for i in range(20):
                if goods[my_id][goodnum] == 0:
                        goodnum = randint(0,4)
	Ask0 = random.randint(1,10)
	return 'ask', Ask0, goodnum

def stubborn_buyer(my_id, offers, old_offers, old_transactions, my_preferences):
	price = randint(1,10)
	good = randint(0,4)
	#choice, good = Utility0 
	return 'bid', price, good

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
        print "     NOTHING TO BUY, I'm SO SAD!", offers
	return 0,0,0

def Market(agents):
        t = 0
        old_offers = []
        old_transaction = [0,0,0,0,0]
        current_offers = [0,0,0,0,0]
        offers = [('none',0,0)]*len(agents)
        while t < 100:
                print 'offers are', offers
                print 'IT IS NOW ROUND', t
                for i in shufflerange(len(agents)):
                        #the following sends agent i his own id and returns: choice, price, good
                        agentU[i][t] = update(i)				#updates each agents utility
                        choice, price, good = agents[i](i, offers, old_offers, old_transaction, my_preferences)
                   
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
                                                                offers[i] = ('none',0,0)
                                                                offers[j] = ('none',0,0)
                                                                old_transaction[i] = price
                                                                break
                        elif choice == 'bid':
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
                                                                offers[i] = ('none',0,0)
                                                                offers[j] = ('none',0,0)
                                                                old_transaction[i] = price
                                                                break
                        else:
                                print '   *** ', agent_names[i], i, 'makes no offer'

	        # A0,gRand = Agent0()			#Updates Utility and makes Trade proposals
	        # B1 = Agent1(A0)
	        # Market(A0, B1, gRand)				#Makes Trades and Updates goods and bank account
	        t = t + 1
                old_offers.append(copy.copy(offers))
        return t, old_transaction

               

agent_names = ["stubborn_buyer", "picky_agent", "stubborn_seller", "smart_agent", "shopping_addict", "other"]
my_agents = [stubborn_buyer, picky_agent, stubborn_seller, smart_agent, shopping_addict, other]
my_utilities = [Utility1, Utility1, Utility1, Utility1, Utility1, Utility1]
my_preferences = [
        [3,7,15,4,25],
        [3,16,19,2,40],
        [7,8,35,5,20],			#stubborn Seller
        [10,100,17,25,5],			#smart Agent
        [7,16,12,6,3],			#Shopping Addict
        [3,48,39,2,4],			#other
        ]

old_offers, gama = Market(my_agents)
print my_preferences[0][1]

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
print gama

#graphing smart agents utility 
for i in range(len(my_agents)):
	A[i], = plt.plot(agentU[i][:], label = agent_names[i]) 
	plt.title('smart agents utility')
	plt.xlabel('time')
	plt.ylabel('utils')
plt.legend(handles = [A[0], A[1], A[2], A[3], A[4], A[5]])


for g in range(5):
        plt.figure('Utility vs. good')
        gmax = 100
        g0 = np.arange(0.0, gmax, 1.0)
        u0 = np.zeros_like(g0)
        agent_to_plot = 3
        for i in range(len(g0)):
                goods[agent_to_plot][:] = 0
                goods[agent_to_plot][g] = g0[i]
                u0[i] = Utility1(agent_to_plot, goods[agent_to_plot], 'a')

        plt.plot(g0, u0, label='$U(g_%d)$' % g)
        plt.legend(loc='best')
        plt.xlabel('amount of good')
        plt.ylabel('utility')

        plt.figure('Marginal utility')
        plt.plot(g0[1:], np.diff(u0), label=r'$\frac{\partial U}{\partial g_%d}$' % g)
        plt.xlabel('amount of good %d' % g)
        plt.legend(loc='best')
        plt.ylabel(r'marginal utility $\frac{\partial U}{\partial g_i}$')

plt.show()


# ~ a0, = plt.plot(agentU[0][:],label = agent_names[0]) 
# ~ a1, = plt.plot(agentU[1][:],label = 'Picky Agent') 
# ~ a2, = plt.plot(agentU[2][:],label = 'Stubborn Seller') 
# ~ a3, = plt.plot(agentU[3][:],label = 'Smart Agent') 
# ~ a4, = plt.plot(agentU[4][:],label = 'Shopping Addict') 
# ~ a5, = plt.plot(agentU[5][:],label = 'Other') 
# ~ plt.title('Utility')
# ~ plt.xlabel('time')
# ~ plt.ylabel('utils')
# ~ plt.legend(handles=[a0, a1, a2, a3, a4, a5])
# ~ plt.show()

#~ #creating utility function depending on calories
#~ plt.figure()
#~ Q = np.arange(0.0, 5000.0, 0.5)
#~ utility_Calories = 100*(Q / Q0) / ((Q / Q0) + 1) 
#~ #creating utility function for goods 1-5
#~ g = np.arange(0.0, 50, 1)
#~ g0 = 5
#~ g1 = 7
#~ g2 = 9
#~ g3 = 11
#~ g4 = 13
#~ #smart Agents Utility
#~ utility_g0 = 100*(g/g0)/((g/g0)**2+1)
#~ utility_g1 = 100*(g/g1)/((g/g1)**2+1)
#~ utility_g2 = 100*(g/g2)/((g/g2)**2+1)
#~ utility_g3 = 100*(g/g3)/((g/g3)**2+1)
#~ utility_g4 = 100*(g/g4)/((g/g4)**2+1)
#~ plt.plot(g,utility_g0, label='good 0')
#~ plt.plot(g,utility_g1, label='good 1')
#~ plt.plot(g,utility_g2, label='good 2')
#~ plt.plot(g,utility_g3, label='good 3')
#~ plt.plot(g,utility_g4, label='good 4')
#~ plt.legend()
#~ plt.title('Utility as a Function of goods')
#~ plt.xlabel('Quantity of good')
#~ plt.ylabel('Utils')

#~ #graphing Calorie Utility
#~ plt.figure()
#~ plt.plot(Q,utility_Calories)
#~ plt.title('Utility as a Function of Calories')
#~ plt.xlabel('Calories')
#~ plt.ylabel('Utils')








#~ plt.show()
