#Name: Bryson Crook
#Class: 5th Hour
#Assignment: HW20

#1. Create a class containing a def function that inits self and 3 other attributes for store items (stock, cost, and weight).
class store_items:
    def __init__(self,stock,cost,weight):
        self.stock=stock
        self.cost=cost
        self.weight=weight
    def cost_multiplier(self):
        self.cost=self.cost * 2
#2. Make 3 objects to serve as your store items and give them values to those 3 attributes defined in the class.
pc=store_items(1, 1000, 20)
paper=store_items(100, 10, 5)
pen=store_items(1000, 10,2.5)
#3. Print the stock of all three objects and the cost of the second store item.
print("Pc stock",pc.stock,)
print("Paper stock",paper.stock)
print("Pen stock",pen.stock)
print("Paper cost is", paper.cost)
#4. Make a def function within the class that doubles the cost an item, double the cost of the second store item, and print the new cost below the original cost print statement.
paper.cost_multiplier()
print("Paper cost is", paper.cost)
#5. Directly change the stock of the third store item to approx. 1/4th the original stock and then print the new stock amount.
pen.stock= round(pen.stock/4)
print("The stock of pens as decreased to 1/4 it's original amount, the new new stock is:",pen.stock)
#6. Delete the first store item and then attempt to print the weight of the first store item. Create a try/except catch to fix the error.
del pc

try:
    print(pc.weight)
except:
    print("There is no more in stock try again in a year")
