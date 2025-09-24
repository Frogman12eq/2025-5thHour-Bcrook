#Name:Bryson Crook
#Class: 5th Hour
#Assignment: HW7
from HW6 import students_in_class

#1. Print Hello World!
print("Hello World!")
#2. Create a dictionary with 3 keys and a value for each key. One of the keys must have a value with a list containing
#three numbers inside.
judes_info= {
    "Name": "Jude",
    "Age": 14000,
    "Judes_social_security_number": [1,8,0]
}
#3. Print the keys of the dictionary from #2.
print(judes_info.keys())
#4. Print the values of the dictionary from #2
print(judes_info.values())
#5. Print one of the three numbers from the list by itself
print(judes_info["Judes_social_security_number"][0])
#6. Using the update function, add a fourth key to the dictionary and give it a value.
judes_info.update({"Birthdate" : "June 31st 1"})
#7. Print the entire dictionary from #2 with the updated key and value.
print(judes_info)
#8. Make a nested dictionary with three entries containing the name of another classmate and two other pieces of information
#within each entry.
students_in_class = {
    "Student_1" : {
     "Name": "Jude",
  "Age": 14,
    "sports" : False
      },
"Student_two" : {
     "Name": "Marti",
    "Age": 18,
    "sports" : False,
},
    "Student_3" : {
     "Name": "Waylon",
    "Age": 16,
        "sports" : False,
    }
}
#9. Print the names of all three classmates on the same line.
print(students_in_class["Student_3"]["Name"],students_in_class["Student_two"]["Name"],students_in_class["Student_1"]["Name"])
#10. Use the pop function to remove one of the nested dictionaries inside and print the full dictionary from #8.
students_in_class.pop("Student_1")
print(students_in_class)