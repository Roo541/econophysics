import numpy as np
from random import randint
import random
import matplotlib.pyplot as plt
import copy
import math

#global stuff
max_agents = 15
Numgoods = 5
goods = np.zeros((max_agents,Numgoods))
Bank_Account = np.zeros((max_agents))
box = np.zeros((Numgoods, 3))
box[:][:] = 10
utility_g = np.zeros(len(goods))

def Utility1(my_id, my_goods):
	value = Bank_Account[my_id]
	#Agent Utility update
        U = 0
	for i in range(Numgoods):
		U += my_preferences[my_id][i]*(my_goods[i]/my_preferences[my_id][i]/np.sqrt((my_goods[i]/my_preferences[my_id][i])**2+1))
	return U

my_utilities = max_agents*[Utility1]

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

def highest_recent_bid(good, old_offers):
        highest_bid = 0
        for offers in old_offers[-3*Numgoods:]:
                for offer in offers:
                        if offer[0] == 'bid' and offer[2] == good:
                                highest_bid = max(highest_bid, offer[1])
        return highest_bid

def lowest_recent_ask(good, old_offers):
        lowest_ask = 1e12
        for offers in old_offers[-3*Numgoods:]:
                for offer in offers:
                        if offer[0] == 'ask' and offer[2] == good:
                                lowest_ask = min(lowest_ask, offer[1])
        return lowest_ask

def random_good():
        return randint(0,Numgoods-1)

