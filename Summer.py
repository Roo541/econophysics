import numpy as np
from random import randint
import random
import matplotlib.pyplot as plt
import copy
import math

#global stuff
agents = 15
Numgoods = 5
goods = np.zeros((agents,Numgoods))
Calories = np.zeros((Numgoods,1))
Bank_Account = np.zeros((agents))
box = np.zeros((Numgoods, 3))
Q0 = 500 #minimum calories needed
smartU = np.zeros(100)
agentU = np.zeros((6, 100))
aSavings = [2000,2000,2000,2000,2000,2000]
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

def Utility1(my_id, my_goods):
	#Agent 1 Utility update
	utility_A1 = np.zeros((1,100))	
	for i in range(Numgoods):
		utility_g[i] = my_preferences[my_id][i]*(my_goods[i]/my_preferences[my_id][i]/np.sqrt((my_goods[i]/my_preferences[my_id][i])**2+1))
		#utility_s[my_id] = aSavings[my_id]*(Bank_Account[my_id]/aSavings[my_id]/np.sqrt((Bank_Account[my_id]/aSavings[my_id])**2+1))

	#Instantaneous utility for Agent 1 
	utility_A1 = utility_g[0] + utility_g[1] + utility_g[2] + utility_g[3] + utility_g[4] #+ .01*utility_s[my_id]
        return utility_A1

# TODO
#
# 1. Try to make smart_agent use offers and prices to buy and sell
#    (monetary_desperation = mu?).
#
# 2. Make utility function use arrays as inputs, maybe also have different asymptotes. Check

#Make other agent only buy and sell what is offered

def update(my_id):
        U = my_utilities[my_id]
        update = U(my_id, goods[my_id])
        return update

def send(price,good):				#Gives a reasonable price for good based on past transactions
	if box[good][randint(0,1)] == 0:
		box[good][randint(0,1)] = price
	if box[good][randint(0,1)] != 0:
		box[good][randint(0,1)] = price
	box[good][2] = math.ceil((box[good][0]+box[good][1])/2)
	reasonable_price = box[good][2]
	return reasonable_price

def shufflerange(n):
        return random.sample(range(n), k=n)

def smart_agent(my_id, offers, old_offers, old_transactions, my_preferences):
        # ~ choice, my_price, good = compare(my_id)
        choice = 'none'
        my_price = 0
        good = 0
        B = 0
        A = 0
        U = my_utilities[my_id]
        Org = U(my_id, goods[my_id]) 
        print "Orginal Utility is ", Org
	for i in range(5):
                possible_goods =1*goods[my_id]
                possible_goods[i] += 1
                BuyingU = U(my_id, possible_goods)
                if BuyingU > Org and BuyingU > B:
                        B = BuyingU
                        choice = 'bid'
                        my_price = box[good][2]			#Must use a relevant price for my bid
                        good = i
	for i in range(5):
                possible_goods = 1*goods[my_id]
                possible_goods[i] -= 1
                AskingU = U(my_id, possible_goods)
                if AskingU > Org and AskingU > A:
                        A = AskingU
			print '**************************************************************************************************'
                        choice1 = 'ask'
                        price1 = box[good][2]				#Must use relevant price for my ask
                        good1 = i
	print "Smart Agent Utility if Bid:", B
	print "Smart Agent Utility if Ask:", A
	if  A < B:
	    choice = 'bid'
            print 'compare is recommending an bid'
        for i in range(len(offers)):				#Going through offers and setting them to their_good place holder
                their_good = offers[i][2]
                their_price = offers[i][1]
		if i != my_id and choice == 'bid' and offers[i][0] == 'ask' and their_good == good and their_price <= my_price:
                        return 'bid', their_price, good
		
        return choice, my_price, good
	if  A > B:
	    choice = 'ask'
	    my_price = price1
	    good = good1
            print 'compare is recommending an ask'
        for i in range(len(offers)):				#Going through offers and setting them to their_good place holder
                their_good = offers[i][2]
                their_price = offers[i][1]
		if i != my_id and choice == 'ask' and offers[i][0] == 'bid' and their_good == good and their_price >= my_price:
                        return 'ask', their_price, good
		
        return choice, my_price, good
