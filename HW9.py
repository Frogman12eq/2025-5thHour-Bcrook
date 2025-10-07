#Name: Bryson Crook
#Class: 6th Hour
#Assignment: HW9
import random

#1. Print "Hello World!"
print("Hello World!")
#2. Create a list with three variables that each randomly generate a number between 1 and 100
Number= [random.randint(1,100), random.randint(1,100), random.randint(1,100)]
#3. Print the list.
print(Number)
#4. Create an if statement that determines which of the three numbers is the highest and prints the result.
if Number[0] > Number[1] and Number[0] > Number[2]:
    print("One is bigger than number 2 and 3")
    num = Number[0]
elif Number[1] > Number[0] and Number[1] > Number[2]:
    print("Two is bigger than number 1 and 3")
    num = Number[1]
else:
    print("Three is bigger than 1 and 2")
    num = Number[2]
#5. Tie the result (the largest number) from #4 to a variable called "num".

#6. Create a nested if statement that prints if num is divisible by 2, divisible by 3, both, or neither.
if num % 2 == 0:
    if num % 3 == 0:
        print("Divisible by both two and three")
    else:
        print("Divisible by two but not three")
else:
    if num % 3 == 0:
        print("Not divisible by two but it is by three")
    else:
        print("it is neither divisible by two but not three")