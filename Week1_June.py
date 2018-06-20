import numpy as np
from random import randint, expovariate
import random
import matplotlib.pyplot as plt
import copy

#global stuff
tmax = 1000
agents = 15
Numgoods = 5
goods = np.zeros((agents,Numgoods))
Bank_Account = np.zeros((agents))
smartU = np.zeros(tmax)
agentU = np.zeros((5, tmax))

#Filling out the arrays with initial values
for i in range(agents):
	for j in range(Numgoods):
		goods[i][j]= 10
for i in range(agents):
	Bank_Account[i] = 5000
utility_g = np.zeros(len(goods))

def Utility1(my_id, my_goods, other, Bank_Account):
	#Agent 1 Utility update
	a = Bank_Account
	utility_A1 = np.zeros((1,tmax))
	if other == 'a' :
	    for i in range(Numgoods):
		    utility_g[i] = my_preferences[my_id][i]*(my_goods[i]/my_preferences[my_id][i]/np.sqrt((my_goods[i]/my_preferences[my_id][i])**2+1))   
	if other == 1:
	    for i in range(Numgoods):
		    utility_g[i] = my_preferences[my_id][i]*(my_goods[i]/my_preferences[my_id][i]/np.sqrt((my_goods[i]/my_preferences[my_id][i])**2+1))
	#Instantaneous utility for Agent 1 
	utility_A1 = utility_g[0] + utility_g[1] + utility_g[2] + utility_g[3] + utility_g[4]  + np.log10(np.abs(a)+.1)
        return utility_A1

# TODO
#
# 1. Try to make smart_agent use offers and prices to buy and sell. check but still no monetary_desperation because I am confused
#    (monetary_desperation = mu?).
#
# 2. Make utility function use arrays as inputs, maybe also have different asymptotes. Check

def update(my_id):
        U = my_utilities[my_id]
        update = U(my_id, goods[my_id], 'a', Bank_Account[my_id])
        return update

def shufflerange(n):
        return random.sample(range(n), k=n)

def clever_agent(my_id, offers, old_offers, g0_transaction, g1_transaction, g2_transaction, g3_transaction, g4_transaction, my_preferences):
        # This is an agent that tries to be sell at times, when it
        # could help to make purchases later.
	choiceBestDeal = 0
	priceBestDeal = 0
	goodBestDeal =0
	choice = 'none'
	my_price = 0
	good = 0
	current_good = 0
	BidU = 0
	AskU = 0
	BestDeal = 0
	# ~ money_utility = 0.01 # this is in units of utility per dollar
	money_utility = 1000/(Bank_Account[my_id]+1)
	U = my_utilities[my_id]
	OriginalU = U(my_id, goods[my_id], 'a', Bank_Account[my_id])
	print "        Orginal Utility is ", OriginalU
	#existing Ask offers
	for i in range(len(offers)):
	    if offers[i][0] == 'ask':
                current_price = offers[i][1]
                if current_price <= Bank_Account[my_id]:
                    # We can ignore any asks that we can't even afford to buy
                    other = offers[i][2]
                    possible_goods =1*goods[my_id]
                    possible_goods[other] += 1
                    Current_Ask_U = U(my_id, possible_goods, 1, Bank_Account[my_id]) - current_price*money_utility
                    print "        buying from existing offers is", Current_Ask_U
		    if Current_Ask_U > OriginalU and Current_Ask_U > BestDeal:
			BestDeal = Current_Ask_U
			choiceBestDeal = 'bid'
			priceBestDeal = current_price
			goodBestDeal = other
	#existing Bid offers
	for i in range(len(offers)):
	    if offers[i][0] == 'bid':
                other = offers[i][2]
                current_price = offers[i][1]
                possible_goods =1*goods[my_id]
                possible_goods[other] -= 1
                Current_Bid_U = U(my_id, possible_goods, 1, Bank_Account[my_id]) + current_price*money_utility
                print "        selling to existing offers is", Current_Bid_U
		if Current_Bid_U > OriginalU and Current_Bid_U > BestDeal:
		    BestDeal = Current_Bid_U
		    choiceBestDeal = 'ask'
		    priceBestDeal = offers[i][1]
		    goodBestDeal = other
        if BestDeal > OriginalU:
	    print '         #### CLOSE THE DEAL!'
	    return choiceBestDeal, priceBestDeal, goodBestDeal
        # There is no deal that is worthwhile out there, so let's
        # randomly decide to either put out a bid or an ask.
        if Bank_Account[my_id] > 0 and randint(0,10) < 5:
                # Let's try putting out a bid for a random good.
                # Random good is better than the good we want most,
                # because maybe noone wants to sell the good we want
                # most, and we might be able to get our second-best
                # good.
                good = randint(0, Numgoods-1)
                possible_goods =1*goods[my_id]
                possible_goods[i] += 1
                BuyingU = U(my_id, possible_goods, 'a', Bank_Account[my_id])
                break_even_price = (BuyingU - OriginalU)/money_utility
                # We'll put out a bid that is some fraction of our
                # break_even_price.  How hard a bargain should we
                # drive? I have no clue.
                price = int(break_even_price / randint(2,5))
                if price >= 1 and price <= Bank_Account[my_id]:
                        return 'bid', price, good
                if price >= 1 and randint(1,1000) == 3 and Bank_Account[my_id] > 0: 
                        # Occasionally, if we can't afford the above
                        # bargain price, just try offering whatever
                        # we've got.
		        return 'bid', Bank_Account[my_id]/randint(5,10), good
        # We didn't decide to bid, so we'll have to make an ask.
        good = randint(0, Numgoods-1)
        possible_goods =1*goods[my_id]
        possible_goods[i] -= 1
        SellingU = U(my_id, possible_goods, 'a', Bank_Account[my_id])
        break_even_price = (OriginalU - SellingU)/money_utility
        if break_even_price > 0:
                # pick a price that is a random factor higher than our break-even price.
                return 'ask', int(break_even_price*(1+expovariate(2.0))), good
                