def intelligent_agent(my_id, offers, old_offers, old_transactions, my_preferences, t):
        offers = 1*offers
        offers[my_id] = ('none', 0, 0) # just to avoid accidentally responding to myself.
	U = my_utilities[my_id]
	Org = U(my_id, goods[my_id])
        richest = 0
        for i in range(len(Bank_Account)):
                if i != my_id:
                        richest = max(richest, Bank_Account[i])
	Mu = 0
	for g in range(Numgoods):
		possible_goods = 1*goods[my_id]
		possible_goods[g] += 1
		marginalU = U(my_id, possible_goods) - Org
                lowest_ask = lowest_recent_ask(g, old_offers+[offers])
		Mu = max(Mu, marginalU/(2.0*lowest_ask)) # devalue money a factor of two
	# Go through existing offers to see whether anyone is selling
	# and at what prices:
        highest_price = 0
	for what, price, good in offers:
		if what == 'ask':
                        highest_price = max(highest_price, price)
        if highest_price < Bank_Account[my_id]/10:
                # Everything is a bargain, so buy whatever we like
                # most, without regard to price!
                best_buy = 0
                best_price = 0
                best_good = 0
	        for what, price, good in offers:
		        if what == 'ask':
			        possible_goods = 1*goods[my_id]
			        possible_goods[good] += 1
			        BuyingU = U(my_id, possible_goods)
                                if BuyingU > best_buy:
                                        best_buy = BuyingU
                                        best_price = price
                                        best_good = good
                if best_buy > 0:
                        return 'bid', best_price, best_good
	# Looks like we might be running short on cash, so we should
	# consider selling. Go through existing offers to see what is
	# best.
        best_deal = 0
        best_choice = 'none'
        best_price = 0
        best_good = 0
	for what, price, good in offers:
		if what == 'ask' and price < Bank_Account[my_id]:
			possible_goods = 1*goods[my_id]
			possible_goods[good] += 1
			BuyingU = U(my_id, possible_goods) - price*Mu
			if BuyingU > best_deal:
				best_deal = BuyingU
				best_choice = 'bid'
				best_price = price
				best_good = good
		if what == 'bid' and goods[my_id][good] > 0:
			possible_goods = 1*goods[my_id]
			possible_goods[good] -= 1
			AskingU = U(my_id, possible_goods) + price*Mu
			if AskingU > best_deal:
				best_deal = AskingU
				best_choice = 'ask'
				best_price = price
				best_good = good
	if best_deal > Org:
		return best_choice, best_price, best_good
        # Let's see about making a bid!
        best_deal = Org
        for g in shufflerange(Numgoods):
	        # FUTURE: only want to bid on goods others have.
	        # FUTURE: possibly use historical prices to guess what people will want to sell.
		possible_goods =1*goods[my_id]
		possible_goods[g] += 1
		break_even_price = (U(my_id, possible_goods) - best_deal)/Mu
                lowest_ask = lowest_recent_ask(g, old_offers+[offers])
                highest_bid = highest_recent_bid(g, old_offers+[offers])
                if lowest_ask < break_even_price and lowest_ask < Bank_Account[my_id]:
                        # If someone has been offering a good deal
                        # recently (but not this turn) see if they are
                        # still willing!
                        return 'bid', lowest_ask, g
		if int(break_even_price-1) > 1 and highest_recent_bid < int(break_even_price-1) and Bank_Account[my_id] > break_even_price:
                        # pick a price that is higher than the most
                        # recent high bid, in hopes of attracting a
                        # seller.
		        price = randint(highest_bid, int(break_even_price-1))
                        if price > 0:
			        return 'bid', price, g
        # Looks like we can't even afford to make a decent bid, so
        # let's see if we can scrap together some money.
        for g in shufflerange(Numgoods):
	        if goods[my_id][g] > 0:
		        possible_goods = 1*goods[my_id]
		        possible_goods[g] -= 1
		        break_even_price = (Org - U(my_id, possible_goods))/Mu
                        lowest_ask = lowest_recent_ask(g, old_offers+[offers])
                        highest_bid = highest_recent_bid(g, old_offers+[offers])
                        if highest_bid > break_even_price:
                                # Someone has been recently asking for
                                # this good at a decent price, so
                                # let's see if they'll buy it again!
                                return 'ask', highest_bid, g
		        if break_even_price >= 1 and lowest_ask > break_even_price+1 and int(break_even_price)+1 < richest:
                                price = randint(int(break_even_price)+1, min(lowest_ask, richest))
			        return 'ask', price, g
        # This means that noone has been offering to sell *anything*
        # recently.  In this case we will need to decide what the
        # situation is.  Either we are at the beginning and we may
        # just need to get things started, or we are at the end and
        # everyone has all that they want of each good.  In either
        # case, let's just ask for most of the money that anyone has,
        # and let's just pick a random good to sell at this price.
        for g in shufflerange(Numgoods):
	        if goods[my_id][g] > 0:
                        price = randint(int(richest/2), richest)
                        if price < 1:
                                price = 1
			return 'ask', price, g
	return 'none',0,0


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
	for g in range(Numgoods):
		possible_goods = 1*goods[my_id]
		possible_goods[g] += 1
		marginalU = U(my_id, possible_goods) - Org
		Mu = max(Mu, marginalU/box[g][2])
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
	        #Look past previous few offers looking for a bargain
		high = 0
		low = 1000000
		for item in old_offers[t-3:]:
			for a,b,c in item:
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
	if True:  #Offers that don't beat original utility make a new bid or ask
		# Let's make a bid!
		i = random_good()
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
		if i != my_id and offers[i][0] == 'ask' and offers[i][1] <= Bank_Account[my_id]:
                        return 'bid', offers[i][1], offers[i][2] 	#shopping addict just returns a. Wants to buy anything
	# ~ print "  &&&&&   NOTHING TO BUY, I'm SO SAD!"
	return 0,0,0

def Market(agent_names, tmax):
        agents = [agent_by_name[name] for name in agent_names]
        agentU = np.zeros((10, tmax))
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
								#print 'We MATCH!!!'
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
								#print 'We MATCH!!!'
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
	return t, old_offers, agentU

agent_by_name = {
	"IQ": IQ,
        "intelligent_agent": intelligent_agent,
        "ia": intelligent_agent,
        "S3": Smart_Agent_3,
        "shopping_addict": shopping_addict,
        "stubborn_seller": stubborn_seller,
}
