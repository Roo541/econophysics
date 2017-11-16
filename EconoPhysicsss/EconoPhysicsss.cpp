// EconoPhysicsss.cpp : Defines the entry point for the console application.

#include "stdafx.h"
#include <iostream>
#include <array>
#include <cmath>
#include <math.h>
using namespace std;

#define num_goods 5
#define num_agents 5

float Sell(int[num_agents][num_goods], float[]);
float Agent_1(float[num_agents][num_goods], float[]);

//information of agents and what they have:goods, cash
int main()
{
	float Goods[num_agents][num_goods]; //creates a 2-d array of agents and number of goods they have
	for (int a=0;a<=num_agents;a++) {
		for (int g=0;g<=num_goods;g++) {
			Goods[a][g] = 100;
		}
	}
	float Cash[num_agents] = { 1000, 1000, 200, 10, 10 }; //creates array of cash each agent has
	float calories[num_goods] = { 100, 50, 250, 200, 300 }; // index of calories each good has
	float number = Agent_1(Goods, Cash); 
	
	system("Pause");

	return 0;
}

float Agent_1(float Goods[num_agents][num_goods], float Cash[]) 
{
	float gmax[num_goods] = {10, 5, 20, 30, 5};
	float Q = 1;
	float Q0 = 5;
	float utility_1g = 10;
	float utility_1Q = (Q / Q0) / ((Q / Q0) - 1);
	float utility_1I = log(Cash[0]);
	for (int a = 0;a <= num_goods; a++) {
		 float placeholder = (Goods[0][a] / gmax[a]) / ((Goods[0][a] / gmax[a])*(Goods[0][a] / gmax[a]) + 1);
		 utility_1g = placeholder + (Goods[0][a] / gmax[a]) / ((Goods[0][a] / gmax[a])*(Goods[0][a] / gmax[a]) + 1);
	}	
	float Utility_1_T = utility_1Q + utility_1g + utility_1I;
	
	return 0;
}

//sell function
float Sell(int a[num_agents][num_goods], float b[num_agents])
{
	//cout << a[0] << endl;
	//cout << b[0] << endl;

	return 0;
}
