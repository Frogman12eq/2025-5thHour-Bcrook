#Name: Bryson
#Class: 5th Hour
#Assignment: HW_R8


#1. Import all of HW_R7 into this assignment using the from/import function.
from H7_Review import *
#2. Create an object of three students in the classroom. Ask for their name, grade, and favorite color as need be.
Hogan= person_info("Hogan", 10, "Blue and or Green")
Ashton= person_info("Ashton", 11, "Purple")
Ivan= person_info("Ivan", 12, "Purple")
#3. Print the name of the first student.
print(Hogan.Name)
#4. Use the def function from HW_R7 to bump the grade level of the second student up by 1. Print the new grade.
Ashton.grade_up()
print(Ashton.Grade)
#5. Use the def function from HW_R7 to ask the third student to change their favorite color to something else.
#Print the new color.
Ivan.new_color()
print(Ivan.color)