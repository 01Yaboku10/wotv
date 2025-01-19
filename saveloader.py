import os
import character as ch
import failsafe as fs

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
                save.write(f"//ID:{c.id}//Firstname:{c.firstname}//Surname:{c.surname}//Attribute:{c.attribute}//Races:{c.racial_classes}//Jobs:{c.job_classes}//Power:{c.power_level}//Karma:{c.karma}//Religion:{c.religion}//HP:{c.hp}//MP:{c.mp}//PHY.ATK:{c.phyatk}//PHY.DEF:{c.phydef}//Agility:{c.agility}//Finess:{c.finess}//MAG.ATK:{c.magatk}//MAG.DEF:{c.magdef}//Resistance:{c.resistance}//Special:{c.special}//Athletics:{c.athletics}//Acrobatics:{c.acrobatics}//Stealth:{c.stealth}//Sleight:{c.sleight}//Investigation:{c.investigation}//Insight:{c.insight}//Perception:{c.perception}//Deception:{c.deception}//Intimidation:{c.intimidation}//Persuasion:{c.persuasion}//Performance:{c.performance}\n")
                print("DEBUGG: Character Updated")
                character_found = True
            else:
                save.write(line)
        if not character_found:
            save.write(f"//ID:{c.id}//Firstname:{c.firstname}//Surname:{c.surname}//Attribute:{c.attribute}//Races:{c.racial_classes}//Jobs:{c.job_classes}//Power:{c.power_level}//Karma:{c.karma}//Religion:{c.religion}//HP:{c.hp}//MP:{c.mp}//PHY.ATK:{c.phyatk}//PHY.DEF:{c.phydef}//Agility:{c.agility}//Finess:{c.finess}//MAG.ATK:{c.magatk}//MAG.DEF:{c.magdef}//Resistance:{c.resistance}//Special:{c.special}//Athletics:{c.athletics}//Acrobatics:{c.acrobatics}//Stealth:{c.stealth}//Sleight:{c.sleight}//Investigation:{c.investigation}//Insight:{c.insight}//Perception:{c.perception}//Deception:{c.deception}//Intimidation:{c.intimidation}//Persuasion:{c.persuasion}//Performance:{c.performance}\n")
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
        "Attribute": "attribute",
        "Races": "racial_classes",
        "Jobs": "job_classes",
        "Power": "power_level",
        "Karma": "karma",
        "Religion": "religion",
        "HP": "hp",
        "MP": "mp",
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

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            # Initialize a dictionary to store character attributes
            character_data = {
                'id': None,
                'firstname': None,
                'surname': None,
                'attribute': [],
                'racial_classes': [],
                'job_classes': [],
                'power_level': 0,
                'karma': 0,
                'religion': None,
                'hp': 0,
                'mp': 0,
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
                        if key in ["Races", "Jobs"]:
                            character_data[var_name] = eval(value)  # List of tuples
                        elif value.isdigit():
                            character_data[var_name] = int(value)
                        else:
                            character_data[var_name] = value

            # Create a Character object using the character_data dictionary
            character = ch.Character(
                id=character_data['id'],
                firstname=character_data['firstname'],
                surname=character_data['surname'],
                attribute=character_data['attribute'],
                racial_classes=character_data['racial_classes'],
                job_classes=character_data['job_classes'],
                power_level=character_data['power_level'],
                karma=character_data['karma'],
                religion=character_data['religion'],
                hp=character_data['hp'],
                mp=character_data['mp'],
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
