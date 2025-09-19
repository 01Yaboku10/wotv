from colorama import Fore, Style, init
from typing import Iterable, Any
import racial_classes as rc
import job_classes as jc
import character as ch
import spell as sp
import item as it
import abilities as ab
import obstacle as ob
import flooreffect as fe
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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
    
def is_player_prefix(prefix_list: dict, prefix: str = None, extra_text: str = "") -> object:
    while True:
        if prefix is None:
            prefix = input(f"Player prefix{extra_text}: ").upper().strip()
        player: object = prefix_list.get(prefix)
        if player is not None:
            break
        prefix = None
    return player
    
def is_in_iterable(question: str, iterable: Iterable) -> Any:
    """
    Checks if an item exists in an iterable
    """
    while True:
        inputted = input(question)
        if inputted in iterable:
            break
    return inputted
    
def is_max(character: object, attribute: str, effect: int, mode: str = "d") -> list[int, int]: # Effect value, excession
    """Checks if the effect will exceed, if it does, will cap to 100,
    otherwise it will return the value."""
    attri: int = getattr(character, f"new_{attribute}")
    cap = 100
    if mode == "karma":
        cap = 500
    if attri >= 0:
        if attri + effect > cap:
            return [effect, (attri+effect)-cap]
        else:
            return [effect, 0]
    else:
        if attri + effect < cap:
            return [effect, (attri+effect)-cap]
        else:
            return [effect, 0]

def is_sheet(creds: str, sheetname: str):
    try:
        service = build("drive", "v3", credentials=creds)

        result = service.files().list(
            q=f"name = '{sheetname}' and mimeType = 'application/vnd.google-apps.spreadsheet'",
            spaces='drive',
            fields='files(id, name)',
            pageSize=10).execute()

        files = result.get('files', [])

        if not files:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} No sheet found for '{sheetname}'")
            return False

        print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} Sheet found: {files[0]['name']} with ID: {files[0]['id']}")
        return True

    except HttpError as error:
        if error.resp.status == 404:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Sheet not found (404 error)")
            return False
        else:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {error}")
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
    spell = spell.strip().lower()

    try:
        return sp.spell_list(spell)
    except KeyError:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Spell does not exist")
        return False
    
def is_obstacle(obstacle: str) -> bool:
    try:
        return ob.obstacle_list(obstacle)
    except KeyError:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Obstacle does not exist")
        return False

def is_floor(floor: str) -> bool:
    try:
        return fe.floor_list(floor)
    except KeyError:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Floor Effect does not exist")
        return False

def is_ability(ability: str) -> bool:
    try:
        return ab.ability_list(ability)
    except KeyError:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Ability does not exist")
        return False

def is_cooldown(player: object, spell: str) -> int:
    if player.cooldowns:
        for cooldown in player.cooldowns:
            if cooldown == spell:
                return player.cooldowns[cooldown]
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
