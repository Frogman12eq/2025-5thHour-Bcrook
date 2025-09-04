#Name:  Bryson Crook
#Class: 5th Hour
#Assignment: HW5


#1. Create a list with 9 different numbers inside.
big_list = [1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 ,  9]
#2. Sort the list from highest to lowest.
big_list.sort(reverse=True)
#3. Create an empty list.
small_list = []
#4. Remove the median number from the first list and add it to the second list.
chicken = big_list[4]
big_list.pop(4)
small_list.append(chicken)
#5. Remove the first number from the first list and add it to the second list.
bigger_chicken = big_list[0]
big_list.pop(0)
small_list.append(bigger_chicken)
#6. Print both lists.
print(small_list)
print(big_list)
#7. Add the two numbers in the second list together and print the result.
tiny_list = small_list[0] + small_list[1]
print(tiny_list)
#8. Move the number back to the first list (like you did in #4 and #5 but reversed).
big_list.append(tiny_list)
small_list.pop(0)
small_list.pop(0)
print(small_list)
#9. Sort the first list from lowest to highest and print it.
big_list.sort()
print(big_list)