#only makes or takes existing offers       
def other(my_id, offers, old_offers, old_transactions, my_preferences):
        # ~ choice, my_price, good = compare(my_id)
        choice = 'none'
        my_price = 0
        good = 0
        BuyingU = 0
        AskingU = 0
	B = 0
        A = 0
        U = my_utilities[my_id]
        Org = U(my_id, goods[my_id]) 
        print "Orginal Utility is ", Org
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
				choice = 'ask'
				my_price = b
				good = c
	return choice, my_price, good
	# ~ for i in range(5):
                # ~ possible_goods =1*goods[my_id]
                # ~ possible_goods[i] += 1
                # ~ BuyingU = U(my_id, possible_goods)
                # ~ if BuyingU > Org and BuyingU > B:
                        # ~ B = BuyingU
                        # ~ choice = 'bid'
                        # ~ my_price = box[good][2]			#Must use a relevant price for my bid
                        # ~ good = i
	# ~ for i in range(5):
                # ~ possible_goods = 1*goods[my_id]
                # ~ possible_goods[i] -= 1
                # ~ AskingU = U(my_id, possible_goods)
                # ~ if AskingU > Org and AskingU > A:
                        # ~ A = AskingU
                        # ~ choice1 = 'ask'
                        # ~ price1 = box[good][2]				#Must use relevant price for my ask
                        # ~ good1 = i		                  

	# ~ print "Other Agent Utility if Bid:", B
	# ~ print "Other Agent Utility if Ask:", A
	# ~ if  A < B:
	    # ~ choice = 'bid'
            # ~ print 'compare is recommending an bid'
        # ~ for i in range(len(offers)):
                # ~ their_good = offers[i][2]
                # ~ their_price = offers[i][1]
		# ~ if i != my_id and choice == 'bid' and offers[i][0] == 'ask' and their_good == good and their_price <= my_price:		    
                        # ~ return 'bid', their_price, good
        # ~ for i in range(len(offers)):
                # ~ their_good = offers[i][2]
                # ~ their_price = offers[i][1]
		# ~ if i != my_id and choice == 'ask' and offers[i][0] == 'bid' and their_good == good and their_price >= my_price:		    
                        # ~ return 'ask', their_price, good
        # ~ return choice, my_price, good

def stubborn_seller(my_id, offers, old_offers, old_transactions, my_preferences):
        goodnum = randint(0,4)
        for i in range(20):
                if goods[my_id][goodnum] == 0:
                        goodnum = randint(0,4)
	Ask0 = random.randint(1,10)
	return 'ask', Ask0, goodnum

def stubborn_buyer(my_id, offers, old_offers, old_transactions, my_preferences):
	good = randint(0,4)
	price = box[good][2]
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
        old_transactions = []
        offers = [('none',0,0)]*len(agents)
        while t < 100:
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
                                                                #~ old_offers[i] = offers[j]
                                                                old_transactions.append((price,good))
                                                                offers[i] = ('none',0,0)
                                                                offers[j] = ('none',0,0)
								send(price,good)
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
                                                                old_transactions.append((price,good))
                                                                offers[i] = ('none',0,0)
                                                                offers[j] = ('none',0,0)
								send(price,good)
                                                                break
                        else:
                                print '   *** ', agent_names[i], i, 'makes no offer'

	       
	        t = t + 1
                old_offers.append(copy.copy(offers))
        return t

               

agent_names = ["stubborn_buyer", "picky_agent", "stubborn_seller", "smart_agent", "shopping_addict", "other"]
my_agents = [stubborn_buyer, picky_agent, stubborn_seller, smart_agent, shopping_addict, other]
my_utilities = [Utility1, Utility1, Utility1, Utility1, Utility1, Utility1]
my_preferences = [
        [3,7,15,4,25],
        [3,16,19,2,40],
        [7,8,35,5,20],			#stubborn Seller
        [1,3,7,2,4],		#smart Agent
        [7,16,12,6,3],			#Shopping Addict
        [4,4,3,2,4],			#other
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
        gmax = 100
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

plt.show()
print box








