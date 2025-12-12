#Name: Bryson Crook
#Class: 5th Hour
#Assignment: HW14
import random
import time
#1. Create a for loop with variable i that counts down from 5 to 1 and then prints "Hello World!"
#at the end.

for i in range(5,0,-1):
    time.sleep(0.5)
    print(i)
else:
    print("Hello World")
#2. Create a for loop that counts up and prints only even numbers between 1 and 30.
for l in range(1,31):
    time.sleep(0.25)
    if l % 2 == 0:
        print(l)

#3. Create a for loop that prints from 1 to 30 and continues (skips the number) if the number is
#divisible by 3.
for a in range(1,31):
    if a % 3 == 0:
        continue
    else:
        print(a)

#4. Create a for loop that prints 5 different animals from a list.
animals= ["Bat", "Cat", "Dog", "Dolphin", "Tiger"]
for animal in animals:
    print(animal)
#5. Create a for loop that spells out a word you input backwards.
#(HINT: Google "How to reverse a string in Python")
for d in input("Give me a word: ")[::-1]:
    print(d)
#6. Create a list containing 10 integers of your choice and print the list.
c= [1,2,3,4,5,6,7,8,9,1]
print(c)
#7. Create two empty variables named evenNumbers and oddNumbers.
even=0
odd=0
#8. Make a loop that counts the number of even and odd numbers in the list, and prints the
#result after the loop.
for g in c:
    if g % 2 == 0:
        even += 1
    else:
        odd += 1
print(even, odd)
#9. Create a variable that asks the user for an integer and an empty integer variable.
p = int(input("Give me a number: "))
o=1
#10. Create a loop with a range from 1 to the number the user input. Use the loop to find the
#factorial of that number and print the result. A factorial of a number is that number multiplied
#by every number before it until you reach 1. (For example: 5! is 5 x 4 x 3 x 2 x 1 = 120)
for z in range(1,p + 1):
    o*=z
print(o)