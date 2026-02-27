#Name: Bryson Crook
#Class: 5th Hour
#Assignment: Scenario 6

import random
from ctypes import GetLastError


#With a fresh perspective, the team lead wants you to look back and refactor the old combat code to
#be streamlined with classes so the character and enemy stats won't be built in bulky dictionaries anymore.

#(Translation: Rebuild Semester Project 1 using classes instead of dictionaries, include and refactor
#the combat test code below as well.)
class character:
    def __init__(self,HP,init,ac,atkmod,damage):
        self.HP = HP
        self.init = init
        self.atkmod = atkmod
        self.damage = damage
        self.ac = ac
Astarion= character(40,3,14,5,random.randint(1,8) + random.randint(1,6) + 4)
LaeZel= character(48,1,17,6,random.randint(1,6) + random.randint(1,6) + 3)
Shadowheart=character(40,1,18, 4, random.randint(1,6) +3)
Gale= character(32,1,14,6, random.randint(1,10) + random.randint(1,10))
Goblin=character(7,0,12,4, random.randint(1,12)+ 3)
Orc=character(15,1,13,5,random.randint(1,12) + 3)
Troll=character(84,1,15,7, random.randint(1,6) + random.randint(1,6) + 4)
Mindflayer=character(71,1,15,7,random.randint(1,10) + random.randint(1,10) + 4)
Dragon=character(127,2,18,7,random.randint(1,10) + random.randint(1,10)+ random.randint(1,8) + 4)


hero_init_roll= random.randint(1,20) + Astarion.init
villain_init_roll= random.randint(1,20) + Orc.init
print(hero_init_roll, villain_init_roll)
if hero_init_roll > villain_init_roll:
    print("Hero goes first")
    hero_first = True
elif villain_init_roll > hero_init_roll:
    print("Villain goes first")
    hero_first= False
else:
    print("Hero goes first")
    hero_first= True


if hero_first ==True:
    while Astarion.HP > 0 or Orc.HP > 0:
        hero_atk_roll = random.randint(1, 20)
        if hero_atk_roll == 20:
            print("Critical Hit!")
            Orc.HP -= (Astarion.damage * 2)
        elif hero_atk_roll == 1:
            print("Critical Miss!")
        elif hero_atk_roll + Astarion.atkmod >= Orc.ac:
            print("Hero hits!")
            Orc.HP -= Astarion.damage
        elif hero_atk_roll + Astarion.atkmod < Orc.ac:
            print("Hero misses!")

        if Orc.HP <= 0:
            print("The Orc is dead!")
            break
        else:
            print(f"Orc has {Orc.HP} HP")

        orc_atk_roll = random.randint(1, 20)
        if orc_atk_roll == 20:
                print("Critical Hit!")
                Astarion.HP -= (Orc.damage * 2)
        elif orc_atk_roll == 1:
                print("Critial Miss!")
        elif orc_atk_roll + Orc.atkmod >= Astarion.ac:
                print("Orc hits!")
                Astarion.HP -= Orc.damage
        elif orc_atk_roll + Orc.atkmod < Astarion.HP:
                print("Orc misses!")

        if Astarion.HP <= 0:
                print("Astarion is dead!")
                break
        else:
            print(f"Astarion has {Astarion.HP} HP.")

elif hero_first==False:
    while Astarion.HP > 0 or Orc.HP > 0:
        orc_atk_roll = random.randint(1, 20)
        if orc_atk_roll == 20:
            print("Critical Hit!")
            Astarion.HP -= (Orc.damage * 2)
        elif orc_atk_roll == 1:
            print("Critial Miss!")
        elif orc_atk_roll + Orc.atkmod >= Astarion.ac:
            print("Orc hits!")
            Astarion.HP -= Orc.damage
        elif orc_atk_roll + Orc.atkmod < Astarion.HP:
            print("Orc misses!")

        if Astarion.HP <= 0:
            print("Astarion is dead!")
            break
        else:
            print(f"Astarion has {Astarion.HP} HP.")

        hero_atk_roll = random.randint(1, 20)
        if hero_atk_roll == 20:
            print("Critical Hit!")
            Orc.HP -= (Astarion.damage * 2)
        elif hero_atk_roll == 1:
            print("Critical Miss!")
        elif hero_atk_roll + Astarion.atkmod >= Orc.ac:
            print("Hero hits!")
            Orc.HP -= Astarion.damage
        elif hero_atk_roll + Astarion.atkmod < Orc.ac:
            print("Hero misses!")

        if Orc.HP <= 0:
            print("The Orc is dead!")
            break
        else:
            print(f"Orc has {Orc.HP} HP")
