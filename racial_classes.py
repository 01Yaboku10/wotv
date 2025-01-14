class Race():
    def __init__(self,
                 name: str,
                 type: str,
                 level: int,
                 armor_class: str = "No",
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
        self.name = name
        self.type = type
        self.level = level
        self.armor_class = armor_class
        self.power_level = power_level
        self.hp = hp * level
        self.mp = mp * level
        self.phyatk = phyatk * level
        self.phydef = phydef * level
        self.agility = agility * level
        self.finess = finess * level
        self.magatk = magatk * level
        self.magdef = magdef * level
        self.resistance = resistance * level
        self.special = special * level
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

    def __repr__(self) -> str:
        return (f"Race(name={self.name}, type={self.type}, level={self.level}, armor_class={self.armor_class}, "
                f"hp={self.hp}, mp={self.mp}, phyatk={self.phyatk}, phydef={self.phydef}, agility={self.agility}, "
                f"finess={self.finess}, magatk={self.magatk}, magdef={self.magdef}, resistance={self.resistance}, "
                f"special={self.special}, athletics={self.athletics}, acrobatics={self.acrobatics}, stealth={self.stealth}, "
                f"sleight={self.sleight}, investigation={self.investigation}, insight={self.insight}, "
                f"perception={self.perception}, deception={self.deception}, intimidation={self.intimidation}, "
                f"persuasion={self.persuasion}, performance={self.performance})")

def race_list(race_name, level):
    racial_class_list = {
        "human": Race("Human", "humanoid", 1, power_level=50, hp=30, mp=30, phyatk=20, phydef=20, agility=20, finess=50, magatk=15, magdef=15, resistance=5, special=1, athletics=1, acrobatics=2, sleight=1, investigation=1, persuasion=1),
        "four_eye": Race("Four Eye", "humanoid", 1, power_level=40, hp=25, mp=10, phyatk=30, phydef=25, agility=35, finess=40, magatk=10, magdef=10, resistance=10, special=5, athletics=2, acrobatics=2, investigation=2, insight=2, perception=3, intimidation=1, persuasion=1),
        "dwarf": Race("Dwarf", "humanoid", 1, power_level=50, hp=40, mp=10, phyatk=30, phydef=25, agility=25, finess=65, magatk=5, magdef=20, resistance=10, special=1, athletics=1, stealth=1, sleight=1, investigation=1, insight=1, persuasion=1),
        "rainbow_eye": Race("Rainbow Eye", "humanoid", 1, power_level=40, hp=40, mp=50, phyatk=5, phydef=15, agility=20, finess=30, magatk=25, magdef=20, resistance=10, special=5, acrobatics=1, investigation=2, insight=2, perception=2, deception=1, persuasion=2, performance=3),
    }
    racial_class = racial_class_list[race_name]
    return racial_class