#Name:
#Class: 5th Hour
#Assignment: HW15

#1. import the "random" library
import random
#2. print "Hello World!"
print("Hello World")
#3. Create three variables named a, b, and c, and allow the user to input an integer for each.
a= int(input("Enter a number"))
b= int(input("Enter another number"))
c= int(input("Enter a number"))
#4. Add a and b together, then divide the sum by c. Print the result.
num= (a+b)/c
print(num)
#5. Round the result from #3 up or down, and then determine if it is even or odd.
num=round(num)
print(num)
if num % 2 == 0:
    print("Even")
else:
    print("Odd")
print(num)
#6. Create a list of five different random integers between 1 and 10.
numList= [random.randint(1,10), random.randint(1,10), random.randint(1,10), random.randint(1,10), random.randint(1,10),]
#7. Print the 4th number in the list.
print(numList[3])
#8. Append another integer to the end of the list, also random from 1 to 10.
numList.append(random.randint(1,10))
#9. Sort the list from lowest to highest and then print the 4th number in the list again.
numList.sort()
print(numList)
print(numList[3])
#10. Create a while loop that starts at 1, prints i and then adds i to itself until it is greater than 100.
i=1
while i <100:
    i+=i
    print(i)
#11. Create a list containing the names of five other students in the classroom.
people= ["Jude", "Hogan", "Dylan", "Ivan", "Sam"]
#12. Create a for loop that individually prints out the names of each student in the list.
for person in people:
    print(person)
#13. Create a for loop that counts from 1 to 100, but ends early if the number is a multiple of 10.
z= 1
for z in range(1,101):
    print(z)
    if z % 10 ==0:
        break
#14. Free space. Do something creative. :)
list=["S", "O", "M", "E", "T", "H", "I", "N", "G", "C", "R","E", "A", "T", "I", "V", "E"]

print(list)