#Name: Bryson Crook
#Class: 5th Hour
#Assignment: HW10
from operator import truediv

#1. Print Hello World!
print("Hello world!")
#2. Create three different boolean variables named wifi, login, and admin.
wifi= True
login= True
admin= True
#3. Create a separate integer variable that denotes the number of times
#someone with admin credentials has logged in.
login_tries= 67
#4. Create a nested if statement that checks to see if wifi is true,
#login is true, and admin is true. If they are all true, print a
#welcome message and increase the integer variable by one. If one of them
#is false, print an error message telling them which one they are "missing".
if wifi == True:
    if login == True:
        if admin == True:
            print("Welcome Admin")
            login_tries = login_tries + 1
        else:
            print("You are not an Admin")
    else:
        print("Your login failed")
else:
    print("You have no wifi")