def Agent_1(my_id, offers, old_offers, g0_transaction, g1_transaction, g2_transaction, g3_transaction, g4_transaction, my_preferences):
        # ~ choice, my_price, good = compare(my_id)
	goodsAvgPrice = [np.ceil(np.mean(g0_transaction)),np.ceil(np.mean(g1_transaction)),np.ceil(np.mean(g2_transaction)),np.ceil(np.mean(g3_transaction)),np.ceil(np.mean(g4_transaction))]
	choiceBestDeal = 0
	priceBestDeal = 0
	goodBestDeal =0
	choice = 'none'
	my_price = 0
	price1 =0
	good = 0
	good1 = 0
	current_good = 0
	BidU = 0
	AskU = 0
	money_utility = 10/(Bank_Account[my_id]+1)
	BestDeal = 0
	U = my_utilities[my_id]
	OriginalU = U(my_id, goods[my_id], 'a', Bank_Account[my_id])
	#existing Ask offers
	for i in range(len(offers)):
	    if offers[i][0] == 'ask':
		other = offers[i][2]
		current_price = offers[i][1]
		possible_goods =1*goods[my_id]
                possible_goods[other] += 1
		Current_Ask_U = U(my_id, possible_goods, 1, Bank_Account[my_id])- current_price*money_utility
		print "buying from existing Ask offers is", Current_Ask_U
		if Current_Ask_U > OriginalU and Current_Ask_U > BestDeal and offers[i][1] <= Bank_Account[my_id]:
		    BestDeal = Current_Ask_U
		    choiceBestDeal = 'bid'
		    priceBestDeal = offers[i][1]
		    priceBestDeal = goodsAvgPrice[other]
		    goodBestDeal = other
	#existing Bid offers
	for i in range(len(offers)):
	    if offers[i][0] == 'bid':
		other = offers[i][2]
		current_price = offers[i][1]
		possible_goods =1*goods[my_id]
                possible_goods[other] -= 1
		Current_Bid_U = U(my_id, possible_goods, 1, Bank_Account[my_id]) + current_price*money_utility
		print "Selling from existing Bid offers is", Current_Bid_U
		if Current_Bid_U > OriginalU and Current_Bid_U > BestDeal:
		    BestDeal = Current_Bid_U
		    choiceBestDeal = 'ask'
		    priceBestDeal = goodsAvgPrice[other]
		    goodBestDeal = other
    #ideal Buying 
	for i in range(len(offers)):
                possible_goods =1*goods[my_id]
                possible_goods[i] += 1
                BuyingU = U(my_id, possible_goods, 'a', Bank_Account[my_id]) 
                if BuyingU > OriginalU and BuyingU > BidU and Bank_Account[my_id] > 0:
                        BidU = BuyingU
                        my_priceB = goodsAvgPrice[i]
                        goodB = i
    #ideal Selling
	for i in range(len(offers)):
                possible_goods = 1*goods[my_id]
                possible_goods[i] -= 1
                AskingU = U(my_id, possible_goods, 'a', Bank_Account[my_id])
                if AskingU > AskU:
                        AskU = AskingU
                        choice1 = 'ask'
                        price1 = goodsAvgPrice[i]
                        good1 = i
	print "Smart Agent Utility if Bid:", BidU
	print "Smart Agent Utility if Ask:", AskU
        # Let's default to accepting any offer that seems to benefit
        # us.  Yes, we might do better by holding out for something
        # even more lucrative, but someone else might also snap up
        # this offer.
	if BestDeal > OriginalU:
		print '         #### CLOSE THE DEAL!'
		return choiceBestDeal, priceBestDeal, goodBestDeal
	elif BidU > AskU:
		print 'bid utility: ', BidU
		return 'bid', my_priceB, goodB
	else:
		return 'ask', price1, good1
	return 'none', 0, 0
