class Job():
    def __init__(self,
                 name: str,
                 type: str,
                 level: int,
                 power_level: int = 0,
                 armor_class: str = "None",
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
        self.name = name
        self.type = type
        self.level = level
        self.power_level = power_level
        self.armor_class = armor_class
        self.hp = hp
        self.mp = mp
        self.sp = sp
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

    def __repr__(self) -> str:
        return (f"Job(name={self.name}, type={self.type}, power_level={self.power_level}, level={self.level}, armor_class={self.armor_class}, "
                f"hp={self.hp}, mp={self.mp}, phyatk={self.phyatk}, phydef={self.phydef}, agility={self.agility}, "
                f"finess={self.finess}, magatk={self.magatk}, magdef={self.magdef}, resistance={self.resistance}, "
                f"special={self.special}, athletics={self.athletics}, acrobatics={self.acrobatics}, stealth={self.stealth}, "
                f"sleight={self.sleight}, investigation={self.investigation}, insight={self.insight}, "
                f"perception={self.perception}, deception={self.deception}, intimidation={self.intimidation}, "
                f"persuasion={self.persuasion}, performance={self.performance})")

def job_list(job_name, level):
    job_class_list = {
        # Magic Caster
        "wizard": Job("Wizard", "magic", level, 30, "light", mp=1, magatk=1, magdef=1, investigation=1),
        "greater_wizard": Job("Greater Wizard", "magic", level, 50, "light", mp=1, magatk=1, magdef=1, investigation=1),
        "master_wizard": Job("Master Wizard", "magic", level, 125, "light", mp=1, magatk=1, magdef=1, investigation=1),
        "mage": Job("Mage", "magic", level, 30, "light", mp=1, magatk=1, magdef=1, investigation=1),
        "elemental_mage": Job("Elemental Mage", "magic", level, 30, mp=3, magatk=1, magdef=1, investigation=1),
        "spirit_tamer": Job("Spirit Tamer", "magic", level, 30, mp=2, resistance=-5, insight=2, performance=2),
        "greater_spirit_tamer": Job("Greater Spirit Tamer", "magic", level, 60, mp=2, resistance=-5, insight=2, performance=1),
        "master_spirit_tamer": Job("Master Spirit Tamer", "magic", level, 130, mp=2, resistance=-5, insight=2),
        "priest": Job("Priest", "magic", level, 30, "light", mp=1, resistance=10, magdef=2, magatk=1),
        "greater_priest": Job("Greater Priest", "magic", level, 30, "light", mp=1, resistance=10, magdef=2, magatk=1),
        "master_priest": Job("Master Priest", "magic", level, 30, "light", mp=1, resistance=10, magdef=2, magatk=1),

        # Warrior
        "knight": Job("Knight", "warrior", level, 25, "medium", sp= 1, phydef=1, phyatk=1, agility=1, athletics=1, perception=1),
        "greater_knight": Job("Greater Knight", "warrior", level, 50, "medium", phydef=1, sp= 1, phyatk=1, agility=1, athletics=1, perception=1),
        "master_knight": Job("Master Knight", "warrior", level, 125, "medium", phydef=1, sp= 1, phyatk=1, agility=1, athletics=1, perception=1),
        "tank": Job("Tank", "warrior", level, 40, "heavy", phydef=1, sp= 1, phyatk=1, athletics=1, perception=1),

        # Commander

        # Production
        "alchemist": Job("Alchemist", "magic", level, 20, finess=15, investigation=3, insight=2),
        "greater_alchemist": Job("Greater Alchemist", "magic", level, 40, finess=10, investigation=2, insight=1)
    }
    job_class = job_class_list[job_name]
    return job_class
