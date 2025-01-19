import os
import character as ch
import failsafe as fs
import random

def log_clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def team_assign(players: list[object]) -> tuple[list[object], list[object]]:
    print("---------=Assign Teams=---------")
    for index, character in enumerate(players):
            print(f"[{index+1}] ID:{character.id} {character.firstname}")
    team_1 = []
    team_2 = []
    print("--=Assign players for Team 1=--")
    while True:
        choice = input("Assign id ([D]one): ").upper()
        if choice == "D":
            break
        if not choice.isdigit():
            print("ERROR: Not integer")
            continue
        choice = int(choice)
        if 1 <= choice <= len(players):
            player = players[choice-1]
            if player in team_1:
                print("ERROR: Player already registered")
                continue
            team_1.append(player)
    print("--=Assign players for Team 2=--")
    while True:
        choice = input("Assign id ([D]one): ").upper()
        if choice == "D":
            break
        if not choice.isdigit():
            print("ERROR: Not integer")
            continue
        choice = int(choice)
        if 1 <= choice <= len(players):
            player = players[choice-1]
            if player in team_1 or player in team_2:
                print("ERROR: Player already registered")
                continue
            team_2.append(player)
    return team_1, team_2

def player_assign() -> tuple[list[int], list[object]]:
    print("---------=Assign Players=---------")
    assigned_players = []
    player_objects = []
    for index, character in enumerate(ch.character_dic):
            print(f"[{index+1}] ID:{character} {ch.character_dic[character].firstname}")

    while True:
        choice = input("Assign id ([D]one): ").upper()
        if choice == "D":
            break
        if not choice.isdigit():
            print("ERROR: Not integer")
            return
        choice = int(choice)
        if 1 <= choice <= len(ch.character_dic):
            assigned_player = list(ch.character_dic.keys())[choice-1]
            if assigned_player in assigned_players:
                print("ERROR: Player already registered")
                continue
            assigned_players.append(assigned_player)
            player_objects.append(ch.character_dic[assigned_player])

    return assigned_players, player_objects    

def magic_attribute_gen():
    attributes = [
            #  Natrual Elements (weight 10)
            Magic("Fire", 10),
            Magic("Water", 10),
            Magic("Earth", 10),
            Magic("Air", 10),
            Magic("Ice", 10),
            Magic("Nature", 10),
            Magic("Metal", 10),
            Magic("Wood", 10),
            Magic("Stone", 10),
            Magic("Sand", 10),
            Magic("Crystal", 10),
            Magic("Wind", 10),
            Magic("Storm", 10),
            Magic("Thunder", 10),
            Magic("Lava", 10),
            Magic("Mud", 10),
            Magic("Poison", 10),

            #  Ethereal elements (weight 5)
            Magic("Spirit", 5),
            Magic("Holy", 5),
            Magic("Space", 5),
            Magic("Dream", 5),

            #  Abstract elements (weight 1)
            Magic("Chaos", 1),
            Magic("Void", 5),
            Magic("Mind", 1),
            Magic("Time", 1),
            Magic("Illusion", 1),
            Magic("Plague", 1),
            Magic("Mirror", 1),
            Magic("Gravity", 1),
            Magic("Sound", 1),
            Magic("Death", 1),
            Magic("Moon", 1),
            Magic("Sun", 1),
            Magic("Light", 1),
            Magic("Blood", 1),
        ]

    weights = [magic.weight for magic in attributes]

    random_magic = random.choices(attributes, weights=weights, k=1)[0]
    return random_magic.name

class Turnmeter():
    def __init__(self):
        self.currentturn = 1
    def nextturn(self):
        self.currentturn += 1

class Magic():
    def __init__(self, name: str, weight: float):
        self.name = name
        self.weight = weight
