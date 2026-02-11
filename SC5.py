#Name: Bryson Crook
#Class: 5th Hour
#Assignment: SC5

#Import all of SC4 here
from SC4 import *

listAverage = 0

def final_average():
    global listAverage
    listAverage =  sum(stat_results)/len(stat_results)   #Calculate the sum of the list by the length of the list here
    return listAverage

final_average()

print(listAverage)