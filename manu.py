import character as ch
import failsafe as fs
import saveloader as sl
import scenario as so
import gamelogic as gl
def main_menu():
    print("---------=Whisper of The Void=---------")
    choice = input("[C]haracter Menu, [S]cenario, [Q]uit\n").upper().strip()
    if choice == "C":
        character_menu()
    elif choice == "S":
        scenario_menu()
    elif choice == "Q":
        print("DEBUGG: Quitting game...")
        exit()
    else:
        main_menu()

def character_menu():
    print("---------=Character Menu=---------")
    choice = input("[C]reate character, [L]ook up character, [E]dit character, [S]ave character, [M]ain Menu\n").upper().strip()
    if choice == "C":
        character_creation()
    elif choice == "L":
        lookup_character()
    elif choice == "E":
        lookup = fs.is_player(input("Character id: "))
        if not lookup:
            return
        edit_character(lookup)
    elif choice == "S":
        save_character()
    elif choice == "M":
        main_menu()
    else:
        character_menu()

def scenario_menu():
    print("---------=Scenario Menu=---------")
    choice = input("[N]ew scenario, [M]ain Menu\n").upper().strip()
    if choice == "N":
        foo = so.Game()
    elif choice == "M":
        main_menu()
    else:
        scenario_menu()

def character_creation():
    id: int = fs.is_int(input("Character id: "))
    firstname: str = input("Character firstname: ").capitalize()
    surname: str = input("Character surname: ").capitalize()
    karma: int = fs.is_int(input("Character karma: "))
    religion: str = input("Character religon").capitalize()
    attributes: list = []
    while True:
        attribute = input("Magical Attribute ([R]andom), ([D]one): ").capitalize()
        if attribute == "D":
            break
        if attribute == "R":
            attribute = gl.magic_attribute_gen()
            attributes.append(attribute)
            print(f"Added Magic Attribute: {attribute}")
        else:
            attributes.append(attribute)
            print(f"Added Magic Attribute: {attribute}")
            
    while True:
        race = input("Character Race: ").lower()
        if not fs.is_race(race):
            print("Try Again...")
        else:
            break
    level = fs.is_int(input("Race level: "))
    player = ch.Character(id, firstname, surname, attributes, karma, religion, [(race, level)])
    edit_character(player)

def lookup_character():
    chara = input("Lookup character with id: ")
    if not fs.is_player(chara):
        return
    print(ch.character_dic.get(chara))
    character_menu()

def edit_character(player: object):
    while True:
        print(f"---------={player.firstname} {player.surname}=---------")
        choice = input("[R]ace, [J]obs, [I]nfo, [E]quipment, [D]one: \n").upper().strip()
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
        elif choice == "I":
            while True:
                print(f"---------={player.firstname} {player.surname}=---------")
                print(f"Firstname: {player.firstname}\nSurname: {player.surname}\nNicknames: {player.nicknames}\nMagical Attributes: {player.attribute}\nKarma: {player.karma}\nReligion: {player.religion}\nOccupation: {player.occupation}\nResidence: {player.residence}")
                choice = input("Change: [F]irstname, [S]urname, [N]icknames, [O]ccupation, [H]ome, [R]eligion, [A]ttribute, [K]arma, [D]one\n").upper().strip()
                if choice == "F":
                    player.firstname = input("New Firstname: ").lower().capitalize()
                elif choice == "S":
                    player.surname = input("New Surname: ").lower().capitalize()
                elif choice == "N":
                    while True:
                        choice = input("[A]dd, [R]emove: ").upper()
                        if choice == "A":
                            player.nicknames.append(input("Add Nickname: ").capitalize())
                            break
                        elif choice == "R":
                            for i, nickname in enumerate(player.nicknames):
                                print(f"[{i+1}] {nickname}")
                            remove = fs.is_int(input("Remove nickname ID: "))
                            if 1 <= remove <= len(player.nicknames):
                                remove = player.nicknames[remove-1]
                                print(f"Removed {player.nicknames(remove)}")
                                del player.nicknames[remove]
                            break
                elif choice == "O":
                    player.occupation = input("New Occupation: ").lower().capitalize()
                elif choice == "R":
                    player.religion = input("New Religion: ").lower().capitalize()
                elif choice == "H":
                    player.residence = input("New Residence: ").lower().capitalize()
                elif choice == "A":
                    for index, attrib in enumerate(player.attribute):
                        print(f"[{index+1}] {attrib}")
                    while True:
                        choice = (input("A[dd], [R]emove: "))
                        if choice == "A":
                            attribute = input("Add attribute: ").capitalize
                            player.attribute.append(attribute)
                        elif choice == "R":
                            choice = fs.is_int(input("Remove attribute with index: "))
                            if 1 <= choice <= len(player.attribute):
                                remove = player.attribute[choice-1]
                                print(f"Removed {player.attribute(remove)}")
                                del player.attribute[remove]
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
                    "---------=Inventory=---------\n"
                    f"{player.inventory}"
                )
                choice = input("[A]dd, [R]emove, [E]quip, [D]one: ").upper()
                if choice == "A":
                    player.equipment_add()
                elif choice == "R":
                    remove = input("Remove from [I]nventory, [E]quipment: ").upper()
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
    chara = input("Save character with id: ")
    if chara == "SA":
        players: list[object] = []
        for key, player in ch.character_dic.items():
            players.append(player)
        sl.save_all("character_saves", players)
    else:
        if not fs.is_player(chara):
            return
        sl.save_character("character_saves", ch.character_dic.get(chara))
    character_menu()