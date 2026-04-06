#Name: Bryson
#Class: 5th Hour
#Assignment: HW-R5

#1. Create a list of the names of all the students in the classroom.
names= ["Dylan", "Ivan", "Bryson", "Sam", "Brennlyn", "Aiden", "Ashton", "Hogan"]
#2. Create a for loop that prints the names of every student in the list.
for name in names:
    print(name)
#3. Using the "in" operator (hint: Google), create a for loop that only prints
#the name of a student if the letter "e" is in it.
print("------")
for name in names:
    if "e" in name:
        print(name)