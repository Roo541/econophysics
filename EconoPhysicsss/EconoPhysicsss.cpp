// EconoPhysicsss.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <array>
using namespace std;

#define NUM_GOODS 5
#define NUM_AGENTS 7

float Sell(int[NUM_AGENTS][NUM_GOODS], float[]);

int main()
{
	int Goods[NUM_AGENTS][NUM_GOODS];
	for (int a=0;a<NUM_AGENTS;a++) {
		for (int g=0;g<NUM_GOODS;g++) {
			Goods[a][g] = 100;
		}
	}
	float Cash[NUM_AGENTS] = { 1000, 1000, 200, 10, 10, 10, 10 };
	int number = Sell(Goods, Cash);
	cout << number << endl;

#ifdef _WIN32
	system("Pause");
#endif
	return 0;
}

float Sell(int a[NUM_AGENTS][NUM_GOODS], float b[NUM_AGENTS])
{
	cout << a[0] << endl;
	cout << b[0] << endl;

	return 0;
}
