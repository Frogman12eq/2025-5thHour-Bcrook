#Name: Bryson Crook
#Class: 5th Hour
#Assignment: HW4


#1. Print Hello World!
print ("hello world")
#1. Create a list with 5 strings containing 5 different names in it.
bohemian_car_insurance = ["Ford" , "Volvo" , "Kia" , "Nissan" , "Cheverlette"]
#2. Append a new name onto the Name List.
bohemian_car_insurance.append(input("Car Brand Here:"))
#3. Print out the 4th name on the list.
print(bohemian_car_insurance [3])
#4. Create a list with 4 different integers in it.
Amount_of_money = [4 , 5 , 6 ,7]
#5. Insert a new integer into the 2nd spot and print the new list.
Amount_of_money.insert (2, 8)
print(Amount_of_money)
#6. Sort the list from lowest to highest and print the sorted list.
Amount_of_money.sort()
print(Amount_of_money)
#7. Add the 1st three numbers on the sorted list together and print the sum.
Amount_of_money_subsum = Amount_of_money[0] + Amount_of_money[1] + Amount_of_money[2]
print(Amount_of_money_subsum)
#8. Create a list with two strings, two variables, and too boolean values.
Judes_bank_business = [True , False , " big successful" , "MASSIVE successful" , 6 , 7]
#9. Create a print statement that asks the user to input their own index value for the list on #8.
print(Judes_bank_business[int(input("insert number here: "))])