import os
from colorama import Fore, Style, init
import character as ch
import failsafe as fs
import google_sheet as gs
import item as it
import racial_classes as rc
import job_classes as jc
import gamelogic as gl
import saveloader as sl
import obstacle as ob
import copy
import effects as ef
import ast
import spell as sp

init(autoreset=True)

def create_savefolder(directory):
    if not os.path.exists(directory):
        print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} Creating new saves folder...")
        os.makedirs(directory)
        if os.path.exists(directory):
            print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} New directory called {directory} has been created")
        else:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} New directory {directory} could not be created.")

def save_check(file_path) -> bool:
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    with open(file_path, "r", encoding="utf-8") as file:
        for index, line in enumerate(lines):
            if not line.startswith("//"):
                print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} An error occured within the save file at line {index+1}")
                return False
    return True


def save_all(directory: str, players: list[object]):
    file_path = os.path.join(directory, "characters_temp.txt")
    true_path = os.path.join(directory, "characters.txt")
    with open(true_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    with open(file_path, "w", encoding="utf-8") as save:
        for line in lines:
            save.write(line)
    for player in players:
        print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} Saving {player.firstname}")
        save_character(directory, player)
    if save_check(file_path):
        os.remove(true_path)
        os.rename(file_path, true_path)

def save_character(directory: str, character: object):
    create_savefolder(directory)
    c = character
    character_found = False
    character_id = "characters_temp.txt"
    file_path = os.path.join(directory, character_id)

    # Read the file and store lines in a list
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    with open(file_path, "w", encoding="utf-8") as save:
        for line in lines:
            if line.startswith("*"):
                continue
            spirits = []
            if not c.character_type == "spirit":
                for index, spirit in enumerate(c.spirits):
                    if not fs.is_type(spirit, int):
                        spirits.append(spirit.id)
                    else:
                        spirits.append(spirit)
            if f"ID:{c.id}" in line:
                save.write(f"//ID:{c.id}"
                            f"//Firstname:{c.firstname}"
                            f"//Surname:{c.surname}"
                            f"//Nicknames:{c.nicknames}"
                            f"//Type:{c.character_type}"
                            f"//RaceType:{c.race_type}"
                            f"//Occupation:{c.occupation}"
                            f"//Residence:{c.residence}"
                            f"//Attribute:{c.attribute}"
                            f"//BalanceBreaker:{c.balance_breaker}"
                            f"//Spirits:{spirits}"
                            f"//Master:{c.master}"
                            f"//VasselSlot:{c.equip_slot}"
                            f"//Races:{c.racial_classes}"
                            f"//Jobs:{c.job_classes}"
                            f"//Power:{c.power_level}"
                            f"//Karma:{c.karma}"
                            f"//Religion:{c.religion}"
                            f"//HP:{c.hp}"
                            f"//MP:{c.mp}"
                            f"//SP:{c.sp}"
                            f"//PHY.ATK:{c.phyatk}"
                            f"//PHY.DEF:{c.phydef}"
                            f"//Agility:{c.agility}"
                            f"//Finess:{c.finess}"
                            f"//MAG.ATK:{c.magatk}"
                            f"//MAG.DEF:{c.magdef}"
                            f"//Resistance:{c.resistance}"
                            f"//Special:{c.special}"
                            f"//Athletics:{c.athletics}"
                            f"//Acrobatics:{c.acrobatics}"
                            f"//Stealth:{c.stealth}"
                            f"//Sleight:{c.sleight}"
                            f"//Investigation:{c.investigation}"
                            f"//Insight:{c.insight}"
                            f"//Perception:{c.perception}"
                            f"//Deception:{c.deception}"
                            f"//Intimidation:{c.intimidation}"
                            f"//Persuasion:{c.persuasion}"
                            f"//Performance:{c.performance}"
                            f"//Weight:({c.weight}, {c.max_weight})"
                            f"//Gold:({c.gold}, {c.silver}, {c.bronze})"
                            f"//Inventory:{c.inventory}"
                            f"//Equipment:({c.equipment_h}, {c.equipment_c}, {c.equipment_l}, {c.equipment_s}, {c.equipment_g}, {c.equipment_be}, {c.equipment_rh}, {c.equipment_lh}, {c.equipment_n}, {c.equipment_r1}, {c.equipment_r2}, {c.equipment_br})\n")
                print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} Character Updated")
                character_found = True
            else:
                save.write(line)
        if not character_found:
            save.write(f"//ID:{c.id}"
                            f"//Firstname:{c.firstname}"
                            f"//Surname:{c.surname}"
                            f"//Nicknames:{c.nicknames}"
                            f"//Type:{c.character_type}"
                            f"//RaceType:{c.race_type}"
                            f"//Occupation:{c.occupation}"
                            f"//Residence:{c.residence}"
                            f"//Attribute:{c.attribute}"
                            f"//BalanceBreaker:{c.attribute}"
                            f"//Spirits:{c.spirits}"
                            f"//Master:{c.master}"
                            f"//VasselSlot:{c.equip_slot}"
                            f"//Races:{c.racial_classes}"
                            f"//Jobs:{c.job_classes}"
                            f"//Power:{c.power_level}"
                            f"//Karma:{c.karma}"
                            f"//Religion:{c.religion}"
                            f"//HP:{c.hp}"
                            f"//MP:{c.mp}"
                            f"//SP:{c.sp}"
                            f"//PHY.ATK:{c.phyatk}"
                            f"//PHY.DEF:{c.phydef}"
                            f"//Agility:{c.agility}"
                            f"//Finess:{c.finess}"
                            f"//MAG.ATK:{c.magatk}"
                            f"//MAG.DEF:{c.magdef}"
                            f"//Resistance:{c.resistance}"
                            f"//Special:{c.special}"
                            f"//Athletics:{c.athletics}"
                            f"//Acrobatics:{c.acrobatics}"
                            f"//Stealth:{c.stealth}"
                            f"//Sleight:{c.sleight}"
                            f"//Investigation:{c.investigation}"
                            f"//Insight:{c.insight}"
                            f"//Perception:{c.perception}"
                            f"//Deception:{c.deception}"
                            f"//Intimidation:{c.intimidation}"
                            f"//Persuasion:{c.persuasion}"
                            f"//Performance:{c.performance}"
                            f"//Weight:({c.weight}, {c.max_weight})"
                            f"//Gold:({c.gold}, {c.silver}, {c.bronze})"
                            f"//Inventory:{c.inventory}"
                            f"//Equipment:({c.equipment_h}, {c.equipment_c}, {c.equipment_l}, {c.equipment_s}, {c.equipment_g}, {c.equipment_be}, {c.equipment_rh}, {c.equipment_lh}, {c.equipment_n}, {c.equipment_r1}, {c.equipment_r2}, {c.equipment_br})\n")
    print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} Character {c.id} saved to {directory}.")