#another smart agent
def Agent_2(my_id, offers, old_offers, g0_transaction, g1_transaction, g2_transaction, g3_transaction, g4_transaction, my_preferences):
        # ~ choice, my_price, good = compare(my_id)
	goodsAvgPrice = [np.ceil(np.mean(g0_transaction)),np.ceil(np.mean(g1_transaction)),np.ceil(np.mean(g2_transaction)),np.ceil(np.mean(g3_transaction)),np.ceil(np.mean(g4_transaction))]
	choiceBestDeal = 0
	priceBestDeal = 0
	goodBestDeal =0
	choice = 'none'
	my_price = 0
	price1 = 0
	good1 = 0
	good = 0
	current_good = 0
	BidU = 0
	AskU = 0
	money_utility = 10/(Bank_Account[my_id]+100)
	BestDeal = 0
	U = my_utilities[my_id]
	OriginalU = U(my_id, goods[my_id], 'a', Bank_Account[my_id])
	#existing Ask offers
	for i in range(len(offers)):
	    if offers[i][0] == 'ask':
		other = offers[i][2]
		current_price = offers[i][1]
		possible_goods =1*goods[my_id]
                possible_goods[other] += 1
		Current_Ask_U = U(my_id, possible_goods, 1, Bank_Account[my_id])- current_price*money_utility
		print "buying from existing Ask offers is", Current_Ask_U
		if Current_Ask_U > OriginalU and Current_Ask_U > BestDeal and offers[i][1] <= Bank_Account[my_id]:
		    BestDeal = Current_Ask_U
		    choiceBestDeal = 'bid'
		    priceBestDeal = goodsAvgPrice[other]
		    goodBestDeal = other
	#existing Bid offers
	for i in range(len(offers)):
	    if offers[i][0] == 'bid':
		other = offers[i][2]
		current_price = offers[i][1]
		possible_goods =1*goods[my_id]
                possible_goods[other] -= 1
		Current_Bid_U = U(my_id, possible_goods, 1, Bank_Account[my_id]) + current_price*money_utility
		print "Selling from existing Bid offers is", Current_Bid_U
		if Current_Bid_U > OriginalU and Current_Bid_U > BestDeal:
		    BestDeal = Current_Bid_U
		    choiceBestDeal = 'ask'
		    priceBestDeal = goodsAvgPrice[other]
		    goodBestDeal = other
    #ideal Buying 
	for i in range(len(offers)):
                possible_goods =1*goods[my_id]
                possible_goods[i] += 1
                BuyingU = U(my_id, possible_goods, 'a', Bank_Account[my_id]) 
                if BuyingU > OriginalU and BuyingU > BidU and Bank_Account[my_id] > 0:
                        BidU = BuyingU
                        my_priceB = goodsAvgPrice[i]
                        goodB = i
    #ideal Selling
	for i in range(len(offers)):
                possible_goods = 1*goods[my_id]
                possible_goods[i] -= 1
                AskingU = U(my_id, possible_goods, 'a', Bank_Account[my_id])
                if AskingU > AskU:
                        AskU = AskingU
                        choice1 = 'ask'
                        price1 = goodsAvgPrice[i]
                        good1 = i
	print "Smart Agent Utility if Bid:", BidU
	print "Smart Agent Utility if Ask:", AskU
        # Let's default to accepting any offer that seems to benefit
        # us.  Yes, we might do better by holding out for something
        # even more lucrative, but someone else might also snap up
        # this offer.
	if BestDeal > OriginalU:
            print '         #### CLOSE THE DEAL!'
            return choiceBestDeal, priceBestDeal, goodBestDeal
	if BidU > AskU:
            print 'bid utility: ', BidU
            return 'bid', my_priceB, goodB
	else:
            return 'ask', price1, good1
	return 'none', 0, 0
