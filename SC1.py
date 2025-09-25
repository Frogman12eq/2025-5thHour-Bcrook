#Name:
#Class: 5th Hour
#Assignment: Scenario 1

#Scenario 1:
#You are a programmer for a fledgling game developer. Your team lead has asked you
#to create a nested dictionary containing five enemy creatures (and their properties)
#for combat testing. Additionally, the testers are asking for a way to input changes
#to the enemy's damage values for balancing, as well as having it print those changes
#to confirm they went through.
bad_guys= {
    "Enemy 1" : {
        "Name": "Nosyrb",
    "Ability": "Semi truck",
    "Damage" : 1000000000000000000000000000000000000000000000000000000000000000000000
    },
    "Enemy 2" : {
        "Name": "Eduj",
    "Ability": "car.",
    "Damage" : 20
    },
"Enemy 3" : {
        "Name 3": "NnylnerB",
    "Ability": "trike",
    "Damage" : 2
    },
"Enemy 4" : {
        "Name": "Nitram",
    "Ability": "helicopter",
    "Damage" : 3
    },
"Enemy 5" : {
        "Name": "Koorc",
    "Ability": "Missile",
    "Damage" : 100
    },
}
bad_guys["Enemy 1"]["Damage"] = input("Enter new damage: ")
bad_guys["Enemy 2"]["Damage"] = input("Enter new damage: ")
bad_guys["Enemy 3"]["Damage"] = input("Enter new damage: ")
bad_guys["Enemy 4"]["Damage"] = input("Enter new damage: ")
bad_guys["Enemy 5"]["Damage"] = input("Enter new damage: ")
print(bad_guys)
#It is up to you to decide what properties are important and the theme of the game.