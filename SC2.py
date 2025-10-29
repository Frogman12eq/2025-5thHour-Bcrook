#Name:
#Class: 5th Hour
#Assignment: SC2


#A local health clinic is looking to add a quick BMI calculator to their website so that their
#patients can quickly input their height and weight and be given a number as well as their
#classification. The classifications are as follows:

# - Underweight: Less than 18.5 BMI
# - Normal Weight: 18.5 to 24.9 BMI
# - Overweight: 25 to 29.9 BMI
# - Obese: 30 or more BMI

#It is up to you to figure out the calculation for an accurate BMI reading and tying it to
#the right classification

#Code Here:

weight = int(input("Enter bodyweight here in pounds:"))
height = int(input("Enter height in inches:"))
bmi=(weight/height ** 2) * 703
print(bmi)
if bmi < 18.5:
    print("You are underweight")
elif 18.5 <= bmi < 24.9:
    print("You are normal")
elif 25 <= bmi < 29.9:
    print("You are overweight")
else:
    print("You are obese")