// EconoPhysicsss.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <array>
using namespace std;

float Sell(int[], float[]);
int main()
{
	int Goods[5] = { 1,2,3,4,5 };
	float Cash[1] = { 1000 };
	int number = Sell(Goods, Cash);
	cout << number << endl;

	system("Pause");
	return 0;
}

float Sell(int a[5], float b[1])
{
	cout << a[0] << endl;
	cout << b[0] << endl;

	return 0;
}
