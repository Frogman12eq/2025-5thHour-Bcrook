#Name: Bryson Crook
#Class: 5th Hour
#Assignment: HW_R7


#1. Create a class containing a def function that inits self and the three attributes: name, grade, color.
class person_info:
    def __init__ (self, Name, Grade, color):
        self.Name = Name
        self.Grade = Grade
        self.color = color
#2. Make a def function within the class that adds 1 to the grade attribute to any object called to it.
#If they are 12th grade, have the code change their grade to "graduated" instead.
    def grade_up(self):
        if self.Grade == 12:
            self.Grade = "Graduated"
        else:
            self.Grade  += 1

#3. Make a def function within the class that offers the user to input/change their favorite color.
    def new_color(self):
        self.color = input("Pick a new color: ")