class Item():
    def __init__(self,
                 name: str,
                 type: str,  #  Item / Equipment  /  Consumable
                 level: int = 5,
                 armor_class: str = "No",
                 weight: int = 0,
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
        level_name_list = {
            5: "Divine ",
            4: "Legendary ",
            3: "Great ",
            2: "",
            1: "Flimsy "
        }
        level_stat_list = {
            5: 1,
            4: 0.75,
            3: 0.5,
            2: 0.25,
            1: 0.1
        }

        self.name = level_name_list[level] + name
        self.type = type
        self.level = level
        self.armor_class = armor_class
        self.weight = weight
        self.hp = round(hp*level_stat_list[level])
        self.mp = round(mp*level_stat_list[level])
        self.sp = round(sp*level_stat_list[level])
        self.phyatk = round(phyatk*level_stat_list[level])
        self.phydef = round(phydef*level_stat_list[level])
        self.agility = round(agility*level_stat_list[level])
        self.finess = round(finess*level_stat_list[level])
        self.magatk = round(magatk*level_stat_list[level])
        self.magdef = round(magdef*level_stat_list[level])
        self.resistance = round(resistance*level_stat_list[level])
        self.special = round(special*level_stat_list[level])
        self.athletics = round(athletics*level_stat_list[level])
        self.acrobatics = round(acrobatics*level_stat_list[level])
        self.stealth = round(stealth*level_stat_list[level])
        self.sleight = round(sleight*level_stat_list[level])
        self.investigation = round(investigation*level_stat_list[level])
        self.insight = round(insight*level_stat_list[level])
        self.perception = round(perception*level_stat_list[level])
        self.deception = round(deception*level_stat_list[level])
        self.intimidation = round(intimidation*level_stat_list[level])
        self.persuasion = round(persuasion*level_stat_list[level])
        self.performance = round(performance*level_stat_list[level])

    def __repr__(self) -> str:
        return (f"Item(name={self.name}, type={self.type}, level={self.level}, armor_class={self.armor_class}, weight={self.weight}, "
                f"hp={self.hp}, mp={self.mp}, phyatk={self.phyatk}, phydef={self.phydef}, agility={self.agility}, "
                f"finess={self.finess}, magatk={self.magatk}, magdef={self.magdef}, resistance={self.resistance}, "
                f"special={self.special}, athletics={self.athletics}, acrobatics={self.acrobatics}, stealth={self.stealth}, "
                f"sleight={self.sleight}, investigation={self.investigation}, insight={self.insight}, "
                f"perception={self.perception}, deception={self.deception}, intimidation={self.intimidation}, "
                f"persuasion={self.persuasion}, performance={self.performance})")
    
def item_list(item_name: str, level: int):
    items_list = {
        "iron_helmet": Item("Iron Helmet", "equipment", level, "medium", 1.5, phydef=7, magdef=7, perception=3, stealth=-1, sleight=-1),
        "iron_chestplate": Item("Iron Chestplate", "equipment", level, "medium", 3, phydef=10, magdef=8, perception=3, stealth=-2, sleight=-1),
        "iron_leggings": Item("Iron Leggings", "equipment", level, "medium", 2.5, phydef=7, magdef=6, perception=3, stealth=-2, sleight=-1),
        "iron_boots": Item("Iron Boots", "equipment", level, "medium", 1, phydef=5, magdef=4, acrobatics=-1, perception=3, stealth=-2, sleight=-1),
        "iron_gloves": Item("Iron Gloves", "equipment", level, "medium", 1, phydef=5, magdef=5, finess=-10, perception=3, stealth=-1, sleight=-5),
        "warrior_belt": Item("Warrior Belt", "equipment", level, "light", 1, hp=5, sp=5, phyatk=8, phydef=8, athletics=5),
        "warrior_ring": Item("Warrior Ring", "equipment", level, weight=0.1, sp=5, phyatk=7, phydef=5, athletics=3),
        "caster_hat": Item("Magic Caster Hat", "equipment", level, "light", 1, mp=10, phydef=5, magdef=10, magatk=10, resistance=5, special=5, investigation=3),
        "caster_robe": Item("Magic Caster Robe", "equipment", level, "light", 2, mp=8, phydef=5, magdef=15, magatk=15, resistance=5, special=5, investigation=3),
        "caster_leggings": Item("Magic Caster Leggings", "equipment", level, "light", 2.5, mp=5, phydef=5, magdef=15, magatk=8, resistance=5, special=5, investigation=3),
        "caster_boots": Item("Magic Caster Boots", "equipment", level, "light", 1, mp=3, phydef=5, magdef=8, magatk=8, agility=5, acrobatics=2, resistance=5, special=5, investigation=3),
        "caster_gloves": Item("Magic Caster Gloves", "equipment", level, "light", 1, mp=3, phydef=5, magdef=5, magatk=8, resistance=5, special=5, investigation=3),
        "magic_ring": Item("Magic Ring", "equipment", level, weight=0.1, mp=5, magatk=10, magdef=5, investigation=3),
        "caster_belt": Item("Magic Caster Belt", "equipment", level, "light", 1, hp=5, mp=5, magatk=8, magdef=8, athletics=3),
        "apple": Item("Apple", "consumable", 2, weight=0.1)
    }
    item = items_list[item_name]
    return item