#Name: Bryson Crook
#Class: 5th Hour
#Assignment: HW11

#1. Go to the link below and convert the code into pseudocode in comments, then code the flowchart completely:
#https://adacomputerscience.org/images/content/computer_science/design_and_development/program_design/figures/ada_cs_design_flow_ifelseif.svg

#import random library
import random
#Make temperature variable, give it a value (random from 1 to 30)
temp = random.randint (1, 30)
#Make if statement that checks if temp is more than 20
#   - If more, print it's hot
#   - If less, go to next if statement

#Make if statement that checks if temp is more than 10
#   - If more, print it's mild
#   - If less, print it's cold

#Print thank you, and end the code


#Code goes here:
print(temp)
if temp > 20:
    print("It is hot")
elif temp > 10:
    print("It is mild")
else:
    print("It is cold")
print("Thank you")