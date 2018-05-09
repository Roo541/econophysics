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

def Utility1(my_id, my_goods):
	#Agent 1 Utility update
	utility_A1 = np.zeros((1,100))
	utility_Calories = 0
	g = np.arange(0.0, 750, 0.5)	
	utilityNew1 =0
	j = 0
	if my_id == 0 or my_id == 1 or my_id == 2 or my_id == 4:
		g0 = randint(25,50)
		g1 = 15
		g2 = 15
		g3 = 15
		g4 = randint(25,50)

	if my_id == 3:
	    g0 = randint(10,20)
	    g1 = 1
	    g2 = randint(10,20)
	    g3 = randint(10,20)
	    g4 = 1
	if my_id == 5:
		g0 = randint(1,20)
		g1 = randint(1,20)
		g2 = randint(1,20)
		g3 = randint(1,20)
		g4 = randint(1,20)

	#Calculates utility value at given point in time
	utility_g0 = 100*(my_goods[0]/g0)/((my_goods[0]/g0)**2+1)
	utility_g1 = 100*(my_goods[1]/g1)/((my_goods[1]/g1)**2+1)
	utility_g2 = 100*(my_goods[2]/g2)/((my_goods[2]/g2)**2+1)
	utility_g3 = 100*(my_goods[3]/g3)/((my_goods[3]/g3)**2+1)
	utility_g4 = 100*(my_goods[4]/g4)/((my_goods[4]/g4)**2+1)

	# ~ for i in range(len(my_goods)):
		# ~ utility_Calories = utility_Calories + 100*(my_goods[i]*Calories[i][0]/Q0)/(my_goods[i]*Calories[i][0]/Q0+1)

	#ideal Utility per good
	Ideal_g0 = 100*(g0/g0)/((g0/g0)**2+1)
	Ideal_g1 = 100*(g1/g1)/((g1/g1)**2+1)
	Ideal_g2 = 100*(g2/g2)/((g2/g2)**2+1)
	Ideal_g3 = 100*(g3/g3)/((g3/g3)**2+1)
	Ideal_g4 = 100*(g4/g4)/((g4/g4)**2+1)

	#Instantaneous utility for Agent 1 
	utility_A1 = utility_g0 + utility_g1 + utility_g2 + utility_g3 + utility_g4 
        return utility_A1

# TODO
#
# 1. Try to make smart_agent buy and sell (monetary_desperation = mu?) no MU but he now sells stuff too
#
# 2. Possibly make a different utility function (simpler?).  Or make		works with my_id but not simpler
#    the utility function work with different preferences based on my_id.
#
# 3. Create utility vs. time plots for everyone? All on same plot with legend? check
#
# 4. Create utility vs. goods plots, having it use Utility1 itself to compute values.
def update(my_id):
        U = my_utilities[my_id]
        update = U(my_id, goods[my_id])
        return update
def compare (my_id):
        choice = 'none'
        price = 0
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
                        price = randint(1,10)
                        good = i
	for i in range(5):
                possible_goods = 1*goods[my_id]
                possible_goods[i] -= 1
                AskingU = U(my_id, possible_goods)
                if AskingU > Org and AskingU > A:
                        A = AskingU
                        choice1 = 'ask'
                        price1 = randint(1,10)
                        good1 = i
	print "Smart Agent Utility if Bid:", B
	print "Smart Agent Utility if Ask:", A
	if  A > B:
	    choice = 'ask'
	    price = price1
	    good = good1
	return choice, price, good

def shufflerange(n):
        return random.sample(range(n), k=n)
        
def other(my_id, offers, old_offers, old_transactions):
        choice, my_price, good = compare(my_id)
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

def smart_agent(my_id, offers, old_offers, old_transactions):
        choice, my_price, good = compare(my_id)
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

def stubborn_seller(my_id, offers, old_offers, old_transactions):
        goodnum = randint(0,4)
        for i in range(20):
                if goods[my_id][goodnum] == 0:
                        goodnum = randint(0,4)
	Ask0 = random.randint(1,10)
	return 'ask', Ask0, goodnum

def stubborn_buyer(my_id, offers, old_offers, old_transactions):
	price = randint(1,10)
	good = randint(0,4)
	#choice, good = Utility0 
	return 'bid', price, good

#Only Buys good 0 and Sells good 4
def picky_agent(my_id, offers, old_offers, old_transactions):
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
def shopping_addict(my_id, offers, old_offers, old_transactions):
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
                #smartU[t] = update(3)
                #~ otherU[t] = update(5)
                print 'offers are', offers
                print 'IT IS NOW ROUND', t
                for i in shufflerange(len(agents)):
                        #the following sends agent i his own id and returns: choice, price, good
                        agentU[i][t] = update(i)
                        choice, price, good = agents[i](i, offers, old_offers, old_transactions)
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
                                                                break
                        else:
                                print '   *** ', agent_names[i], i, 'makes no offer'

	        # A0,gRand = Agent0()			#Updates Utility and makes Trade proposals
	        # B1 = Agent1(A0)
	        # Market(A0, B1, gRand)				#Makes Trades and Updates goods and bank account
	        t = t + 1
                old_offers.append(copy.copy(offers))
        return t

               

agent_names = ["stubborn_buyer", "picky_agent", "stubborn_seller", "smart_agent", "shopping_addict", "other"]
my_agents = [stubborn_buyer, picky_agent, stubborn_seller, smart_agent, shopping_addict, other]
my_utilities = [Utility1, Utility1, Utility1, Utility1, Utility1, Utility1]
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
print A
#graphing smart agents utility 
for i in range(len(my_agents)):
	A[i], = plt.plot(agentU[i][:], label = agent_names[i]) 
	plt.title('smart agents utility')
	plt.xlabel('time')
	plt.ylabel('utils')
plt.legend(handles = [A[0], A[1], A[2], A[3], A[4], A[5]])
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
