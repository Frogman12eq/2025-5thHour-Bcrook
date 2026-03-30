#Name: Bryson Crook
#Class: 5th Hour
#Assignment: HW-R2

import random
#1. Print "Hello World!"
print("Hello World!")
#2. Create an empty list.
empty_list= []
#3. Create a list that contains the names of everyone in the classroom.
names_of_students= ["Ashton", "Hogan", "Aiden", "Sam", "Brennlyn", "Bryson"]
#4. Print the list from #3, sort the list, then print the list again.
print(names_of_students)
names_of_students.sort()
print(names_of_students)
#5. Append 5 different integers into the empty list from #2 and print the list.
empty_list.append(1)
empty_list.append(2)
empty_list.append(3)
empty_list.append(4)
empty_list.append(5)
print(empty_list)
#6. Add together the middle three numbers in the list from #2 and print the result.
adding= empty_list[1] + empty_list[2] + empty_list[3]
print(adding)
#7. Remove the very first number in the list from #2. Print the new first number.
empty_list.pop(0)
print(empty_list[0])
#8. Create a dictionary with three keys with respective values: your name, your grade, and your favorite color.
brysoninfoDict = {
    "Name" : "Bryson",
    "Grade" : "9th",
    "Fav color" : "Navy Blue"
}

#9. Using the update function, add a fourth key and value determining your favorite candy.
brysoninfoDict.update({"Fav Candy" : "Candy Senzu Beans"})
#10. Print ONLY the values of the dictionary from #8.
print(brysoninfoDict["Name"])
print(brysoninfoDict["Grade"])
print(brysoninfoDict["Fav Candy"])
print(brysoninfoDict["Fav color"])