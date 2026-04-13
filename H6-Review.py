#Name: Bryson Crook
#Class: 5th Hour
#Assignment: HW-R6


#1. Create a def function that prints out "Hello World!". Call the function.
def hello_world():
    print("hello world")
hello_world()
#2. Create a def function that prints your name. Call the function with the name as the argument.
def name(name):
    print(name)
name("Bryson")
#3. Create a def function that calculates the average of a list. Call the function with the list as the argument.
def num(*num):
    avg = sum(num) / len(num)
    print(avg)
num(2,32,54,61)
#4. Call the function from #3 but with a new list of different numbers.
num(1,49,76,80)
#5. Create a def function that takes two numbers as arguments, x and y. Inside the function, create a for loop
#with a range of 10. Inside the loop, make z equal the sum of x and y, make x equal y, then y equal z.
def fib(x,y):
    for p in range(10):
        z = x + y
        x = y
        y = z
        print(x)
#6. Call the function from #5 with the arguments for x and y being 0 and 1.
fib(0 ,1)