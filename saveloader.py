import os
import character as ch
import failsafe as fs
import google_sheet as gs
import item as it

def create_savefolder(directory):
    if not os.path.exists(directory):
        print("DEBUGG: Creating new saves folder...")
        os.makedirs(directory)
        if os.path.exists(directory):
            print(f"DEBUGG: New directory called {directory} has been created")
        else:
            print(f"ERROR: New directory {directory} could not be created.")

def save_all(directory: str, players: list[object]):
    for player in players:
        save_character(directory, player)

def save_character(directory: str, character: object):
    create_savefolder(directory)
    c = character
    character_found = False
    character_id = "characters.txt"
    file_path = os.path.join(directory, character_id)
    
    # Read the file and store lines in a list
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    with open(file_path, "w", encoding="utf-8") as save:
        for line in lines:
            if f"ID:{c.id}" in line:
                save.write(f"//ID:{c.id}"
                            f"//Firstname:{c.firstname}"
                            f"//Surname:{c.surname}"
                            f"//Nicknames:{c.nicknames}"
                            f"//RaceType:{c.race_type}"
                            f"//Occupation:{c.occupation}"
                            f"//Residence:{c.residence}"
                            f"//Attribute:{c.attribute}"
                            f"//BalanceBreaker:{c.attribute}"
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
                            f"//Inventory:{c.inventory}"
                            f"//Equipment:({c.equipment_h}, {c.equipment_c}, {c.equipment_l}, {c.equipment_s}, {c.equipment_g}, {c.equipment_be}, {c.equipment_rh}, {c.equipment_lh}, {c.equipment_n}, {c.equipment_r1}, {c.equipment_r2}, {c.equipment_br})\n")
                print("DEBUGG: Character Updated")
                character_found = True
            else:
                save.write(line)
        if not character_found:
            save.write(f"//ID:{c.id}"
                            f"//Firstname:{c.firstname}"
                            f"//Surname:{c.surname}"
                            f"//Nicknames:{c.nicknames}"
                            f"//RaceType:{c.race_type}"
                            f"//Occupation:{c.occupation}"
                            f"//Residence:{c.residence}"
                            f"//Attribute:{c.attribute}"
                            f"//BalanceBreaker:{c.attribute}"
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
                            f"//Inventory:{c.inventory}"
                            f"//Equipment:({c.equipment_h}, {c.equipment_c}, {c.equipment_l}, {c.equipment_s}, {c.equipment_g}, {c.equipment_be}, {c.equipment_rh}, {c.equipment_lh}, {c.equipment_n}, {c.equipment_r1}, {c.equipment_r2}, {c.equipment_br})\n")
    print(f"DEBUGG: Character {c.id} saved to {directory}.")

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
        "Attribute": "attribute",
        "Races": "racial_classes",
        "Jobs": "job_classes",
        "Power": "power_level",
        "Karma": "karma",
        "Religion": "religion",
        "BalanceBreaker": "balance_breaker",
        "Residence": "residence",
        "Occupation": "occupation",
        "RaceType": "race_type",
        "Inventory": "inventory",
        "Equipment": "equipment",
        "Weight": "weight",
        "HP": "hp",
        "MP": "mp",
        "SP": "sp",
        "PHY.ATK": "phyatk",
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
            # Initialize a dictionary to store character attributes
            character_data = {
                'id': None,
                'firstname': None,
                'surname': None,
                'nicknames': None,
                'attribute': [],
                'racial_classes': [],
                'job_classes': [],
                'balance_breaker': [],
                'power_level': 0,
                'residence': None,
                'race_type': None,
                'occupation': None,
                'karma': 0,
                'religion': None,
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
                'max_weight': 0,
                'hp': 0,
                'mp': 0,
                'sp': 0,
                'phyatk': 0,
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
                        elif key == "Attribute":
                            try:
                                character_data[var_name] = eval(value)
                            except:
                                character_data[var_name] = value.split(",")
                        elif key == "Weight":
                            weight = eval(value)
                            character_data['weight'], character_data['max_weight'] = weight
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
                attribute=character_data['attribute'],
                racial_classes=character_data['racial_classes'],
                job_classes=character_data['job_classes'],
                power_level=character_data['power_level'],
                residence=character_data['residence'],
                occupation=character_data['occupation'],
                race_type=character_data['race_type'],
                karma=character_data['karma'],
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
                max_weight=character_data['max_weight'],
                hp=character_data['hp'],
                mp=character_data['mp'],
                sp=character_data['sp'],
                phyatk=character_data['phyatk'],
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

def update_sheet(p: object):
    print(f"Updating sheet for {p.firstname}...")

    sheet = f"wotv player {p.id}"
    rcn = []
    rcl = []
    jcn = []
    jcl = []
    invn = []
    inva = []
    att = []
    nick = []

    if p.racial_classes:
        for i in p.racial_classes:
            name, level = i
            rcn.append(name)
            rcl.append(level)
    if p.job_classes:
        for i in p.job_classes:
            name, level = i
            jcn.append(name)
            jcl.append(level)
    if p.inventory:
        for i in p.inventory:
            name, amount = i
            if fs.is_tuple(name):
                name, level = name
                item = it.item_list(name, level)
                name = item.name
                invn.append(name)
            else:
                item = it.item_list(name, 2)
                name = item.name
                invn.append(name)
            inva.append(amount)
    if p.attribute:
        for i in p.attribute:
            att.append(i)
    if p.nicknames:
        for i in p.nicknames:
            nick.append(i)

    # Equipment
    equipment_ids = ["h", "c", "l", "s", "g", "be", "rh", "lh", "n", "r1", "r2", "br"]
    equip_data = []
    for i in equipment_ids:
        equip_name = f"equipment_{i}"
        equipment = getattr(p, equip_name, None)
        if equipment is not None:
            equip_name, equip_level = equipment
            eq = it.item_list(equip_name, equip_level)
            equipment_attrib = [eq.name, eq.hp, eq.mp, eq.sp, eq.phyatk, eq.phydef, eq.agility, eq.finess, eq.magatk, eq.magdef, eq.resistance, eq.special, eq.athletics, eq.acrobatics, eq.stealth, eq.sleight, eq.investigation, eq.insight, eq.perception, eq.deception, eq.intimidation, eq.persuasion, eq.performance]
            equip_data.append(equipment_attrib)
        else:
            equip_data.append(["", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    # Effects
    status_effects = []
    if p.status_effects:
        for e in p.status_effects:
            status_effects.append([e.name, e.new_hp, e.new_mp, e.new_sp, e.new_phyatk, e.new_phydef, e.new_agility, e.new_finess, e.new_magatk, e.new_magdef, e.new_resistance, e.new_special, e.new_athletics, e.new_acrobatics, e.new_stealth, e.new_sleight, e.new_investigation, e.new_insight, e.new_perception, e.new_deception, e.new_intimidation, e.new_persuasion, e.new_performance, e.time_left])
    else:
        for i in range(10):
            status_effects.append(["", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    data = gs.create_matrix(rcn, rcl, jcn, jcl, invn, inva, att, nick)

    update_data = [
        {"range": "A2:V5", "values": [
            [p.hp, p.mp, p.sp, p.phyatk, p.phydef, p.agility, p.finess, p.magatk, p.magdef, p.resistance, p.special, p.athletics, p.acrobatics, p.stealth, p.sleight, p.investigation, p.insight, p.perception, p.deception, p.intimidation, p.persuasion, p.performance],
            [p.new_hp, p.new_mp, p.new_sp, p.new_phyatk, p.new_phydef, p.new_agility, p.new_finess, p.new_magatk, p.new_magdef, p.new_resistance, p.new_special, p.new_athletics, p.new_acrobatics, p.new_stealth, p.new_sleight, p.new_investigation, p.new_insight, p.new_perception, p.new_deception, p.new_intimidation, p.new_persuasion, p.new_performance],
            [p.max_hp, p.max_mp, p.max_sp, p.max_phyatk, p.max_phydef, p.max_agility, p.max_finess, p.max_magatk, p.max_magdef, p.max_resistance, p.max_special, p.max_athletics, p.max_acrobatics, p.max_stealth, p.max_sleight, p.max_investigation, p.max_insight, p.max_perception, p.max_deception, p.max_intimidation, p.max_persuasion, p.max_performance]
        ]},
        {"range": "A6:M6", "values": [
            [p.id, p.firstname, p.surname, p.karma, p.religion, p.weight, p.max_weight, p.power_level, p.armor_class, p.race_type, p.occupation, p.residence, p.balance_breaker]
        ]},
        {"range": "O6:X39", "values": data},
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

    print("Update Complete")