#Second Smart Agent
def Agent_3(my_id, offers, old_offers, g0_transaction, g1_transaction, g2_transaction, g3_transaction, g4_transaction, my_preferences):
        # ~ choice, my_price, good = compare(my_id)
        choiceBestDeal = 0
        priceBestDeal = 0
        goodBestDeal =0
        choice = 'none'
        my_price = 0
        good = 0
	current_good = 0
        BidU = 0
        AskU = 0
        money_utility = 1000/(Bank_Account[my_id]+1)
	BestDeal = 0
        U = my_utilities[my_id]
        OriginalU = U(my_id, goods[my_id], 'a', Bank_Account[my_id])
        print "Orginal Utility is ", OriginalU
	#existing Ask offers
	for i in range(len(offers)):
	    if offers[i][0] == 'ask':
		other = offers[i][2]
		current_price = offers[i][1]
		possible_goods =1*goods[my_id]
                possible_goods[other] += 1
		Current_Ask_U = U(my_id, possible_goods, 1, Bank_Account[my_id])- current_price*money_utility
		print "buying from existing Ask offers is", Current_Ask_U
		if Current_Ask_U > OriginalU and Current_Ask_U > BestDeal and offers[i][1] <= Bank_Account[my_id]:
		    BestDeal = Current_Ask_U
		    choiceBestDeal = 'bid'
		    priceBestDeal = offers[i][1]
		    goodBestDeal = other
	#existing Bid offers
	for i in range(len(offers)):
	    if offers[i][0] == 'bid':
		other = offers[i][2]
		current_price = offers[i][1]
		possible_goods =1*goods[my_id]
                possible_goods[other] -= 1
		Current_Bid_U = U(my_id, possible_goods, 1, Bank_Account[my_id]) + current_price*money_utility
		print "Selling from existing Bid offers is", Current_Bid_U
		if Current_Bid_U > OriginalU and Current_Bid_U > BestDeal:
		    BestDeal = Current_Bid_U
		    choiceBestDeal = 'ask'
		    priceBestDeal = offers[i][1]
		    goodBestDeal = other
	for i in range(len(offers)):
                possible_goods =1*goods[my_id]
                possible_goods[i] += 1
                BuyingU = U(my_id, possible_goods, 'a', Bank_Account[my_id]) 
                if BuyingU > OriginalU and BuyingU > BidU and Bank_Account[my_id] > 0:
                        BidU = BuyingU
                        my_priceB = randint(1,Bank_Account[my_id])
                        goodB = i
	for i in range(len(offers)):
                possible_goods = 1*goods[my_id]
                possible_goods[i] -= 1
                AskingU = U(my_id, possible_goods, 'a', Bank_Account[my_id])
                if AskingU > AskU:
                        AskU = AskingU
                        choice1 = 'ask'
                        price1 = randint(1,10)
                        good1 = i
	print "Smart Agent Utility if Bid:", BidU
	print "Smart Agent Utility if Ask:", AskU
        # Let's default to accepting any offer that seems to benefit
        # us.  Yes, we might do better by holding out for something
        # even more lucrative, but someone else might also snap up
        # this offer.
	if BestDeal > OriginalU:
            print '         #### CLOSE THE DEAL!'
            return choiceBestDeal, priceBestDeal, goodBestDeal
	elif BidU > AskU:
            print 'bid utility: ', BidU
            return 'bid', my_priceB, goodB
	else:
            return 'ask', price1, good1
        return 'none', 0, 0

