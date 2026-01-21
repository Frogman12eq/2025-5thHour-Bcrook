#Name: Bryson Crook
#Class: 5th Hour
#Assignment: HW17
import random
#1. Create a def function that plays a single round of rock, paper, scissors where the user inputs
#1 for rock, 2 for paper, or 3 for scissors and compares it to a random number generated to serve
#as the "opponent's hand".

#2. Create a def function that prompts the user to input if they want to play another round, and
#repeats the RPS def function if they do or exits the code if they don't.
def rock_paper_scissors():
    players_rps=int(input("Enter rock (1) paper (2) or scissors (3):"))
    computer = random.randint(1, 3)
    print(computer)
    if computer == players_rps:
        print("It's a draw!")
    elif computer == 1 and players_rps == 2:
        print("you win!")
    elif computer == 2 and players_rps == 1:
        print("you lose!")
    elif computer == 3 and players_rps == 2:
        print("you lose!")
    elif computer == 2 and players_rps == 3:
        print("you win!")
    elif computer== 3 and players_rps == 1:
        print("you win!")
    elif computer == 1 and players_rps== 3:
        print("you lose!")
    restart_game()
def restart_game():
    restart= input("Do you want to restart game? (y/n) ")
    if restart == "y" or restart == "Y":
        rock_paper_scissors()
    else:
        print("Thank you for playing!")
        exit()
rock_paper_scissors()