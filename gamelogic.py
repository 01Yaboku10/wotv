import os
from colorama import Fore, Style, init
import character as ch
import failsafe as fs
import random
import copy

init(autoreset=True)
SKILLS = ["athletics", "acrobatics", "stealth", "sleight", "investigation", "insight", "perception", "deception", "intimidation", "persuasion", "performance", "max_weight"]

def log_clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def team_assign(players: list[object]) -> tuple[list[object], list[object]]:
    print("---------=Assign Teams=---------")
    for index, character in enumerate(players):
        print(f"[{index+1}] ID:{character.id} {character.firstname}")
    print("--=Assign players for Team 1=--")
    while True:
        choice = input("Assign id ([D]one): ").upper()
        if choice == "D":
            break
        if not choice.isdigit():
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Not integer")
            continue
        choice = int(choice)
        if 1 <= choice <= len(players):
            player = players[choice-1]
            player.team = 1
    print("--=Assign players for Team 2=--")
    while True:
        choice = input("Assign id ([D]one): ").upper()
        if choice == "D":
            break
        if not choice.isdigit():
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Not integer")
            continue
        choice = int(choice)
        if 1 <= choice <= len(players):
            player = players[choice-1]
            player.team = 2

def player_assign(players: list[object] = None) -> tuple[list[int], list[object]]:
    print("---------=Assign Players=---------")
    assigned_players = []
    player_objects = []
    player_prefixes = {}
    new_players = []

    # Check for already existing players
    if players is not None:
        for pl in players:
            assigned_players.append(pl.id)
            player_objects.append(pl)
            player_prefixes[pl.prefix] = pl
    
    for pla in ch.character_dic:
        pla = int(pla)
        if pla not in assigned_players:
            new_players.append(str(pla))

    for index, play in enumerate(ch.character_dic):
        player = ch.character_dic.get(play)
        print(f"[{index+1}] ID:{player.id}, {player.firstname}")

    while True:
        choice = input("Assign id ([D]one): ").upper()
        if choice == "D":
            break
        if not choice.isdigit():
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Not integer")
            return
        if 1 <= int(choice) <= len(list(ch.character_dic.keys())):
            player: object = ch.character_dic[list(ch.character_dic.keys())[int(choice)-1]]
            if player.id in assigned_players:
                assigned_player: object = copy.deepcopy(player)
            else:
                assigned_player: object = player
            if assigned_player.id in assigned_players:
                while True:
                    multi = input(f"{Fore.RED}[WARNING]{Style.RESET_ALL} Player is already registered, register multiple? [Y/N]: ").upper()
                    if multi == "N":
                        break
                    elif multi == "Y":
                        break
                if multi == "N":
                    continue
            while True:
                prefix = input("Assign board piece: ").upper()
                if prefix in player_prefixes:
                    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Prefix already taken.")
                    continue
                assigned_player.prefix = prefix
                if assigned_player.id not in assigned_players:
                    assigned_players.append(assigned_player.id)
                player_objects.append(assigned_player)
                player_prefixes[prefix] = assigned_player
                break
        else:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Key out of bounce")

    return assigned_players, player_objects, player_prefixes

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