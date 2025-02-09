from colorama import Fore, Style, init
import racial_classes as rc
import job_classes as jc
import character as ch
import spell as sp
import item as it

init(autoreset=True)

def is_int(prompt: str):
    while True:
        try:
            return int(prompt)
        except ValueError:
            print("Invalid Input! Please use a valid integer")
            prompt = input("New value: ")

def is_type(input, type: type) -> bool:
    if isinstance(input, type):
        return True
    else:
        return False
    
def is_attrib(player: object, attribute: str) -> bool:
    if hasattr(player, attribute):
        return True
    else:
        return False

def is_race(race: str) -> bool:
    try:
        return rc.race_list(race, 1)
    except KeyError:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Race does not exist")
        return False
    
def is_spell(spell: str) -> bool:
    try:
        return sp.spell_list(spell)
    except KeyError:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Spell does not exist")
        return False

def is_job(job: str) -> bool:
    try:
        return jc.job_list(job, 1)
    except KeyError:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Job does not exist")
        return False
    
def is_item(item: str) -> bool:
    try:
        return it.item_list(item, 1)
    except KeyError:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Item does not exist")
        return False

def is_slot_taken(player: object, slot: str) -> bool:
    target_slot: tuple[str, int] = getattr(player, slot, None)
    if target_slot:
        return True
    else:
        return False

def is_player(player_id: str) -> bool:
    try:
        return ch.character_dic.get(player_id)
    except KeyError:
        return False

def is_saved(file_path, player_id: str) -> bool:
    player_id = "ID:" + str(player_id)
    with open(file_path, "r", encoding="utf-8") as save:
        for line in save:
            if player_id in line:
                return True
        return False

def spell_dice(tier: int) -> int:
    if tier <= 2:
        dice = 4
    elif tier == 3:
        dice = 6
    elif tier == 4:
        dice = 8
    elif tier <= 6:
        dice = 10
    elif tier <= 9:
        dice = 12
    else:
        dice = 20
    return dice
