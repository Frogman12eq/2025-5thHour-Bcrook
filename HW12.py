#Name: Bryson crook
#Class: 5th Hour
#Assignment: HW12
import random
#1. Create a while loop with variable i that counts down from 5 to 0 and then prints
#"Hello World!" at the end.
i = 5
while i >= 0:
    print(i)
    i -= 1
else:
    print("hello world")
#2. Create a while loop that prints only even numbers between 1 and 30 (HINT: modulo).
l = 1
while l <= 30:
    if l % 2 == 0:
        print(l)
    l += 1
#3. Create a while loop that prints from 1 to 30 and continues (skips the number) if the
#number is divisible by 3.
c = 1
while c <= 30:
    if c % 3 == 0:
        c +=1
        continue
    else:
        print(c)
        c+=1
#4. Create a while loop that randomly generates a number between 1 and 6, prints the result,
#and then breaks the loop if it's a 1.
r = random.randint(1,6)
while r < 6:
    if r == 1:
        break
    print(r)
    r = random.randint(1, 6)
#5. Create a while loop that asks for a number input until the user inputs the number 0.
n = int(input("Insert number here:"))
while n != 0:
    print(n)
    n = int(input("Insert number here:"))