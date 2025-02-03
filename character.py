import job_classes
import racial_classes
import item as it
import failsafe as fs
import saveloader as sl
id_list = []
character_dic = {}

class Character():
    def __init__(self,
                 id: int,
                 firstname: str,
                 surname: str,
                 attribute: list[str] = None,
                 karma: int = 0,
                 religion: str = None,
                 racial_classes: list[tuple[str, int]] = None,
                 job_classes: list[tuple[str, int]] = None,
                 inventory: list[tuple[str, int]] = None,
                 status_effects: list[object] = None,
                 equipment_h: tuple[str, int] = None,
                 equipment_c: tuple[str, int] = None,
                 equipment_l: tuple[str, int] = None,
                 equipment_s: tuple[str, int] = None,
                 equipment_g: tuple[str, int] = None,
                 equipment_be: tuple[str, int] = None,
                 equipment_rh: tuple[str, int] = None,
                 equipment_lh: tuple[str, int] = None,
                 equipment_n: tuple[str, int] = None,
                 equipment_r1: tuple[str, int] = None,
                 equipment_r2: tuple[str, int] = None,
                 equipment_br: tuple[str, int] = None,
                 power_level: int = 0,
                 residence: str = None,
                 balance_breaker: list[str] = None,
                 occupation: str = None,
                 nicknames: list[str] = None,
                 race_type: str = None,
                 weight: int = 0,
                 max_weight: int = 0,
                 hp: int = 0,
                 mp: int = 0,
                 sp: int = 0,
                 phyatk: int = 0,
                 phydef: int = 0,
                 agility: int = 0,
                 finess: int = 0,
                 magatk: int = 0,
                 magdef: int = 0,
                 resistance: int = 0,
                 special: int = 0,
                 athletics: int = 0,
                 acrobatics: int = 0,
                 stealth: int = 0,
                 sleight: int = 0,
                 investigation: int = 0,
                 insight: int = 0,
                 perception: int = 0,
                 deception: int = 0,
                 intimidation: int = 0,
                 persuasion: int = 0,
                 performance: int = 0) -> None:
        self.id = id
        self.firstname = firstname.capitalize()
        self.surname = surname.capitalize()
        self.attribute = attribute if attribute is not None else []
        self.job_classes = job_classes if job_classes is not None else []
        self.racial_classes = racial_classes if racial_classes is not None else []
        self.inventory = inventory if inventory is not None else []
        self.balance_breaker = balance_breaker if balance_breaker is not None else []
        self.status_effects = status_effects if status_effects is not None else []
        self.equipment_h = equipment_h
        self.equipment_c = equipment_c
        self.equipment_l = equipment_l
        self.equipment_s = equipment_s
        self.equipment_g = equipment_g
        self.equipment_be = equipment_be
        self.equipment_rh = equipment_rh
        self.equipment_lh = equipment_lh
        self.equipment_n = equipment_n
        self.equipment_r1 = equipment_r1
        self.equipment_r2 = equipment_r2
        self.equipment_br = equipment_br
        self.power_level = power_level
        self.residence = residence
        self.occupation = occupation
        self.nicknames = nicknames if nicknames is not None else []
        self.weight = weight
        self.max_weight = max_weight
        self.karma = self.new_karma = self.max_karma = karma
        self.race_type = race_type
        self.religion = religion
        self.level = 0
        self.hp = self.new_hp = self.max_hp = hp
        self.mp = self.new_mp = self.max_mp = mp
        self.sp = self.new_sp = self.max_sp = sp
        self.phyatk = self.new_phyatk = self.max_phyatk = phyatk
        self.phydef = self.new_phydef = self.max_phydef = phydef
        self.agility = self.new_agility = self.max_agility = agility
        self.finess = self.new_finess = self.max_finess = finess
        self.magatk = self.new_magatk = self.max_magatk = magatk
        self.magdef = self.new_magdef = self.max_magdef = magdef
        self.resistance = self.new_resistance = self.max_resistance = resistance
        self.special = self.new_special = self.max_special = special
        self.athletics = self.new_athletics = self.max_athletics = athletics
        self.acrobatics = self.new_acrobatics = self.max_acrobatics = acrobatics
        self.stealth = self.new_stealth = self.max_stealth = int(stealth)
        self.sleight = self.new_sleight = self.max_sleight = int(sleight)
        self.investigation = self.new_investigation = self.max_investigation = investigation
        self.insight = self.new_insight = self.max_insight = insight
        self.perception = self.new_perception = self.max_perception = perception
        self.deception = self.new_deception = self.max_deception = deception
        self.intimidation = self.new_intimidation = self.max_intimidation = intimidation
        self.persuasion = self.new_persuasion = self.max_persuasion = persuasion
        self.performance = self.new_performance = self.max_performance = performance
        self.team = None

        self.weight = 0

        self.race_type_list = []
        self.armor_classes = []
        self.armor_class = "None"

        self.update_race()
        self.update_job()

        self.id_check()
        self.race_check()
        self.armor_class_check()
        self.equipment_check()
        self.attribute_check()

        self.power_check()

    def __repr__(self) -> str:
        return (
        f"---------={self.firstname} {self.surname}=---------\n"
        f"Nicknames: {self.nicknames}\n"
        f"Power level: {self.power_level}\n"
        f"Karma: {self.karma}\n"
        f"Attributes: {self.attribute}\n"
        f"Armor Class: {self.armor_class}\n"
        f"Race Type: {self.race_type}\n"
        f"Occupation: {self.occupation}\n"
        f"Residence: {self.residence}\n"
        f"Weight: {self.weight}/{self.max_weight} kg\n"
        "---------=Stats=---------\n"
        f"HP:{self.hp}, MP:{self.mp}, SP:{self.sp}\n"
        f"Agility:{self.agility}, Finess:{self.finess}\n"
        f"PHY.ATK:{self.phyatk}, PHY.DEF:{self.phydef}\n"
        f"MAG.ATK:{self.magatk}, MAG.DEF:{self.magdef}\n"
        f"Resistance:{self.resistance}, Special:{self.special}\n"
        "---------=Skills=---------\n"
        f"ATH:{self.athletics}, ACRO:{self.acrobatics}\n"
        f"STE:{self.stealth}, SOH:{self.sleight}\n"
        f"INV:{self.investigation}, PER:{self.perception}\n"
        f"DEC:{self.deception}, INTI:{self.intimidation}\n"
        f"PERS:{self.persuasion}, PERF:{self.performance}\n"
        "---------=Equipment=---------\n"
        f"Helmet:{self.equipment_h}\n"
        f"Chestplate:{self.equipment_c}\n"
        f"Leggingss:{self.equipment_l}\n"
        f"Shoes:{self.equipment_s}\n"
        f"Gloves:{self.equipment_g}\n"
        f"Belt:{self.equipment_be}\n"
        f"Right Hand:{self.equipment_rh}\n"
        f"Left Hand:{self.equipment_lh}\n"
        f"Necklace:{self.equipment_n}\n"
        f"Ring:{self.equipment_r1}\n"
        f"Ring:{self.equipment_r2}\n"
        f"Bracelet:{self.equipment_br}\n"
        "---------=Inventory=---------\n"
        f"{self.inventory}\n"
    )

    def print_eq(self):
        print(
        "---------=Equipment=---------\n"
        f"Helmet:{self.equipment_h}\n"
        f"Chestplate:{self.equipment_c}\n"
        f"Leggingss:{self.equipment_l}\n"
        f"Shoes:{self.equipment_s}\n"
        f"Gloves:{self.equipment_g}\n"
        f"Belt:{self.equipment_be}\n"
        f"Right Hand:{self.equipment_rh}\n"
        f"Left Hand:{self.equipment_lh}\n"
        f"Necklace:{self.equipment_n}\n"
        f"Ring:{self.equipment_r1}\n"
        f"Ring:{self.equipment_r2}\n"
        f"Bracelet:{self.equipment_br}\n"
        "---------=Inventory=---------\n"
        f"{self.inventory}\n"
        )

    def id_check(self):
        if self.id not in id_list:
            print(f"[DEBUGG]: {self.firstname}'s id set to {self.id}")
        else:
            print(f"[DEBUGG]: id:[{self.id}] already exists,", end = " ")
            self.id = len(id_list) + 1
            print(f"Setting {self.firstname}'s id to {self.id}")
        id_list.append(self.id)
        character_dic[f"{self.id}"] = self
        print(f"DEBUGG: {self.firstname} with id {self.id} has been added to the dictionary")
    
    def attribute_check(self):
        self.athletics += round((((self.phyatk+self.finess)/2)*0.1))
        self.acrobatics += round((((self.agility+self.finess+self.sp)/3)*0.1))
        self.stealth += round((((self.agility+self.finess)/2)*0.1))
        self.sleight += round((((self.phyatk+self.finess+self.agility)/3)*0.1))
        self.investigation += round((((self.mp+self.finess+self.magatk+self.magdef)/4)*0.1))
        self.insight += round((((self.mp+self.magatk+self.magdef)/2)*0.1))
        self.perception += round((((self.phydef+self.magdef+self.resistance)/3)*0.1))
        self.deception += round((((self.phyatk+self.finess+self.magatk)/3)*0.1))
        self.intimidation += round((((self.hp+self.phyatk+self.magatk+self.special)/4)*0.1)+(self.power_level/2500))
        self.persuasion += round((((self.phyatk+self.finess+self.magatk)/3)*0.1))
        self.performance += round((((self.mp+self.agility+self.finess+self.special)/4)*0.1))
        self.max_weight = round(((self.phyatk+self.sp)/2)+(self.athletics*2))

    def power_check(self):
        self.power_level = 0
        for raceclass in self.racial_classes:
            name, level = raceclass
            race = racial_classes.race_list(name, level)
            self.power_level += race.power_level*level
        for jobclass in self.job_classes:
            name, level = jobclass
            job = job_classes.job_list(name, level)
            self.power_level += job.power_level*level
        self.power_level += (self.hp+self.mp+self.phyatk+self.phydef+self.agility+self.finess+self.magdef+self.magatk+self.resistance+self.special+ \
                            10*(self.athletics+self.acrobatics+self.stealth+self.sleight+self.deception+self.perception+self.performance+self.persuasion+self.insight+self.investigation+self.intimidation))
        print(f"Character [ID:{self.id}] {self.firstname}'s power level set to {self.power_level}")

    def equipment_check(self):
        #print("DEBUGG: RUNNING EQUIP CHECK")
        equipments = ["equipment_h", "equipment_c", "equipment_l", "equipment_s", "equipment_g", "equipment_be", "equipment_rh", "equipment_lh", "equipment_n", "equipment_r1", "equipment_r2", "equipment_br"]
        for attrib in equipments:
            piece = getattr(self, attrib)
            if piece is not None:
                equipment, level = piece
                equipped = it.item_list(equipment, level)
                self.hp += equipped.hp
                self.mp += equipped.mp
                self.sp += equipped.sp
                self.weight += equipped.weight
                self.phyatk += equipped.phyatk
                self.phydef += equipped.phydef
                self.agility += equipped.agility
                self.finess += equipped.finess
                self.magatk += equipped.magatk
                self.magdef += equipped.magdef
                self.resistance += equipped.resistance
                self.special += equipped.special
                self.athletics += equipped.athletics
                self.acrobatics += equipped.acrobatics
                self.stealth += equipped.stealth
                self.sleight += equipped.sleight
                self.investigation += equipped.investigation
                self.insight += equipped.insight
                self.perception += equipped.perception
                self.deception += equipped.deception
                self.intimidation += equipped.intimidation
                self.persuasion += equipped.persuasion
                self.performance += equipped.performance

                if fs.is_attrib(self, "new_hp"):
                    self.new_hp += equipped.hp
                    self.new_mp += equipped.mp
                    self.new_sp += equipped.sp
                    self.weight += equipped.weight
                    self.new_phyatk += equipped.phyatk
                    self.new_phydef += equipped.phydef
                    self.new_agility += equipped.agility
                    self.new_finess += equipped.finess
                    self.new_magatk += equipped.magatk
                    self.new_magdef += equipped.magdef
                    self.new_resistance += equipped.resistance
                    self.new_special += equipped.special
                    self.new_athletics += equipped.athletics
                    self.new_acrobatics += equipped.acrobatics
                    self.new_stealth += equipped.stealth
                    self.new_sleight += equipped.sleight
                    self.new_investigation += equipped.investigation
                    self.new_insight += equipped.insight
                    self.new_perception += equipped.perception
                    self.new_deception += equipped.deception
                    self.new_intimidation += equipped.intimidation
                    self.new_persuasion += equipped.persuasion
                    self.new_performance += equipped.performance
                    self.max_hp += equipped.hp
                    self.max_mp += equipped.mp
                    self.max_sp += equipped.sp
                    self.weight += equipped.weight
                    self.max_phyatk += equipped.phyatk
                    self.max_phydef += equipped.phydef
                    self.max_agility += equipped.agility
                    self.max_finess += equipped.finess
                    self.max_magatk += equipped.magatk
                    self.max_magdef += equipped.magdef
                    self.max_resistance += equipped.resistance
                    self.max_special += equipped.special
                    self.max_athletics += equipped.athletics
                    self.max_acrobatics += equipped.acrobatics
                    self.max_stealth += equipped.stealth
                    self.max_sleight += equipped.sleight
                    self.max_investigation += equipped.investigation
                    self.max_insight += equipped.insight
                    self.max_perception += equipped.perception
                    self.max_deception += equipped.deception
                    self.max_intimidation += equipped.intimidation
                    self.max_persuasion += equipped.persuasion
                    self.max_performance += equipped.performance

        #  Inventory Weight
        for i in self.inventory:
            name, amount = i
            if fs.is_tuple(name):
                item_name, level = name
                item = it.item_list(item_name, level)
            else:
                item = it.item_list(name, 1)
            self.weight += item.weight*amount
        #print("DEBUGG: EQUIP CHECK COMPLETE")

        if fs.is_attrib(self, "prefix"):
            sl.update_sheet(self)

    def equipment_reset(self):
        #print("DEBUGG: RUNNING EQUIP RESET")
        equipments = ["equipment_h", "equipment_c", "equipment_l", "equipment_s", "equipment_g", "equipment_be", "equipment_rh", "equipment_lh", "equipment_n", "equipment_r1", "equipment_r2", "equipment_br"]
        for attrib in equipments:
            piece = getattr(self, attrib)
            if piece is not None:
                equipment, level = piece
                equipped = it.item_list(equipment, level)
                self.hp -= equipped.hp
                self.mp -= equipped.mp
                self.sp -= equipped.sp
                self.weight -= equipped.weight
                self.phyatk -= equipped.phyatk
                self.phydef -= equipped.phydef
                self.agility -= equipped.agility
                self.finess -= equipped.finess
                self.magatk -= equipped.magatk
                self.magdef -= equipped.magdef
                self.resistance -= equipped.resistance
                self.special -= equipped.special
                self.athletics -= equipped.athletics
                self.acrobatics -= equipped.acrobatics
                self.stealth -= equipped.stealth
                self.sleight -= equipped.sleight
                self.investigation -= equipped.investigation
                self.insight -= equipped.insight
                self.perception -= equipped.perception
                self.deception -= equipped.deception
                self.intimidation -= equipped.intimidation
                self.persuasion -= equipped.persuasion
                self.performance -= equipped.performance

                if fs.is_attrib(self, "new_hp"):
                    self.new_hp -= equipped.hp
                    self.new_mp -= equipped.mp
                    self.new_sp -= equipped.sp
                    self.weight -= equipped.weight
                    self.new_phyatk -= equipped.phyatk
                    self.new_phydef -= equipped.phydef
                    self.new_agility -= equipped.agility
                    self.new_finess -= equipped.finess
                    self.new_magatk -= equipped.magatk
                    self.new_magdef -= equipped.magdef
                    self.new_resistance -= equipped.resistance
                    self.new_special -= equipped.special
                    self.new_athletics -= equipped.athletics
                    self.new_acrobatics -= equipped.acrobatics
                    self.new_stealth -= equipped.stealth
                    self.new_sleight -= equipped.sleight
                    self.new_investigation -= equipped.investigation
                    self.new_insight -= equipped.insight
                    self.new_perception -= equipped.perception
                    self.new_deception -= equipped.deception
                    self.new_intimidation -= equipped.intimidation
                    self.new_persuasion -= equipped.persuasion
                    self.new_performance -= equipped.performance
                    self.max_hp -= equipped.hp
                    self.max_mp -= equipped.mp
                    self.max_sp -= equipped.sp
                    self.weight -= equipped.weight
                    self.max_phyatk -= equipped.phyatk
                    self.max_phydef -= equipped.phydef
                    self.max_agility -= equipped.agility
                    self.max_finess -= equipped.finess
                    self.max_magatk -= equipped.magatk
                    self.max_magdef -= equipped.magdef
                    self.max_resistance -= equipped.resistance
                    self.max_special -= equipped.special
                    self.max_athletics -= equipped.athletics
                    self.max_acrobatics -= equipped.acrobatics
                    self.max_stealth -= equipped.stealth
                    self.max_sleight -= equipped.sleight
                    self.max_investigation -= equipped.investigation
                    self.max_insight -= equipped.insight
                    self.max_perception -= equipped.perception
                    self.max_deception -= equipped.deception
                    self.max_intimidation -= equipped.intimidation
                    self.max_persuasion -= equipped.persuasion
                    self.max_performance -= equipped.performance
        #print("DEBUGG: EQUIP RESET COMPLETE")

    def race_check(self):
        if "heteromorph" in self.race_type_list:
            self.race_type = "heteromorph"
            return
        if "demi-human" in self.race_type_list:
            self.race_type = "demi-human"
            return
        self.race_type = "humanoid"
    
    def armor_class_check(self):
        if "heavy" in self.armor_classes:
            self.armor_class = "heavy"
            return
        if "medium" in self.armor_classes:
            self.armor_class = "medium"
            return
        if "light" in self.armor_classes:
            self.armor_class = "light"
            return
        self.armor_class = "None"
        for index, armor in enumerate(self.armor_classes):
            del self.armor_classes[index]
            print(f"DEBUGG: Deleted armor class {index}")
              
    def update_job(self):
        self.update_race()
        for jobclass in self.job_classes:
            name, level = jobclass
            job = job_classes.job_list(name, level)
            self.hp += job.hp
            self.mp += job.mp
            self.sp += job.sp
            self.level += level
            self.phyatk += job.phyatk
            self.phydef += job.phydef
            self.agility += job.agility
            self.finess += job.finess
            self.magatk += job.magatk
            self.magdef += job.magdef
            self.resistance += job.resistance
            self.special += job.special
            self.athletics += job.athletics
            self.acrobatics += job.acrobatics
            self.stealth += job.stealth
            self.sleight += job.sleight
            self.investigation += job.investigation
            self.insight += job.insight
            self.perception += job.perception
            self.deception += job.deception
            self.intimidation += job.intimidation
            self.persuasion += job.persuasion
            self.performance += job.performance

            self.armor_classes.append(job.armor_class)
        self.armor_class_check()

    def update_race(self):
        self.race_type_list.clear()
        self.hp, self.mp, self.sp, self.level, self.phyatk, self.phydef, self.agility, self.finess, self.magatk, self.magdef, self.resistance, self.special, self.athletics, self.acrobatics, self.stealth, self.sleight, self.investigation, self.insight, self.perception, self.deception, self.intimidation, self.persuasion, self.performance = (0,) * 23
        for raceclass in self.racial_classes:
            name, level = raceclass
            race = racial_classes.race_list(name, level)
            self.hp += race.hp*level
            self.mp += race.mp*level
            self.sp += race.sp*level
            self.level += level*level
            self.phyatk += race.phyatk*level
            self.phydef += race.phydef*level
            self.agility += race.agility*level
            self.finess += race.finess*level
            self.magatk += race.magatk*level
            self.magdef += race.magdef*level
            self.resistance += race.resistance*level
            self.special += race.special*level
            self.athletics += race.athletics*level
            self.acrobatics += race.acrobatics*level
            self.stealth += race.stealth*level
            self.sleight += race.sleight*level
            self.investigation += race.investigation*level
            self.insight += race.insight*level
            self.perception += race.perception*level
            self.deception += race.deception*level
            self.intimidation += race.intimidation*level
            self.persuasion += race.persuasion*level
            self.performance += race.performance*level

            self.race_type_list.append(race.type)
    
    def race_remove(self):
        if len(self.racial_classes) != 1:
            for index, race in enumerate(self.racial_classes):
                print(f"[{index+1}] {race}")
            remove = input("Remove race class [index]: ")
            print(f"DEBUGG: Removing {self.racial_classes(index-1)}")
            del self.racial_classes[remove-1]
        else:
            print("ERROR: Race class cannot be null")
            self.update_race()

    def race_add(self):
        race = input("Add race: ").lower()
        if not fs.is_race(race):
            return
        level = fs.is_int(input("Race level: "))
        self.racial_classes.append((race, level))
        print(f"DEBUGG: Added level {level} {race} to {self.firstname}")
        self.update_race()
    
    def race_edit(self):
        for index, race in enumerate(self.racial_classes):
            print(f"[{index+1}] {race}")
        while True:
            choice = fs.is_int(input("Edit race with index: "))
            if 1 <= choice <= len(self.racial_classes):
                race_name, foo = self.racial_classes[choice-1]
                level = fs.is_int(input("New level: "))
                del self.racial_classes[choice-1]
                self.racial_classes.append((race_name, level))
                print(f"DEBUGG: {race}'s level has been changed to {level}")
                self.update_race()
                return
            else:
                print("ERROR: Not in range")
    
    def job_remove(self):
        if len(self.job_classes) == 0:
            print("ERROR: Character has no job classes")
            return
        for index, job in enumerate(self.job_classes):
            print(f"[{index+1}] {job}")
        remove = fs.is_int(input("Remove job class [index]: "))
        print(f"DEBUGG: Removing {self.job_classes[remove-1]}")
        del self.job_classes[remove-1]

    def job_add(self):
        job = input("Add job: ").lower()
        if not fs.is_job(job):
            return
        level = fs.is_int(input("Job level: "))
        self.job_classes.append((job, level))
        print(f"DEBUGG: Added level {level} {job} to {self.firstname}")
        self.update_job()

    def job_edit(self):
        if len(self.job_classes) == 0:
            print("ERROR: Character has no job classes")
            return
        for index, job in enumerate(self.job_classes):
            print(f"[{index+1}] {job}")
        while True:
            choice = fs.is_int(input("Edit Job with index: "))
            if 1 <= choice <= len(self.job_classes):
                job_name, foo = self.job_classes[choice-1]
                level = fs.is_int(input("New level: "))
                del self.job_classes[choice-1]
                self.job_classes.append((job_name, level))
                print(f"DEBUGG: {job}'s level has been changed to {level}")
                self.update_job()
                return
            else:
                print("ERROR: Not in range")

    def equipment_add(self):
        self.equipment_reset()
        print("-------------------------")
        add_item: str = input("Add item: ").lower()
        if not fs.is_item(add_item):
            return
        level: int = fs.is_int(input("Item Level [1-5]: "))
        equipment: object = it.item_list(add_item, level)
        if equipment.type == "equipment":
            choice = input("Equip item? [Y/N]: ").upper()
            if choice == "Y":
                self.equipment_equip(add_item, level)
            else:
                self.inventory_add((add_item, level), 1)
        else:
            amount = fs.is_int(input("Amount: "))
            if equipment.type == "consumable":
                self.inventory_add((add_item, level), amount)
            else:
                self.inventory_add(add_item, amount)
        self.equipment_check()

    def equipment_remove(self):
        self.equipment_reset()
        equipment_ids = ["h", "c", "l", "s", "g", "be", "rh", "lh", "n", "r1", "r2", "br"]
        print("-------------------------")
        while True:
            choice = input("[R]emove, [U]nequip: ").upper()
            if choice == "R":
                while True:
                    remove = input("Remove slot [h, c, s, g...]: ").lower()
                    if remove in equipment_ids:
                        slot_rem = f"equipment_{remove}"
                        if fs.is_slot_taken(self, slot_rem):
                            setattr(self, slot_rem, None)
                        break
                break
            elif choice == "U":
                while True:
                    unequip = input("Unequip slot [h, c, s, g...]: ").lower()
                    if unequip in equipment_ids:
                        slot_unequip = f"equipment_{unequip}"
                        if fs.is_slot_taken(self, slot_unequip):
                            name, level = getattr(self, slot_unequip)
                            self.inventory_add((name, level), 1)
                            setattr(self, slot_unequip, None)
                        break
                break
        self.equipment_check()
    
    def equipment_equip(self, add_item, level):
        equipment_ids = ["h", "c", "l", "s", "g", "be", "rh", "lh", "n", "r1", "r2", "br"]
        while True:
            add_to: str = input("Equip to [h, c, s, g...]: ").lower()
            if add_to in equipment_ids:
                equip_slot: str = f"equipment_{add_to}"
                
                if fs.is_slot_taken(self, equip_slot):
                    replace = input("Slot already has equipment [R]eplace to Inv, Replace to [D]iscard: ").upper()
                    if replace == "R":
                        currently_equipped: tuple[str, int] = getattr(self, equip_slot, None)
                        self.inventory_add(currently_equipped, 1)
                    setattr(self, equip_slot, (add_item, level))
                else:
                    setattr(self, equip_slot, (add_item, level))
                print(f"{add_item} added to {self.firstname} {self.surname}")
                break
            else:
                print("ERROR: Invalid slot")

    def inventory_equip(self):
        self.equipment_reset()
        equipable_items: list = []

        for item in self.inventory:
            item_name, amount = item
            if not fs.is_tuple(item_name):
                continue
            name, level = item_name
            got_item = it.item_list(name, level)
            if got_item.type != "equipment":
                continue
            equipable_items.append((name, level))

        if not equipable_items:
            self.equipment_check()
            return

        for index, item in enumerate(equipable_items):
            name, level = item
            got_item = it.item_list(name, level)
            print(f"{[index+1]} {got_item.name}")

        while True:
            equip: int = fs.is_int(input("Equip ID: "))
            if equip <= len(equipable_items) and equip > 0:
                break
            
        item: tuple[str, int] = equipable_items[equip-1]
        name, level = item
        self.equipment_equip(name, level)
        for index, item in enumerate(self.inventory):
            item_name, item_amount = item
            if not fs.is_tuple(item_name):
                continue
            item_name, item_level = item_name
            if item_name == name and level == item_level:
                if item_amount == 1:
                    del self.inventory[index]
                else:
                    self.inventory[index] = ((item_name, item_level), item_amount-1)
        self.equipment_check()

    def inventory_add(self, add_item, add_amount: int):
        item_exists = False
        if self.inventory is None:
            self.inventory.append((add_item, add_amount))
        else:
            for i, (item, amount) in enumerate(self.inventory):
                if item == add_item:
                    self.inventory[i] = (item, amount+add_amount)
                    print(f"Added {add_amount} {item}s to {self.firstname} {self.surname}")
                    item_exists = True
                    break
            if not item_exists:
                self.inventory.append((add_item, add_amount))

    def inventory_remove(self, remove: str, remove_amount: int, def_lvl: int = 0):
        remove_list: list[tuple] = []

        #  Check for identical items
        if def_lvl == 0:
            for item in self.inventory:
                name, amount = item
                if fs.is_tuple(name):
                    name, level = name
                    if name == remove:
                        remove_list.append(item)
            if len(remove_list) > 1:
                for index, item in enumerate(remove_list):
                    name, foo = item
                    name, level = name
                    item_object = it.item_list(name, level)
                    print(f"[{index+1}] {item_object.name}")
                remove = fs.is_int(input("Remove item with ID: "))
                remove = remove_list[remove-1]
                remove_name, foo = remove
                if fs.is_tuple(remove_name):
                    remove_name, remove_level = remove_name
            else:
                for index, item in enumerate(self.inventory):
                    item_name, item_amount = item
                    if fs.is_tuple(item_name):
                        item_name, item_level = item_name
                        if item_name == remove:
                            remove_name = item_name
                    else:
                        remove_level = 0
                        remove_name = item_name
        else:
            remove_name = remove
            remove_level = def_lvl
        
        #  Remove Selected Item
        for index, item in enumerate(self.inventory):
            item_name, item_amount = item
            if fs.is_tuple(item_name):
                item_name, item_level = item_name
                if len(remove_list) == 1:
                    remove_level = item_level
                w_item = it.item_list(item_name, item_level)
                self.weight -= w_item.weight
                if item_name == remove_name and item_level == remove_level:
                    if item_amount > 1 and not item_amount == remove_amount:
                        print(f"Removed {remove_amount} {self.inventory[index]}")
                        self.inventory[index] = ((item_name, item_level), item_amount-remove_amount)
                    else:
                        print(f"Removed {self.inventory[index]}")
                        del self.inventory[index]
            else:
                if item_name == remove_name:
                    w_item = it.item_list(item_name, 2)
                    self.weight -= w_item.weight
                    if item_amount > 1 and not item_amount == remove_amount:
                        print(f"Removed {remove_amount} {self.inventory[index]}")
                        self.inventory[index] = (item_name, item_amount-remove_amount)
                    else:
                        print(f"Removed {self.inventory[index]}")
                        del self.inventory[index]
        remove_list.clear()

    def inventory_use(self) -> None:
        consumables: list[tuple[object, int, str]] = []

        #  Find consumables
        for i in self.inventory:
            name, amount = i
            if fs.is_tuple(name):
                name, level = name
            else:
                level = 2
            item: object = it.item_list(name, level)
            if item.type == "consumable":
                consumables.append((item, amount, name))

        #  Select consumable
        if consumables:
            for index, consumable in enumerate(consumables):
                item, amount, name = consumable
                print(f"[{index+1}] {item.name} [Amount: {amount}]")

            while True:
                choice = fs.is_int(input("Consume item ID: "))
                if 1 <= choice <= len(consumables):
                    consumable, amount, con_name = consumables[choice-1]
                    consume_amount = fs.is_int(input(f"Consume amount [{amount}]: "))
                    for effect in consumable.status_effects:
                        if effect.is_effect:
                            spell_effect = fs.is_int(input(f"Spell Effect for {effect.name}: "))
                        else:
                            spell_effect = 1
                        self.status_effects.append(effect)
                        self.status_apply(effect, spell_effect)
                    self.inventory_remove(con_name, consume_amount, consumable.level)
                    break

    

    def status_apply(self, effect: object, spell_effect: int):
        print(f"Applied {effect.name}")
        if effect.is_effect:
            effect.spell_effect=spell_effect
        effect.apply_bonus(self)
        self.new_hp += effect.new_hp
        self.new_mp += effect.new_mp
        self.new_sp += effect.new_sp
        self.new_phyatk += effect.new_phyatk
        self.new_phydef += effect.new_phydef
        self.new_agility += effect.new_agility
        self.new_finess += effect.new_finess
        self.new_magatk += effect.new_magatk
        self.new_magdef += effect.new_magdef
        self.new_resistance += effect.new_resistance
        self.new_special += effect.new_special
        self.new_athletics += effect.new_athletics
        self.new_acrobatics += effect.new_acrobatics
        self.new_stealth += effect.new_stealth
        self.new_sleight += effect.new_sleight
        self.new_investigation += effect.new_investigation
        self.new_insight += effect.new_insight
        self.new_perception += effect.new_perception
        self.new_deception += effect.new_deception
        self.new_intimidation += effect.new_intimidation
        self.new_persuasion += effect.new_persuasion
        self.new_performance += effect.new_performance
        self.new_karma += effect.new_karma
        if effect.is_max:
            self.max_hp += effect.new_hp
            self.max_mp += effect.new_mp
            self.max_sp += effect.new_sp
            self.max_phyatk += effect.new_phyatk
            self.max_phydef += effect.new_phydef
            self.max_agility += effect.new_agility
            self.max_finess += effect.new_finess
            self.max_magatk += effect.new_magatk
            self.max_magdef += effect.new_magdef
            self.max_resistance += effect.new_resistance
            self.max_special += effect.new_special
            self.max_athletics += effect.new_athletics
            self.max_acrobatics += effect.new_acrobatics
            self.max_stealth += effect.new_stealth
            self.max_sleight += effect.new_sleight
            self.max_investigation += effect.new_investigation
            self.max_insight += effect.new_insight
            self.max_perception += effect.new_perception
            self.max_deception += effect.new_deception
            self.max_intimidation += effect.new_intimidation
            self.max_persuasion += effect.new_persuasion
            self.max_performance += effect.new_performance
            self.max_karma += effect.new_karma