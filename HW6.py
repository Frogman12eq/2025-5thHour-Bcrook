#Name: Bryson Crook
#Class: 5th Hour
#Assignment: HW6


#1. Import the "random" library
import random
#2. print "Hello World!"
print("Hello World")
#3. Create three different variables that each randomly generate an integer between 1 and 10
d10_1 = random.randint(1, 10)
d10_2 = random.randint(1, 10)
d10_3 = random.randint(1, 10)
#4. Print the three variables from #3 on the same line.
print(d10_1, d10_2, d10_3)
#5. Add 2 to the first variable in #3, Subtract 4 from the second variable in #3, and multiply by 1.5 the third variable in #3.
mmm = d10_1 + 2
mmmm = d10_2 - 4
mmmmm = d10_3 * 1.5
#6. Print each result from #5 on the same line.
print(mmm, mmmm, mmmmm)
#7. Create a list containing four variables that each randomly generate an integer between 1 and 6
judes_college_thing = [random.randint(1, 6), random.randint(1, 6), random.randint(1, 6), random.randint(1, 6)]
#8. Sort the list in #7 and print it.
judes_college_thing.sort()
print(judes_college_thing)
#9. Add together the highest three numbers in the list from #7 and print the result.
jude_some_or_something_like_that = judes_college_thing[1] + judes_college_thing[2] + judes_college_thing[3]
print(jude_some_or_something_like_that)
#10. Create a list with 5 names of other students in this class and print the list.
students_in_class = ["Jude", "Hogan", "Waylon", "Marti", "Brennlyn"]
print(students_in_class)
#11. Shuffle the list in #10 and print the list again.
random.shuffle(students_in_class)
print(students_in_class)
#12. Print a random choice from the list of names from #10.
print(random.choice(students_in_class))