import job_classes
import racial_classes
import failsafe as fs
id_list = []
character_dic = {}

class Character():
    def __init__(self,
                 id: int,
                 firstname: str,
                 surname: str,
                 attribute: list[str] = None,
                 karma: int = 0,
                 racial_classes: list[tuple[str, int]] = None,
                 job_classes: list[tuple[str, int]] = None,
                 power_level: int = 0,
                 hp: int = 0,
                 mp: int = 0,
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
        self.power_level = power_level
        self.karma = karma
        self.level = 0
        self.hp = hp
        self.mp = mp
        self.phyatk = phyatk
        self.phydef = phydef
        self.agility = agility
        self.finess = finess
        self.magatk = magatk
        self.magdef = magdef
        self.resistance = resistance
        self.special = special
        self.athletics = athletics
        self.acrobatics = acrobatics
        self.stealth = stealth
        self.sleight = sleight
        self.investigation = investigation
        self.insight = insight
        self.perception = perception
        self.deception = deception
        self.intimidation = intimidation
        self.persuasion = persuasion
        self.performance = performance

        self.race_type_list = []
        self.armor_classes = []
        self.armor_class = "None"

        self.update_race()
        self.update_job()

        self.id_check()
        self.race_check()
        self.armor_class_check()
        self.attribute_check()

        self.power_check()

    def __repr__(self) -> str:
        """return (f"Character(name={self.firstname, self.surname}, attribute={self.attribute}, type={self.race_type}, level={self.level}, power_level={self.power_level}, armor_class={self.armor_class}, "
                f"hp={self.hp}, mp={self.mp}, phyatk={self.phyatk}, phydef={self.phydef}, agility={self.agility}, "
                f"finess={self.finess}, magatk={self.magatk}, magdef={self.magdef}, resistance={self.resistance}, "
                f"special={self.special}, athletics={self.athletics}, acrobatics={self.acrobatics}, stealth={self.stealth}, "
                f"sleight={self.sleight}, investigation={self.investigation}, insight={self.insight}, "
                f"perception={self.perception}, deception={self.deception}, intimidation={self.intimidation}, "
                f"persuasion={self.persuasion}, performance={self.performance})")"""
        return (f"---------={self.firstname} {self.surname if self.surname is not None else ''}=---------\n"
            f"Level: {self.level}\n"
            f"Power Level: {self.power_level}\n"
            f"Racial Classes: {', '.join([f'{race[0]} [{race[1]}]' for race in self.racial_classes])}\n"
            f"Job Classes: {', '.join([f'{job[0]} [{job[1]}]' for job in self.job_classes])}\n"
            f"Karma: {self.karma}")

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
        self.acrobatics += round((((self.agility+self.finess)/2)*0.1))
        self.stealth += round((((self.agility+self.finess)/2)*0.1))
        self.sleight += round((((self.phyatk+self.finess+self.agility)/3)*0.1))
        self.investigation += round((((self.mp+self.finess+self.magatk+self.magdef)/4)*0.1))
        self.insight += round((((self.mp+self.magatk+self.magdef)/2)*0.1))
        self.perception += round((((self.phydef+self.magdef+self.resistance)/3)*0.1))
        self.deception += round((((self.phyatk+self.finess+self.magatk)/3)*0.1))
        self.intimidation += round((((self.hp+self.phyatk+self.magatk+self.special)/4)*0.1)+(self.power_level/2500))
        self.persuasion += round((((self.phyatk+self.finess+self.magatk)/3)*0.1))
        self.performance += round((((self.mp+self.agility+self.finess+self.special)/4)*0.1))

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
        self.hp, self.mp, self.level, self.phyatk, self.phydef, self.agility, self.finess, self.magatk, self.magdef, self.resistance, self.special, self.athletics, self.acrobatics, self.stealth, self.sleight, self.investigation, self.insight, self.perception, self.deception, self.intimidation, self.persuasion, self.performance = (0,) * 22
        for raceclass in self.racial_classes:
            name, level = raceclass
            race = racial_classes.race_list(name, level)
            self.hp += race.hp
            self.mp += race.mp
            self.level += level
            self.phyatk += race.phyatk
            self.phydef += race.phydef
            self.agility += race.agility
            self.finess += race.finess
            self.magatk += race.magatk
            self.magdef += race.magdef
            self.resistance += race.resistance
            self.special += race.special
            self.athletics += race.athletics
            self.acrobatics += race.acrobatics
            self.stealth += race.stealth
            self.sleight += race.sleight
            self.investigation += race.investigation
            self.insight += race.insight
            self.perception += race.perception
            self.deception += race.deception
            self.intimidation += race.intimidation
            self.persuasion += race.persuasion
            self.performance += race.performance

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
        if not fs.is_race(race):
            return
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
        if not fs.is_job(job):
            return
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