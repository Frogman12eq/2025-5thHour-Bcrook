#Name: Bryson Crook
#Class: 5th hour computer science
#Assignment: Playground

import random

'''
guess = input("Enter your guess here range between 1 and 50:")
number = random.randint(1, 50)
brysons_guess=(guess)
print("brysons guess",brysons_guess)
guess_2 = input("Enter your guess here range between 1 and 50:")
judes_guess = (guess_2)
print("Judes guess",judes_guess)
guess_3 = input("Enter your guess here range between 1 and 50:")
ivan_guess=(guess_3)
print("ivan guess",ivan_guess)
print(number)
'''
'''
left_right = random.choice([ "Right", "Left"])
direction = random.choice(["forward", "backwards"])
key_word_guess= input("Enter left or right here:")
if key_word_guess == left_right:
    direction_of_choice = input("Enter forward or backwards here:")
    if direction_of_choice == direction:
        print("You live")
else:
    print("You Die")
    '''
zombie_health= 27
zombie_damage= 2
zombie= [zombie_health,zombie_damage ]
print(zombie)
player_health= 50
player_damage= 4
player= [player_health, player_damage]
print(player)
zombie_location = random.choice(["Zombie", "No Zombie"])
left_right= input("Left or Right?")
if left_right == "Left":
    print("you went left")
    if zombie_location == "Zombie":
        print("Enemy ahead")





