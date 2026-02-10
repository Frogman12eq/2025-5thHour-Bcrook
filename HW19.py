#Name: Bryson crook
#Class: 5th Hour
#Assignment: HW19

#1. Import the def functions created in problem 1-4 from HW16
from HW16 import hello_world, average, animals, repeat
#2. Call the functions here and run HW19
hello_world()
average(4,20,2001)
animals("Leopard", "Bat", "Rat", "Cat", "Chicken")
repeat(20)
#3. Delete all calls from HW16 and run HW19 again.
print("It has been done")
#4. Create a try catch that tries to print variable x (which has no value), but prints "Hello World!" instead.
try:
    print(x)
except:
    print("Hello World")
#5. Create a try catch that tries to divide 100 by whatever number the user inputs, but prints an exception for Divide By Zero errors.
try:
    num_div = int(input("Give me an integer: "))
    print(100/num_div)
except ZeroDivisionError:
    print("Cannot divide by zero!")
#6. Create a variable that asks the user for a number. If the user input is not an integer, prints an exception for Value errors.
try:
    v = int(input("Give me an integer"))
    print(v)
except:
    raise ValueError("It needs to be an integer!")
#7. Create a while loop that counts down from 5 to 0, but raises an exception when it counts below zero.
i = 5
while i > 0:
    print(i)
    i = i - 1
    if i <= 0:
        raise Exception("It's at zero")