def load_characters(directory: str):
    create_savefolder(directory)
    character_id = "characters.txt"
    file_path = os.path.join(directory, character_id)
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as file:
            pass
    # Define a mapping of keys to the corresponding variable names for the Character class
    attribute_map = {
        "ID": "id",
        "Firstname": "firstname",
        "Surname": "surname",
        "Nicknames": "nicknames",
        "Spirits": "spirits",
        "Master": "master",
        "VasselSlot": "equip_slot",
        "Attribute": "attribute",
        "Races": "racial_classes",
        "Jobs": "job_classes",
        "Power": "power_level",
        "Karma": "karma",
        "Type": "character_type",
        "Religion": "religion",
        "BalanceBreaker": "balance_breaker",
        "Residence": "residence",
        "Occupation": "occupation",
        "RaceType": "race_type",
        "Inventory": "inventory",
        "Equipment": "equipment",
        "Weight": "weight",
        "Gold": "gold",
        "HP": "hp",
        "MP": "mp",
        "SP": "sp",
        "PHY.ATK": "phyatk",
        "PHY.DEF": "phydef",
        "Agility": "agility",
        "Finess": "finess",
        "MAG.ATK": "magatk",
        "MAG.DEF": "magdef",
        "Resistance": "resistance",
        "Special": "special",
        "Athletics": "athletics",
        "Acrobatics": "acrobatics",
        "Stealth": "stealth",
        "Sleight": "sleight",
        "Perception": "perception",
        "Deception": "deception",
        "Intimidation": "intimidation",
        "Persuasion": "persuasion",
        "Performance": "performance"
    }

    equipment_ids = ["h", "c", "l", "s", "g", "be", "rh", "lh", "n", "r1", "r2", "br"]

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("*"):
                continue

            # Initialize a dictionary to store character attributes
            character_data = {
                'id': None,
                'firstname': None,
                'surname': None,
                'nicknames': [],
                'attribute': [],
                'racial_classes': [],
                'job_classes': [],
                'balance_breaker': [],
                'spirits': [],
                'master': None,
                'equip_slot': [],
                'power_level': 0,
                'residence': None,
                'race_type': None,
                'occupation': None,
                'karma': 0,
                'religion': None,
                'character_type': None,
                'inventory': [],
                'equipment_h': None,
                'equipment_c': None,
                'equipment_l': None,
                'equipment_s': None,
                'equipment_g': None,
                'equipment_be': None,
                'equipment_rh': None,
                'equipment_lh': None,
                'equipment_n': None,
                'equipment_r1': None,
                'equipment_r2': None,
                'equipment_br': None,
                'weight': 0,
                'gold': 0,
                'silver': 0,
                'bronze': 0,
                'max_weight': 0,
                'hp': 0,
                'mp': 0,
                'sp': 0,
                'phyatk': 0,
                'phydef': 0,
                'agility': 0,
                'finess': 0,
                'magatk': 0,
                'magdef': 0,
                'resistance': 0,
                'special': 0,
                'athletics': 0,
                'acrobatics': 0,
                'stealth': 0,
                'sleight': 0,
                'perception': 0,
                'deception': 0,
                'intimidation': 0,
                'persuasion': 0,
                'performance': 0
            }

            # Remove newline and split the string by the '//' delimiter
            line = line.strip()
            attributes = line.split('//')

            # Iterate over each attribute in the line
            for attr in attributes:
                if attr:
                    key, value = attr.split(':', 1)
                    key = key.strip()
                    value = value.strip()

                    # Map the key to the corresponding variable using the attribute_map
                    if key in attribute_map:
                        var_name = attribute_map[key]

                        # Assign the value, converting to appropriate types
                        if key in ["Races", "Jobs", "Inventory"]:
                            character_data[var_name] = eval(value)  # List of tuples
                        elif key in ["Attribute", "Nicknames", "Spirits", "BalanceBreaker", "VasselSlot"]:
                            try:
                                # Try to evaluate value as a list
                                evaluated_value = eval(value)
                                # If evaluated value is a list but is empty or just whitespace, treat it as an empty list
                                if isinstance(evaluated_value, list) and not evaluated_value:
                                    character_data[var_name] = []
                                else:
                                    character_data[var_name] = evaluated_value
                            except:
                                # If eval fails, treat as a comma-separated string and split into a list
                                character_data[var_name] = [item.strip() for item in value.split(",") if item.strip()]
                        elif key == "Weight":
                            weight = eval(value)
                            character_data['weight'], character_data['max_weight'] = weight
                        elif key == "Gold":
                            gold = eval(value)
                            character_data['gold'], character_data['silver'], character_data['bronze'] = gold
                        elif key == "Equipment":
                            equipment_data = eval(value)
                            for slot, equipment in zip(equipment_ids, equipment_data):
                                if equipment:
                                    equipment_key = f"equipment_{slot}"
                                    character_data[equipment_key] = equipment
                        elif value.isdigit():
                            character_data[var_name] = int(value)
                        else:
                            character_data[var_name] = value

            # Create a Character object using the character_data dictionary
            character = ch.Character(
                id=character_data['id'],
                firstname=character_data['firstname'],
                surname=character_data['surname'],
                nicknames=character_data['nicknames'],
                spirits=character_data['spirits'],
                master=character_data['master'],
                equip_slot=character_data['equip_slot'],
                attribute=character_data['attribute'],
                racial_classes=character_data['racial_classes'],
                job_classes=character_data['job_classes'],
                power_level=character_data['power_level'],
                residence=character_data['residence'],
                occupation=character_data['occupation'],
                race_type=character_data['race_type'],
                karma=character_data['karma'],
                character_type=character_data['character_type'],
                balance_breaker=character_data['balance_breaker'],
                religion=character_data['religion'],
                inventory=character_data['inventory'],
                equipment_h=character_data['equipment_h'],
                equipment_c=character_data['equipment_c'],
                equipment_l=character_data['equipment_l'],
                equipment_s=character_data['equipment_s'],
                equipment_g=character_data['equipment_g'],
                equipment_be=character_data['equipment_be'],
                equipment_rh=character_data['equipment_rh'],
                equipment_lh=character_data['equipment_lh'],
                equipment_n=character_data['equipment_n'],
                equipment_r1=character_data['equipment_r1'],
                equipment_r2=character_data['equipment_r2'],
                equipment_br=character_data['equipment_br'],
                weight=character_data['weight'],
                gold=character_data['gold'],
                silver=character_data['silver'],
                bronze=character_data['bronze'],
                max_weight=character_data['max_weight'],
                hp=character_data['hp'],
                mp=character_data['mp'],
                sp=character_data['sp'],
                phyatk=character_data['phyatk'],
                phydef=character_data['phydef'],
                agility=character_data['agility'],
                finess=character_data['finess'],
                magatk=character_data['magatk'],
                magdef=character_data['magdef'],
                resistance=character_data['resistance'],
                special=character_data['special'],
                athletics=character_data['athletics'],
                acrobatics=character_data['acrobatics'],
                stealth=character_data['stealth'],
                sleight=character_data['sleight'],
                perception=character_data['perception'],
                deception=character_data['deception'],
                intimidation=character_data['intimidation'],
                persuasion=character_data['persuasion'],
                performance=character_data['performance']
            )

