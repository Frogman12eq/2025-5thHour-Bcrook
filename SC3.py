#Name: Bryson Crook
#Class: 5th Hour
#Assignment: SC3

#You have been transferred to a new team working on a mobile game that allows you to dress up a
#model and rate other models in a "Project Runway" style competition.

#They want to start prototyping the rating system and are asking you to make it.
#This prototype needs to allow the user to input the number of players, let each player rate
#a single model from 1 to 5, and then give the average score of all of the ratings.
players=int(input("Enter number of players: "))
o=0
for i in range(1,players + 1):
    rating=int(input("Enter rating between 1-5: "))
    while (rating<1 or rating>5):
        print("Invalid vote")
        rating = int(input("Enter rating between 1-5: "))
    else:
        o+=rating
print(o/players)
