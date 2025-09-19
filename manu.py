from colorama import Fore, Style, init
import character as ch
import failsafe as fs
import saveloader as sl
import scenario as so
import gamelogic as gl

init(autoreset=True)

def main_menu():
    print("---------=Whisper of The Void=---------")
    choice = input("[C]haracter Menu, [S]cenario, [Q]uit\n").upper().strip()
    if choice == "C":
        character_menu()
    elif choice == "S":
        scenario_menu()
    elif choice == "Q":
        print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} Quitting game...\nSee you next time!")
        exit()
    else:
        main_menu()

def character_menu():
    print("------------------------------------=Character Menu=------------------------------------")
    choice = input("[C]reate character, [L]ook up character, [E]dit character, [S]ave character, [U]pload, [M]ain Menu\n").upper().strip()
    if choice == "C":
        character_creation()
    elif choice == "L":
        lookup_character()
    elif choice == "E":
        while True:
            lookup = fs.is_player(input("Character id: "))
            if not lookup:
                continue
            edit_character(lookup)
            break
    elif choice == "S":
        save_character()
    elif choice == "M":
        main_menu()
    elif choice =="U":
        while True:
            lookup = fs.is_player(input("Character id: "))
            if not lookup:
                continue
            sl.update_sheet(lookup)
            break
        character_menu()
    else:
        character_menu()

def scenario_menu():
    print("---------=Scenario Menu=---------")
    choice = input("[N]ew Scenario, [L]oad Scenario, [M]ain Menu\n").upper().strip()
    if choice == "N":
        foo = so.Game("N")
    elif choice == "M":
        main_menu()
    elif choice == "L":
        foo = so.Game("L")
    else:
        scenario_menu()

def character_creation():
    id: int = fs.is_int(input("Character id: "))
    character_type = input("Character Type: ").lower()
    if character_type == "spirit":
        master = input("Master ID: ")
    else:
        master = None
    firstname: str = input("Character firstname: ").capitalize()
    firstname = gl.capitalize_string(firstname, " ")
    surname: str = input("Character surname: ").capitalize()
    surname = gl.capitalize_string(surname, " ")
    karma: int = fs.is_int(input("Character karma: "))
    religion: str = input("Character religon: ").capitalize()
    attributes: list = []
    while True:
        attribute = input("Magical Attribute ([R]andom), ([D]one): ").capitalize()
        if attribute == "D":
            break
        if attribute == "R":
            attribute = gl.magic_attribute_gen()
            attributes.append(attribute)
            print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} Added Magic Attribute: {attribute}")
        else:
            attributes.append(attribute)
            print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} Added Magic Attribute: {attribute}")
            
    while True:
        race = input("Character Race: ").lower()
        if not fs.is_race(race):
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Race not found, Try Again...")
        else:
            break
    level = fs.is_int(input("Race level: "))
    player = ch.Character(id, firstname, surname, attributes, karma, religion, [(race, level)], character_type=character_type, master=master)
    edit_character(player)

def lookup_character():
    while True:
        chara = input("Lookup character with id: ")
        if not fs.is_player(chara):
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Character with id {chara} not found in the registry.")
        break
    print(ch.character_dic.get(chara))
    character_menu()