def update_sheet(player: object):
    print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} Updating sheet for {player.firstname}...")

    sheet = f"wotv player {player.id}"
    blb = []
    rcn = []
    rcl = []
    jcn = []
    jcl = []
    invn = []
    inva = []
    att = []
    nick = []
    gold = []


    if player.balance_breaker:
        for i in player.balance_breaker:
            blb.append(i)
    if player.racial_classes:
        for i in player.racial_classes:
            name, level = i
            race = rc.race_list(name, level)
            name = race.name
            rcn.append(name)
            rcl.append(level)
    if player.job_classes:
        for i in player.job_classes:
            name, level = i
            job = jc.job_list(name, level)
            name = job.name
            jcn.append(name)
            jcl.append(level)
    if player.inventory:
        for i in player.inventory:
            name, amount = i
            if fs.is_type(name, tuple):
                name, level = name
                item = it.item_list(name, level)
                name = item.name
                invn.append(name)
            else:
                item = it.item_list(name, 2)
                name = item.name
                invn.append(name)
            inva.append(amount)
    if player.attribute:
        for i in player.attribute:
            att.append(i)
    if player.nicknames:
        for i in player.nicknames:
            nick.append(i)
    gold.append(player.gold)
    gold.append(player.silver)
    gold.append(player.bronze)

    # Equipment
    equipment_ids = gl.EQUIPMENT_SLOTS_S
    equip_data = []
    for i in equipment_ids:
        equip_name = f"equipment_{i}"
        equipment = getattr(player, equip_name, None)
        if equipment is not None:
            if not fs.is_type(equipment, tuple):
                equip_data.append(["Spirit", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
                continue
            equip_name, equip_level = equipment
            eq = it.item_list(equip_name, equip_level)
            equipment_attrib = [eq.name, eq.hp, eq.mp, eq.sp, eq.phyatk, eq.phydef, eq.agility, eq.finess, eq.magatk, eq.magdef, eq.resistance, eq.special, eq.athletics, eq.acrobatics, eq.stealth, eq.sleight, eq.investigation, eq.insight, eq.perception, eq.deception, eq.intimidation, eq.persuasion, eq.performance]
            equip_data.append(equipment_attrib)
        else:
            equip_data.append(["", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    # Effects
    status_effects = [["", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] for i in range(17)]
    last_index = 0
    if player.status_effects:
        for index, e in enumerate(player.status_effects):
            status_effects[index] = [e.name, e.new_hp, e.new_mp, e.new_sp, e.new_phyatk, e.new_phydef, e.new_agility, e.new_finess, e.new_magatk, e.new_magdef, e.new_resistance, e.new_special, e.new_athletics, e.new_acrobatics, e.new_stealth, e.new_sleight, e.new_investigation, e.new_insight, e.new_perception, e.new_deception, e.new_intimidation, e.new_persuasion, e.new_performance, e.time_left]
            last_index = index
    if player.abilities:
        for index, a in enumerate(player.abilities):
            status_effects[last_index+index+1] = [a.name, a.hp, a.mp, a.mp, a.phyatk, a.phydef, a.agility, a.finess, a.magatk, a.magdef, a.resistance, a.special, a.athletics, a.acrobatics, a.stealth, a.sleight, a.investigation, a.insight, a.perception, a.deception, a.intimidation, a.persuasion, a.performance, a.time]

    data = gs.create_matrix(blb, rcn, rcl, jcn, jcl, invn, inva, att, nick, gold)

    update_data = [
        {"range": "A2:V5", "values": [
            [player.hp, player.mp, player.sp, player.phyatk, player.phydef, player.agility, player.finess, player.magatk, player.magdef, player.resistance, player.special, player.athletics, player.acrobatics, player.stealth, player.sleight, player.investigation, player.insight, player.perception, player.deception, player.intimidation, player.persuasion, player.performance],
            [player.new_hp, player.new_mp, player.new_sp, player.new_phyatk, player.new_phydef, player.new_agility, player.new_finess, player.new_magatk, player.new_magdef, player.new_resistance, player.new_special, player.new_athletics, player.new_acrobatics, player.new_stealth, player.new_sleight, player.new_investigation, player.new_insight, player.new_perception, player.new_deception, player.new_intimidation, player.new_persuasion, player.new_performance],
            [player.max_hp, player.max_mp, player.max_sp, player.max_phyatk, player.max_phydef, player.max_agility, player.max_finess, player.max_magatk, player.max_magdef, player.max_resistance, player.max_special, player.max_athletics, player.max_acrobatics, player.max_stealth, player.max_sleight, player.max_investigation, player.max_insight, player.max_perception, player.max_deception, player.max_intimidation, player.max_persuasion, player.max_performance]
        ]},
        {"range": "A6:L6", "values": [
            [player.id, player.firstname, player.surname, player.karma, player.religion, player.weight, player.max_weight, player.power_level, player.armor_class, player.race_type, player.occupation, player.residence]
        ]},
        {"range": "M6:Y39", "values": data},
        {"range": "B41:X52", "values": equip_data},
        {"range": "B54:Y70", "values": status_effects}
    ]

    # Prepare the batch update request for multiple ranges
    update_requests = [
        {
            "range": item["range"],
            "values": item["values"]
        }
        for item in update_data
    ]

    # Perform batch update
    gs.google_batch_update(sheet, update_requests)


def load_spirits(players: list[object], load: bool = False) -> list[object]:
    summons = []
    for p in players:
        player_spirits = []
        print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} Uploading Spirits for {p.prefix}...")
        for index, spirit in enumerate(p.spirits):
            if not fs.is_type(spirit, int):
                spirit = spirit.id
            summon = ch.character_dic[str(spirit)]
            if not load:
                summon.prefix = input(f"Assign Prefix for Spirit {summon.firstname}: ").upper()
                summon.vassel = False
            summons.append(summon)
            player_spirits.append(summon)
            for attrib in summon.attribute:
                if attrib not in p.attribute:
                    p.attribute.append(attrib)
        p.spirits = player_spirits
    print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} Upload Spirits: {Fore.GREEN}[Completed]{Style.RESET_ALL}")
    return summons

def update_spirit(spirit: object, mode="start") -> None:
    player = ch.character_dic.get(spirit.master)
    if not fs.is_player(spirit.master):
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Spirit could not be updated because of: {Fore.RED}[INCORRECT VAR TYPE]{Style.RESET_ALL}")
        return
    if mode == "start":
        spirit_reset(spirit, player)
    spirit_check(spirit, player)


def spirit_reset(spirit: object, player: object):
    attributes: list = gl.STATS + gl.SKILLS
    old_multiplier = 1
    for job_class in player.job_classes:
        name, level = job_class
        if name == "spirit_tamer" or name == "greater_spirit_tamer" or name == "master_spirit_tamer":
            old_multiplier += level*0.02
    for attribute in attributes:
        if fs.is_attrib(spirit, f"new_{attribute}"):
            spirit_attrib = getattr(spirit, f"new_{attribute}")
            max_spirit_attrib = getattr(spirit, f"max_{attribute}")
            max_player_attrib = getattr(player, f"max_{attribute}")

            new_multiplier = old_multiplier + (max_player_attrib*0.01)/3

            setattr(spirit, f"new_{attribute}", round(spirit_attrib/new_multiplier))
            setattr(spirit, f"max_{attribute}", round(max_spirit_attrib/new_multiplier))
    

def spirit_check(spirit: object, player: object):
    attributes: list = gl.STATS + gl.SKILLS
    old_multiplier = 1
    for job_class in player.job_classes:
        name, level = job_class
        if name == "spirit_tamer" or name == "greater_spirit_tamer" or name == "master_spirit_tamer":
            old_multiplier += level*0.02
    for attribute in attributes:
        if fs.is_attrib(spirit, f"new_{attribute}"):
            spirit_attrib = getattr(spirit, f"new_{attribute}")
            max_spirit_attrib = getattr(spirit, f"max_{attribute}")
            max_player_attrib = getattr(player, f"max_{attribute}")

            new_multiplier = old_multiplier + (max_player_attrib*0.01)/3

            setattr(spirit, f"new_{attribute}", round(spirit_attrib*new_multiplier))
            setattr(spirit, f"max_{attribute}", round(max_spirit_attrib*new_multiplier))

def load_summons() -> list[object]:
    summons = []
    for play in ch.character_dic:
        player: object = ch.character_dic.get(play)
        if player.character_type == "summon":
            summons.append(player)
    return summons

def disp_files(dir: str, file_name: str, file_suf: str) -> str:
    file_list = []
    sl.create_savefolder(dir)
    files = os.listdir(dir)
    for name in files:
        if name.startswith(file_name):
            file_list.append(name.removeprefix(file_name).removesuffix(file_suf))

    if not file_list:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} No files found in {dir}...")
        return

    for i, file in enumerate(file_list):
        print(f"[{i+1}] {file}")

    while True:
        choice = fs.is_int(input("Choose file: "))
        if 1 <= choice <= len(file_list):
            file = f"{file_name}{file_list[choice-1]}{file_suf}"
            return file

def load_scenario(scenario_name: str):
    assigned_players = []
    player_objects = []
    player_prefixes = {}
    player_effects = []

    file_path = os.path.join("scenario_saves", scenario_name)
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as file:
            pass
    
    scenario_map = {
        "Name": "name",
        "Mode": "mode",
        "Turn": "turn",
        "Player Turn": "playerturn",
        "Obstacles": "obstacles"
    }

    scenario_data = {
        'name': None,
        'turn': 0,
        'players': [],
        'playerturn': 0,
        'mode': None,
        'obstacles': {}
    }

    attribute_map = {
        "Karma": "new_karma",
        "HP": "new_hp",
        "MP": "new_mp",
        "SP": "new_sp",
        "PHY.ATK": "new_phyatk",
        "PHY.DEF": "new_phydef",
        "Agility": "new_agility",
        "Finess": "new_finess",
        "MAG.ATK": "new_magatk",
        "MAG.DEF": "new_magdef",
        "Resistance": "new_resistance",
        "Special": "new_special",
        "Athletics": "new_athletics",
        "Acrobatics": "new_acrobatics",
        "Stealth": "new_stealth",
        "Sleight": "new_sleight",
        "Perception": "new_perception",
        "Deception": "new_deception",
        "Intimidation": "new_intimidation",
        "Persuasion": "new_persuasion",
        "Performance": "new_performance",
        "MAX Karma": "max_karma",
        "MAX HP": "max_hp",
        "MAX MP": "max_mp",
        "MAX SP": "max_sp",
        "MAX PHY.ATK": "max_phyatk",
        "MAX PHY.DEF": "max_phydef",
        "MAX Agility": "max_agility",
        "MAX Finess": "max_finess",
        "MAX MAG.ATK": "max_magatk",
        "MAX MAG.DEF": "max_magdef",
        "MAX Resistance": "max_resistance",
        "MAX Special": "max_special",
        "MAX Athletics": "max_athletics",
        "MAX Acrobatics": "max_acrobatics",
        "MAX Stealth": "max_stealth",
        "MAX Sleight": "max_sleight",
        "MAX Perception": "max_perception",
        "MAX Deception": "max_deception",
        "MAX Intimidation": "max_intimidation",
        "MAX Persuasion": "max_persuasion",
        "MAX Performance": "max_performance",
        "Status Effects": "status_effects",
        "Team": "team",
        "Prefix": "prefix",
        "Initiative": "initiative",
        "Cooldowns": "cooldowns",
        "Barriers": "barriers",
        "Vassel": "vassel",
    }

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("*"):
                continue
            elif line.startswith("Init"):  # INIT
                info = line.split("/&/")
                info = info[1].split("//")
                for attr in info:
                    if not attr:
                        continue
                    key, value = attr.split(":", 1)
                    key = key.strip()
                    value = value.strip()

                    if not key in scenario_map:
                        continue
                    var_name = scenario_map[key]

                    if key in ["Obstacles"]:
                        obstacles_dict = {}
                        obstacles: list[list[str, str, int]] = ast.literal_eval(value)  # Prefix, Name, HP
                        for obs in obstacles:
                            prefix, name, hp = obs
                            obstacle: object = ob.obstacle_list(name)
                            obstacle.prefix = prefix
                            obstacle.new_hp = obstacle.max_hp = hp
                            obstacle.new_phydef = obstacle.max_phydef = obstacle.phydef
                            obstacle.new_magdef = obstacle.max_magdef = obstacle.magdef
                            obstacle.status_effects = []
                            obstacle.cooldowns = {}
                            obstacle.barriers = []
                            obstacles_dict[prefix] = obstacle
                        scenario_data[var_name] = obstacles_dict
                    elif value.isdigit():
                        scenario_data[var_name] = int(value)  # For integers
                    else:
                        scenario_data[var_name] = value  # For strings

            elif line.startswith("Player"):  # PLAYER

                character_data = {
                    'new_karma': 0,
                    'new_hp': 0,
                    'new_mp': 0,
                    'new_sp': 0,
                    'new_phyatk': 0,
                    'new_phydef': 0,
                    'new_agility': 0,
                    'new_finess': 0,
                    'new_magatk': 0,
                    'new_magdef': 0,
                    'new_resistance': 0,
                    'new_special': 0,
                    'new_athletics': 0,
                    'new_acrobatics': 0,
                    'new_stealth': 0,
                    'new_sleight': 0,
                    'new_perception': 0,
                    'new_deception': 0,
                    'new_intimidation': 0,
                    'new_persuasion': 0,
                    'new_performance': 0,
                    'max_karma': 0,
                    'max_hp': 0,
                    'max_mp': 0,
                    'max_sp': 0,
                    'max_phyatk': 0,
                    'max_phydef': 0,
                    'max_agility': 0,
                    'max_finess': 0,
                    'max_magatk': 0,
                    'max_magdef': 0,
                    'max_resistance': 0,
                    'max_special': 0,
                    'max_athletics': 0,
                    'max_acrobatics': 0,
                    'max_stealth': 0,
                    'max_sleight': 0,
                    'max_perception': 0,
                    'max_deception': 0,
                    'max_intimidation': 0,
                    'max_persuasion': 0,
                    'max_performance': 0,
                    'status_effects': [],
                    'cooldowns': {},
                    'barriers': [],
                    'initiative': 0,
                    'team': None,
                    'prefix': "foo",
                    'vassel': False
                }

                info = line.split("/&/")
                info = info[1].split("//")

                p_id = info[0].split(":")[1] # Expects Player ID in the first attribute
                player: object = ch.character_dic.get(str(p_id))  # PLAYER
                player.barriers = []
                player.cooldowns = {}
                if player is None:
                    print(f"{Fore.RED}[WARNING]{Style.RESET_ALL} PLAYER NOT FOUND, SKIPPING PLAYER WITH ID {p_id}")
                    continue

                # Add Attributes to dictionary
                for attr in info:
                    if not attr:
                        continue
                    key, value = attr.split(":", 1)
                    key = key.strip()
                    value = value.strip()

                    if key not in attribute_map:
                        continue
                    var_name = attribute_map[key]

                    if key in ["Status Effects"]:
                        effects: list[list[str, int, float, bool, str, bool, int, int]] = ast.literal_eval(value)  # Name, turns, success, use_effect, use_religion, affect_max, effect, spell_effect
                        status_effects: list = []
                        if effects:
                            for effect in effects:
                                effect_seff = effect.pop()
                                effect_eff = effect.pop()
                                status_effect: object = ef.effect_list(*effect)
                                status_effects.append(status_effect)
                                status_effect.effect = effect_eff
                                status_effect.spell_effect = effect_seff
                                status_effect.apply_bonus(player)
                        character_data[var_name] = status_effects
                    elif key in ["Cooldowns"]:
                        character_data[var_name] = ast.literal_eval(value)
                    elif key in ["Vassel"]:
                        if player.character_type == "spirit":
                            character_data[var_name] = ast.literal_eval(value)
                        else:
                            character_data[var_name] = None
                    elif key in ["Barriers"]:
                        barriers: list[tuple[str, int, int, int, int]] = ast.literal_eval(value)  # (name, turns, hp, phydef, magdef)
                        for barrier in barriers:
                            s_name, s_turns, s_hp, s_phydef, s_magdef = barrier
                            upload_barrier = sp.Spell(s_name, "Barrier", 1, 1, s_turns, "magatk", "Mana", True, hp=s_hp, phydef=s_phydef, magdef=s_magdef, status=[ef.effect_list(s_name, s_turns, 1)])
                            upload_barrier.new_hp = s_hp

                            player_effects.append(upload_barrier)
                    elif value.isdigit():
                        character_data[var_name] = int(value)  # For integers
                    else:
                        character_data[var_name] = value  # For Strings

                # Add to lists
                if player.id in assigned_players:
                    assigned_player: object = copy.deepcopy(player)
                else:
                    assigned_player: object = player

                # Update attributes on character
                for attr, value in character_data.items():
                    setattr(assigned_player, attr, value)
                for effe in player_effects:
                    for bari in effe.statuses:
                        assigned_player.status_effects.append(bari)
                    assigned_player.barriers.append(effe)
                assigned_player.cooldowns = character_data["cooldowns"]

                if assigned_player.id in assigned_players:
                    print(f"{Fore.RED}[WARNING]{Style.RESET_ALL} Player is already registered, registgering multiple")
                
                if character_data["prefix"] in player_prefixes:
                    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Prefix already taken, skipping registry")
                    continue
                assigned_player.prefix = character_data["prefix"]
                if assigned_player.id not in assigned_players:
                    assigned_players.append(assigned_player.id)
                player_objects.append(assigned_player)
                player_prefixes[character_data["prefix"]] = assigned_player
                player_effects.clear()
        scenario = (scenario_data["name"], scenario_data["turn"], player_objects, scenario_data["playerturn"], scenario_data["mode"], scenario_data["obstacles"])
    
    return assigned_players, player_objects, player_prefixes, scenario

def save_scenario(scenario: object) -> None:
    create_savefolder("scenario_saves")
    s: object = scenario
    save_file: str = f"scenario_{s.name}.txt"
    file_path = os.path.join("scenario_saves", save_file)

    # CHECK IF FILE EXISTS
    if os.path.exists(file_path):
        os.remove(file_path)
    
    with open(file_path, "w", encoding="utf-8") as save:
        # INIT
        obstacles = []
        for key, obs in s.obstacles.items():
            obstacles.append([key, gl.uncapitalize_string(obs.firstname, " "), obs.new_hp])

        save.write(f"Init/&/"
                   f"Name:{s.name}"
                   f"//Mode:{s.mode}"
                   f"//Turn:{s.turn}"
                   f"//Player Turn:{s.playerturn}"
                   f"//Obstacles:{obstacles}\n")
        
        # PLAYERS
        for p in s.players:
            effects: list[object] = [eff for eff in p.status_effects]
            barriers: list[str] = [bari.barrier_repr for bari in p.barriers]
            save.write(f"Player/&/"
                       f"ID:{p.id}"
                       f"//Initiative:{p.initiative}"
                       f"//Karma:{p.new_karma}"
                       f"//HP:{p.new_hp}"
                       f"//MP:{p.new_mp}"
                       f"//SP:{p.new_sp}"
                       f"//PHY.ATK:{p.new_phyatk}"
                       f"//PHY.DEF:{p.new_phydef}"
                       f"//Agility:{p.new_agility}"
                       f"//Finess:{p.new_finess}"
                       f"//MAG.ATK:{p.new_magatk}"
                       f"//MAG.DEF:{p.new_magdef}"
                       f"//Resistance:{p.new_resistance}"
                       f"//Special:{p.new_special}"
                       f"//Athletics:{p.new_athletics}"
                       f"//Acrobatics:{p.new_acrobatics}"
                       f"//Stealth:{p.new_stealth}"
                       f"//Sleight:{p.new_sleight}"
                       f"//Investigation:{p.new_investigation}"
                       f"//Insight:{p.new_insight}"
                       f"//Perception:{p.new_perception}"
                       f"//Deception:{p.new_deception}"
                       f"//Intimidation:{p.new_intimidation}"
                       f"//Persuasion:{p.new_persuasion}"
                       f"//Performance:{p.new_performance}"
                       f"//MAX Karma:{p.max_karma}"
                       f"//MAX HP:{p.max_hp}"
                       f"//MAX MP:{p.max_mp}"
                       f"//MAX SP:{p.max_sp}"
                       f"//MAX PHY.ATK:{p.max_phyatk}"
                       f"//MAX PHY.DEF:{p.max_phydef}"
                       f"//MAX Agility:{p.max_agility}"
                       f"//MAX Finess:{p.max_finess}"
                       f"//MAX MAG.ATK:{p.max_magatk}"
                       f"//MAX MAG.DEF:{p.max_magdef}"
                       f"//MAX Resistance:{p.max_resistance}"
                       f"//MAX Special:{p.max_special}"
                       f"//MAX Athletics:{p.max_athletics}"
                       f"//MAX Acrobatics:{p.max_acrobatics}"
                       f"//MAX Stealth:{p.max_stealth}"
                       f"//MAX Sleight:{p.max_sleight}"
                       f"//MAX Investigation:{p.max_investigation}"
                       f"//MAX Insight:{p.max_insight}"
                       f"//MAX Perception:{p.max_perception}"
                       f"//MAX Deception:{p.max_deception}"
                       f"//MAX Intimidation:{p.max_intimidation}"
                       f"//MAX Persuasion:{p.max_persuasion}"
                       f"//MAX Performance:{p.max_performance}"
                       f"//Status Effects:{effects}"
                       f"//Team:{p.team}"
                       f"//Prefix:{p.prefix}"
                       f"//Cooldowns:{p.cooldowns}"
                       f"//Barriers:{barriers}"
                       f"//Vassel:{p.vassel}\n")
            print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} Character {p.prefix} {p.firstname} saved in scenario.")
    print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} Scenario {s.name} saved successfuly.")
