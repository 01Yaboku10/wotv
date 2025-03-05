class Race():
    def __init__(self,
                 name: str,
                 type: str,
                 level: int,
                 armor_class: str = "No",
                 power_level: int = 0,
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
                 performance: int = 0,
                 abilites: list[str] = None) -> None:
        self.name = name
        self.type = type
        self.level = level
        self.armor_class = armor_class
        self.power_level = power_level
        self.hp = hp * level
        self.mp = mp * level
        self.sp = sp * level
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

        self.abilites = abilites if abilites is not None else []

    def __repr__(self) -> str:
        return (f"Race(name={self.name}, type={self.type}, level={self.level}, armor_class={self.armor_class}, "
                f"hp={self.hp}, mp={self.mp}, phyatk={self.phyatk}, phydef={self.phydef}, agility={self.agility}, "
                f"finess={self.finess}, magatk={self.magatk}, magdef={self.magdef}, resistance={self.resistance}, "
                f"special={self.special}, athletics={self.athletics}, acrobatics={self.acrobatics}, stealth={self.stealth}, "
                f"sleight={self.sleight}, investigation={self.investigation}, insight={self.insight}, "
                f"perception={self.perception}, deception={self.deception}, intimidation={self.intimidation}, "
                f"persuasion={self.persuasion}, performance={self.performance})")

def race_list(race_name: str, level: int) -> object:
    racial_class_list = {
        # Humanoid
        "human": Race("Human", "humanoid", 1, power_level=50, hp=30, mp=30, sp=40, phyatk=20, phydef=20, agility=20, finess=50, magatk=15, magdef=15, resistance=5, special=1, athletics=1, acrobatics=2, sleight=1, investigation=1, persuasion=1),
        "four_eye": Race("Four Eye", "humanoid", 1, power_level=40, hp=25, sp=30, mp=10, phyatk=30, phydef=25, agility=35, finess=40, magatk=10, magdef=10, resistance=10, special=5, athletics=2, acrobatics=2, investigation=2, insight=2, perception=3, intimidation=1, persuasion=1),
        "dwarf": Race("Dwarf", "humanoid", 1, power_level=50, hp=40, mp=10, sp=30, phyatk=30, phydef=25, agility=25, finess=65, magatk=5, magdef=20, resistance=10, special=1, athletics=1, stealth=1, sleight=1, investigation=1, insight=1, persuasion=1),
        "dark_dwarf": Race("Dark Dwarf", "humanoid", 1, power_level=50, hp=40, mp=10, sp=30, phyatk=30, phydef=25, agility=25, finess=65, magatk=5, magdef=20, resistance=10, special=1, athletics=1, stealth=1, sleight=1, investigation=2, insight=2),
        "dark_elf": Race("Dark Elf", "humanoid", 1, power_level=40, hp=35, mp=40, sp=30, phyatk=20, phydef=15, agility=40, finess=50, magatk=30, magdef=1, resistance=1, special=10, athletics=1, acrobatics=2, stealth=1, sleight=1, investigation=1, insight=1, perception=2, performance=1),
        "elf": Race("Elf", "humanoid", 1, power_level=40, hp=35, mp=40, sp=30, phyatk=20, phydef=15, agility=40, finess=50, magatk=30, magdef=1, resistance=1, special=35, athletics=1, acrobatics=2, stealth=1, sleight=1, investigation=1, insight=1, perception=2, performance=1),
        "rainbow_eye": Race("Rainbow Eye", "humanoid", 1, power_level=40, hp=40, mp=50, sp=20, phyatk=5, phydef=15, agility=20, finess=30, magatk=25, magdef=20, resistance=10, special=5, acrobatics=1, investigation=2, insight=2, perception=2, deception=1, persuasion=2, performance=3),
        "half_elf": Race("Half Elf", "humanoid", 1, power_level=40, hp=30, mp=35, sp=35, phyatk=20, phydef=20, agility=30, finess=50, magatk=30, magdef=10, resistance=5, special=5, athletics=1, sleight=1, investigation=1, insight=1, perception=1),
        
        # Demi-Human
        "bafolk": Race("Bafolk", "demi-human", level, power_level=25, hp=5, mp=0, sp=4, phyatk=5, phydef=4, agility=2, finess=2, magatk=0, magdef=1, resistance=1, athletics=2, acrobatics=1, deception=1, intimidation=1),
        "bafolk_lord": Race("Bafolk Lord", "demi-human", level, power_level=50, hp=1, sp=1, phyatk=1, agility=1, finess=1, magdef=1, resistance=1, special=1, athletics=3, acrobatics=2, deception=2, intimidation=2),
        "fairy": Race("Fairy", "demi-human", level, power_level=30, hp=2, mp=3, sp=1, phyatk=1, phydef=1, agility=4, finess=2, magatk=3, magdef=2, resistance=2, special=1, acrobatics=2, stealth=1, sleight=1, investigation=1, insight=1, perception=2, performance=2),
        "fairy_lord": Race("Fairy Lord", "demi-human", level, power_level=50, hp=1, mp=1, sp=1, agility=1, finess=2, magatk=1, magdef=1, resistance=1, special=1, acrobatics=1, investigation=1, insight=2, perception=2, performance=2),
        "fairy_king": Race("Fairy King", "demi-human", level, power_level=140, hp=1, mp=1, sp=1, agility=1, magatk=1, magdef=1, resistance=1, special=1, acrobatics=1, stealth=1, sleight=1, investigation=2, insight=2, perception=2, intimidation=1, persuasion=1, performance=1),
        "goblin": Race("Goblin", "demi-human", level, power_level=20, hp=2, sp=1, phyatk=1, phydef=1, agility=1, finess=1, magdef=1, magatk=1, resistance=1, special=1, sleight=1, perception=1),
        "goblin_lord": Race("Goblin Lord", "demi-human", level, power_level=40, hp=2, mp=1, sp=1, phyatk=1, phydef=1, agility=2, athletics=1, acrobatics=1, stealth=1, sleight=1, perception=1),
        "goblin_strategist": Race("Goblin Strategist", "demi-human", level, power_level=100, hp=2, mp=3, sp=3, phydef=1, magdef=1, special=2, persuasion=2, perception=2),

        # Heteromorph
        "spirit": Race("Spirit", "heteromorph", level, power_level=30, hp=2, mp=2, sp=1, phyatk=1, phydef=1, agility=2, finess=1, magatk=2, magdef=2, resistance=2, special=2, performance=2, stealth=2),
        "greater_spirit": Race("Greater Spirit", "heteromorph", level, power_level=50, hp=2, mp=2, sp=2, phyatk=1, phydef=1, agility=2, finess=1, magatk=2, magdef=2, resistance=2, special=2, performance=2, stealth=1),
        "spirit_god": Race("Spirit God", "heteromorph", level, power_level=140, hp=3, mp=4, sp=4, phyatk=2, phydef=2, agility=2, finess=2, magatk=2, magdef=1, resistance=3, special=1, perception=3, intimidation=2),
        "royal_spirit": Race("Royal Spirit", "heteromorph", level, power_level=200, hp=2, mp=3, sp=2, phyatk=2, phydef=2, magatk=2, magdef=2, resistance=2, special=2, insight=5, persuasion=2)
    }
    racial_class = racial_class_list[race_name]
    return racial_class