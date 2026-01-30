#Name: Bryson Crook
#Class: 5th Hour
#Assignment: HW18

import random
#1. Import the "random" library and create a def function that prints "Hello World!"
def hello_world():
    print("Hello World!")

#2. Create two empty integer variables named "heads" and "tails"
heads=0
tails=0
#3. Create a def function that flips a coin one hundred times and increments the result in the above variables.
def h_or_t():
    global heads,tails
    for i in range(100):
        h_or_t_flip = random.randint(1, 2)
        if h_or_t_flip==1:
            heads+=1
        else:
            tails+=1


#4. Call the "Hello world" and "Coin Flip" functions here
hello_world()
h_or_t()
#5. Print the final result of heads and tails here
print(heads)
print(tails)
#6. Create a list called beanBag and add at least 5 different colored beans to the list as strings.
beanBag= ["Green", "Red", "Blue", "Yellow", "Purple"]

#7. Create a def function that pulls a random bean out of the beanBag list, prints which bean you pulled, and then removes it from the list.

def bean():
    if beanBag==[]:
        print("No beans")
    else:
        hand=random.choice(beanBag)
        print(hand)
        beanBag.remove(hand)
    bean_repull()
#8. Create a def function that asks if you want to pull another bean out of the bag and, if yes, repeats the #3 def function
def bean_repull():
        repull = input("Would you like to repull? Y/N")

        if repull == "Y" or repull == "y":
            bean()
        else:
            print("Thanks for playing!")

#9. Call the "Bean Pull" function here
bean()