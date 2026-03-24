#Name: Bryson Crook
#Class: 5th Hour
#Assignment: HW-R3


#1. import random and print "Hello World!"
import random
print("Hello World!")
#2. Create three variables that each randomly generate an integer between 1 and 10, print each number on the same line.
x = random.randint(1,10)
y = random.randint(1,10)
z = random.randint(1,10)
print(x,y,z)
#3. Create a list containing 5 strings listing 5 colors.
colors= ["red","blue","green","yellow","pink"]
#4. Use a function to randomly choose one of the 5 colors from the list and print the result.
print(random.choice(colors))
#5. Create an if statement that determines which of the three variables from #2 is the lowest.
if y <= x and y<= z:
 print("Y is the lowest number")
elif x <= y and x<= z:
    print("X is the lowest number")
else:
    print("Z is the lowest number")
