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
Umax2 = 50000
Q0 = 500 #minimum calories needed
alpha1 = 10000
alpha2 = 1
#Filling out the arrays with initial values
for i in range(agents):
	for j in range(goods):
		goods_index[i][j]= 10
for i in range(goods):
	Calories_index[i][0] = 100
for i in range(agents):
	Bank_Account[i][0] = 1000
Ua1 = [0 for i in range (10)]
Ua2 = [0 for i in range (10)]

def Utility1():
	#Agent 1 Utility update
	utility_A1 = np.zeros((1,100))
	utility_Calories = 0
	g = np.arange(0.0, 750, 0.5)	
	utilityNew1 = 0
	j = 0
	g1 = 5							#specific good happiness for agent 1 
	g2 = 7
	g3 = 9
	g4 = 11
	g5 = 13
	while (j < 10):
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
	for i in range(10):
		if Ua1[i] == 0 and Ua1[i-1] != 0:
			utilityNew1 = Ua1[i-1]
		else: i = i + 1
	return utilityNew1

def Utility2():
	#Agent 1 Utility update
	utility_A2 = np.zeros((1,100))
	utility_Calories = 0
	g = np.arange(0.0, 750, 0.5)	
	utilityNew2 =0
	j = 0
	g1 = 1							#specific good happiness for agent 1 
	g2 = 2
	g3 = 3
	g4 = 4
	g5 = 5
	while (j < 10):
		#Calculates utility value at given point in time
		utility_g1 = 100*(goods_index[1][0]/g1)/((goods_index[1][0]/g1)**2+1)
		utility_g2 = 100*(goods_index[1][1]/g2)/((goods_index[1][1]/g2)**2+1)
		utility_g3 = 100*(goods_index[1][2]/g3)/((goods_index[1][2]/g3)**2+1)
		utility_g4 = 100*(goods_index[1][3]/g4)/((goods_index[1][3]/g4)**2+1)
		utility_g5 = 100*(goods_index[1][4]/g5)/((goods_index[1][4]/g5)**2+1)

		for i in range(goods):
			utility_Calories = utility_Calories + 100*(goods_index[1][i]*Calories_index[i][0]/Q0)/(goods_index[1][i]*Calories_index[i][0]/Q0+1)

		#Instantaneous utility for Agent 1 
		utility_A2 = utility_g1 + utility_g2 + utility_g3 + utility_g4 + utility_g5 + utility_Calories
		Ua2[j] = utility_A2
		j = j+1
		
	for i in range(10):
		if Ua2[i] == 0 and Ua2[i-1] != 0:
			utilityNew2 = Ua2[i-1]
		else: i = i + 1
	return utilityNew2

def Agent1(goods_index):
	alpha1 = Utility1()
	if alpha1 < Umax1:
		Bid1 = 0						#Must Have some sort of Calculation to determine Ask/Bid Price
		Ask1 =1
	if alpha1 > Umax1:
		Ask1 = 1
		Bid1 = 0
	#else:
		#nothing()
	return Bid1, Ask1

def Agent2(goods_index):
	alpha2 = Utility2()
	if alpha2 < Umax2:
		Bid2 = 1						#Must Have some sort of Calculation to determine Ask/Bid Price
		Ask2 = 0
	if alpha2 > Umax2:
		Ask2 = 1
		Bid2 = 0
	#else:
		#nothing()
	return Bid2, Ask2


def Market(Bid1, Ask1, Bid2, Ask2):
	if Ask1 == Bid2:
		goods_index[0][0] = goods_index[0][0] - 1
		goods_index[1][0] = goods_index[1][0] + 1

m = 0
while(m < 10):
	B1,A1 = Agent1(goods_index)			#Updates Utility and makes Trade proposals
	B2,A2 = Agent2(goods_index)
	Market(B1,A1,B2,A2)					#Makes Trades and Updates Utility
	m = m + 1

print goods_index



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