def edit_character(player: object):
    while True:
        print(f"---------={player.firstname} {player.surname}=---------")
        choice = input("[R]ace, [J]obs, [I]nfo, [E]quipment, [S]pirits, [D]one: \n").upper().strip()
        if choice == "R":
            while True:
                print("---------=Racial Classes=---------")
                for index, race in enumerate(player.racial_classes):
                    name, level = race
                    print(f"[{index+1}] {name} [{level}]")
                choice = input("[A]dd, [E]dit, [R]emove, [D]one: \n").upper().strip()
                if choice == "R":
                    player.race_remove()
                elif choice == "A":
                    player.race_add()
                elif choice == "E":
                    player.race_edit()
                elif choice == "D":
                    break
        elif choice == "J":
            while True:
                print("---------=Job Classes=---------")
                for index, job in enumerate(player.job_classes):
                    name, level = job
                    print(f"[{index+1}] {name} [{level}]")
                choice = input("[A]dd, [E]dit, [R]emove, [D]one: \n").upper().strip()
                if choice == "R":
                    player.job_remove()
                elif choice == "A":
                    player.job_add()
                elif choice == "E":
                    player.job_edit()
                elif choice == "D":
                    break
        elif choice == "S":
            print("---------=Spirits=---------")
            while True:
                if player.spirits:
                    for index, name in enumerate(player.spirits):
                        spirit=ch.character_dic[name]
                        print(f"[{index+1}] {spirit.firstname}")
                choice = input("[A]dd, [R]emove, [D]one: \n").upper().strip()
                if choice == "A":
                    spirit = input("Add Spirit with ID: ")
                    player.spirits.append(spirit)
                elif choice == "R":
                    if player.spirits:
                        choice = fs.is_int(input("Remove spirit with index: "))
                        if 1 <= choice <= len(player.spirits):
                            del player.spirits[choice-1]
                        else:
                            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Index out of bounce...")
                    else:
                        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} No Spirits found...")
                elif choice == "D":
                    break 
        elif choice == "I":
            while True:
                print(f"---------={player.firstname} {player.surname}=---------")
                print(f"Firstname: {player.firstname}\nSurname: {player.surname}\nNicknames: {player.nicknames}\nCharacter Type: {player.character_type}\nMagical Attributes: {player.attribute}\nKarma: {player.karma}\nReligion: {player.religion}\nOccupation: {player.occupation}\nResidence: {player.residence}")
                choice = input("Change: [F]irstname, [S]urname, [N]icknames, [O]ccupation, [H]ome, [R]eligion, [A]ttribute, [K]arma, [E]quip Slot, [M]aster, [D]one\n").upper().strip()
                if choice == "F":
                    firstname = input("New Firstname: ")
                    player.firstname = gl.capitalize_string(firstname, " ")
                elif choice == "S":
                    surname = input("New Surname: ")
                    player.surname = gl.capitalize_string(surname, " ")
                elif choice == "N":
                    while True:
                        choice = input("[A]dd, [R]emove: ").upper()
                        if choice == "A":
                            nickname = input("Add Nickname: ")
                            player.nicknames.append(gl.capitalize_string(nickname, " "))
                            break
                        elif choice == "R":
                            for i, nickname in enumerate(player.nicknames):
                                print(f"[{i+1}] {nickname}")
                            remove = fs.is_int(input("Remove nickname ID: "))
                            if 1 <= remove <= len(player.nicknames):
                                remove = player.nicknames[remove-1]
                                print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} Removed {player.nicknames[remove]}")
                                del player.nicknames[remove]
                            break
                elif choice == "O":
                    occupation = input("New Occupation: ")
                    player.occupation = gl.capitalize_string(occupation, " ")
                elif choice == "M":
                    if player.character_type != "spirit":
                        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Player is not a spirit...")
                    else:
                        player.master = str(input("New Master ID: "))
                elif choice == "E":
                    if player.character_type != "spirit":
                        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Player is not a spirit...")
                    else:
                        while True:
                            print(f"Slots: {player.equip_slot}")
                            choice = input("[A]dd, [R]emove, [D]one: ").upper()
                            if choice == "D":
                                break
                            elif choice == "A":
                                add = input("Add: ").lower()
                                if add in gl.EQUIPMENT_SLOTS_S:
                                    player.equip_slot.append(add)
                                else:
                                    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {add} is not an equipment slot...")
                            elif choice == "R":
                                remove = input("Remove: ").lower()
                                if remove in player.equip_slot:
                                    player.equip_slot.remove(remove)
                                else:
                                    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {remove} is not an active equip slot...")
                elif choice == "R":
                    religion = input("New Religion: ")
                    player.religion = gl.capitalize_string(religion, " ")
                elif choice == "H":
                    residence = input("New Residence: ")
                    player.residence = gl.capitalize_string(residence, " ")
                elif choice == "A":
                    for index, attrib in enumerate(player.attribute):
                        print(f"[{index+1}] {attrib}")
                    while True:
                        choice = (input("A[dd], [R]emove, [D]one: ")).upper()
                        if choice == "A":
                            attribute = input("Add attribute: ").capitalize()
                            player.attribute.append(attribute)
                        elif choice == "R":
                            choice = fs.is_int(input("Remove attribute with index: "))
                            if 1 <= choice <= len(player.attribute):
                                remove = player.attribute[choice-1]
                                print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} Removed {player.attribute(remove)}")
                                del player.attribute[remove]
                        elif choice == "D":
                            break
                elif choice == "K":
                    player.karma = fs.is_int(input("New Karma: "))
                elif choice == "D":
                    break
        elif choice == "E":
            while True:
                print(f"---------={player.firstname} {player.surname}=---------")
                print(
                    "---------=Equipment=---------\n"
                    f"Helmet:{player.equipment_h}\n"
                    f"Chestplate:{player.equipment_c}\n"
                    f"Leggingss:{player.equipment_l}\n"
                    f"Shoes:{player.equipment_s}\n"
                    f"Gloves:{player.equipment_g}\n"
                    f"Belt:{player.equipment_be}\n"
                    f"Right Hand:{player.equipment_rh}\n"
                    f"Left Hand:{player.equipment_lh}\n"
                    f"Necklace:{player.equipment_n}\n"
                    f"Ring:{player.equipment_r1}\n"
                    f"Ring:{player.equipment_r2}\n"
                    f"Bracelet:{player.equipment_br}\n"
                    "-----------=Gold=-----------\n"
                    f"Gold:{player.gold}/{player.silver}/{player.bronze}\n"
                    "---------=Inventory=---------\n"
                    f"{player.inventory}"
                )
                choice = input("[A]dd, [R]emove, [E]quip, [G]old, [D]one: ").upper()
                if choice == "A":
                    player.equipment_add()
                elif choice == "G":
                    while True:
                        print("---------=Gold=---------")
                        choice = input("[A]dd, [R]emove, [T]ransfer: ").upper()
                        type = input("Type [G]old, [S]ilver, [B]ronze: ").lower()
                        amount = fs.is_int(input("Amount: "))
                        if choice == "A":
                            player.gold_add(type, amount)
                            break
                        elif choice == "R":
                            player.gold_remove(type, amount)
                            break
                        elif choice == "T":
                            opponent = ch.character_dic[str(input("Opponent ID: "))]
                            player.gold_transfer(type, amount, opponent)
                            break
                elif choice == "R":
                    remove = input("Remove from [I]nventory, [E]quipment: ").upper()
                    if remove == "Q":
                        continue
                    while True:
                        if remove == "I":
                            remove_item = input("Remove item: ").lower()
                            remove_amount = fs.is_int(input("Remove Amount: "))
                            player.equipment_reset()
                            player.inventory_remove(remove_item, remove_amount)
                            player.equipment_check()
                            break
                        elif remove == "E":
                            player.equipment_remove()
                            break
                elif choice == "E":
                    player.inventory_equip()
                elif choice == "D":
                    break
        elif choice == "D":

            break
    character_menu()

def save_character():
    players: list[object] = []
    for key, player in ch.character_dic.items():
        players.append(player)
    sl.save_all("character_saves", players)
    character_menu()