#Shopping addict
def Agent_4(my_id, offers, old_offers, g0_transaction, g1_transaction, g2_transaction, g3_transaction, g4_transaction, my_preferences):
        for i in range(len(offers)):
		if i != my_id and offers[i][0] == 'ask':
			return 'bid', offers[i][1], offers[i][2] 	#shopping addict just returns a. Wants to buy anything
        print "     NOTHING TO BUY, I'm SO SAD!", offers
	return 0,0,0

def Market(agents):
        t = 0
        old_offers = []
        g0_transaction = []
        g1_transaction = []
        g2_transaction = []
        g3_transaction = []
        g4_transaction = []        
        old_transaction = []
        current_offers = [0,0,0,0,0]
        offers = [('none',0,0)]*len(agents)
        while t < tmax:
                print 'offers are', offers
                print 'IT IS NOW ROUND', t
                for i in shufflerange(len(agents)):
                        #the following sends agent i his own id and returns: choice, price, good
                        agentU[i][t] = update(i)				#updates each agents utility
                        choice, price, good = agents[i](i, offers, old_offers, g0_transaction, g1_transaction, g2_transaction, g3_transaction, g4_transaction, my_preferences)                
                        offers[i] = (choice, price, good)											#starts with agent0
                        if choice == 'ask':
                                print '   *** ', agent_names[i], i, 'asks',  np.ceil(price), 'for good', good
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
                                                                if good == 0:
									g0_transaction.append(price)
								elif good == 1:
									g1_transaction.append(price)
								elif good == 2:
									g2_transaction.append(price)
								elif good == 3:
									g3_transaction.append(price)
								elif good == 4:
									g4_transaction.append(price)
								break
                        elif choice == 'bid':
                                print '   *** ', agent_names[i], i, 'bids ',  np.ceil(price), 'for good', good
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
								if good == 0:
									g0_transaction.append(price)
								elif good == 1:
									g1_transaction.append(price)
								elif good == 2:
									g2_transaction.append(price)
								elif good == 3:
									g3_transaction.append(price)
								elif good == 4:
									g4_transaction.append(price)
								break
                        else:
                                print '   *** ', agent_names[i], i, 'makes no offer'

	        # A0,gRand = Agent0()			#Updates Utility and makes Trade proposals
	        # B1 = Agent1(A0)
	        # Market(A0, B1, gRand)				#Makes Trades and Updates goods and bank account
	        t = t + 1
                old_offers.append(copy.copy(offers))
		print np.mean(g0_transaction), np.mean(g1_transaction), np.mean(g2_transaction),np.mean(g3_transaction),np.mean(g4_transaction)
        return t, old_transaction, offers

               

agent_names = [ "clever_agent", "Agent_1", "Agent_2", "Agent_3", "Agent_4"]
my_agents = [clever_agent, Agent_1, Agent_2, Agent_3, Agent_4 ]
my_utilities = [Utility1, Utility1, Utility1, Utility1, Utility1]
my_preferences = [
        [150, 200, 19,  20, 40], # clever agent
        [ 10, 10, 17, 25,  5], #Agent_1
        [  7, 160, 120,  6,  3], #Agent_2
        [50, 30, 700, 25, 50],  #Agent_3
	[7, 20, 35, 150, 300]	#Agent_4
        ]

old_offers, gama, dummy = Market(my_agents)
# ~ print my_preferences[0][1]

for i in range(len(my_agents)):
        print '  -- ', goods[i], agent_names[i], i
print Bank_Account[:len(my_agents)]
a0 = 0
a1 = 0
a2= 0
a3 = 0
a4 = 0

A = [a0, a1, a2, a3, a4]
# ~ print gama

#graphing agents utility 
for i in range(len(my_agents)):
	A[i], = plt.plot(agentU[i][:], label = agent_names[i]) 
	plt.title('agents utility')
	plt.xlabel('time')
	plt.ylabel('utils')
plt.legend(handles = [A[0], A[1], A[2], A[3], A[4]])


for g in range(Numgoods):
        plt.figure('Utility vs. good')
        gmax = tmax
        g0 = np.arange(0.0, gmax, 1.0)
        u0 = np.zeros_like(g0)
        agent_to_plot = 0
        for i in range(len(g0)):
                goods[agent_to_plot][:] = 0
                goods[agent_to_plot][g] = g0[i]
                u0[i] = Utility1(agent_to_plot, goods[agent_to_plot], 'a', Bank_Account[agent_to_plot])

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


