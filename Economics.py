import numpy as np
from random import randint
import matplotlib.pyplot as plt

#global stuff
agents = 15
goods = 5
goods_index = np.zeros((agents,goods))
Calories_index = np.zeros((goods,1))
Bank_Account = np.zeros((agents,1))
Umax1 = 5
Q0 = 500 #minimum calories needed
ask = 5
bid = 5
for i in range(agents):
	for j in range(goods):
		goods_index[i][j]= 10
for i in range(goods):
	Calories_index[i][0] = 100
for i in range(agents):
	Bank_Account[i][0] = 1000
Ua1 = [0 for i in range (10)]
#creating utility function depending on calories
Q = np.arange(0.0, 5000.0, 0.5)
utility_Calories = 100*(Q / Q0) / ((Q / Q0) + 1) 
#creating utility function for goods 1-5
#~ g = np.arange(0.0, 750, 1)
#~ utility_g1 = 100*(g/5)/((g/5)**2+1)

def Agent_1():
	#Agent 1 Utility update
	utility_A1 = np.zeros((1,100))
	utility_Calories = 0
	g = np.arange(0.0, 750, 0.5)	
	j = 0
	g1 = 5							#specific good happiness for agent 1 
	g2 = 7
	g3 = 9
	g4 = 11
	g5 = 13
	while (j < 5):
		#Calculates utility value at given point in time
		utility_g1 = 100*(goods_index[0][0]/g1)/((goods_index[0][0]/g1)**2+1)
		utility_g2 = 100*(goods_index[0][1]/g2)/((goods_index[0][1]/g2)**2+1)
		utility_g3 = 100*(goods_index[0][2]/g3)/((goods_index[0][2]/g3)**2+1)
		utility_g4 = 100*(goods_index[0][3]/g4)/((goods_index[0][3]/g4)**2+1)
		utility_g5 = 100*(goods_index[0][4]/g5)/((goods_index[0][4]/g5)**2+1)

		for i in range(goods):
			utility_Calories = utility_Calories + 100*(goods_index[0][i]*Calories_index[i][0]/Q0)/(goods_index[0][i]*Calories_index[i][0]/Q0+1)

		#Instantaneous utility for Agent 1 
		utility_A1 = utility_g1 + utility_g2 + utility_g3 + utility_g4 + utility_g5 + utility_Calories
		Ua1[j] = utility_A1
		j = j+1
Agent_1()
#Finds last part in Utility function
for i in range(10):
	if Ua1[i] == 0 and Ua1[i-1] != 0:
		alpha = Ua1[i-1]
	else: i = i + 1
#Agent1 Buying Price
def Buy(bid):
	bid =1
	return bid
#Agent1 Selling price
def Sell(ask):
	ask = 1
	return ask
#market place
def MarketGood1(a):
	#Ask
	askingPrice = a 
	biddingPrice = 2
	if askingPrice == biddingPrice:
		print "sold"
	else:
		print "not sold"
	
#compares updated utility to maximum utility required	
if alpha < Umax1 :
	b = Buy(bid)
else:
	a = Sell(ask)
	
MarketGood1(a)




























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

