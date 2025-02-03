import effects as ef

class Item():
    def __init__(self,
                 name: str,
                 type: str,  #  Item / Equipment  /  Consumable
                 level: int = 5,
                 armor_class: str = "No",
                 weight: int = 0,
                 status_effects: list = None,
                 send_obj: bool = False,
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
        if send_obj:
            self.use_obj = self
        else:
            self.use_obj = None
        self.status_effects = status_effects if status_effects is not None else []
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
        # Warrior
        "iron_helmet": Item("Iron Helmet", "equipment", level, "medium", 1.5, phydef=7, magdef=4, perception=3, stealth=-1, sleight=-1),
        "iron_chestplate": Item("Iron Chestplate", "equipment", level, "medium", 3, phydef=10, magdef=5, perception=2, stealth=-2, sleight=-1),
        "iron_leggings": Item("Iron Leggings", "equipment", level, "medium", 2.5, phydef=7, magdef=4, perception=2, stealth=-2, sleight=-1),
        "iron_boots": Item("Iron Boots", "equipment", level, "medium", 1, phydef=5, magdef=3, acrobatics=-1, perception=1, stealth=-2, sleight=-1),
        "iron_gloves": Item("Iron Gloves", "equipment", level, "medium", 1, phydef=5, magdef=3, finess=-10, perception=1, stealth=-1, sleight=-5),
        "warrior_belt": Item("Warrior Belt", "equipment", level, "light", 1, hp=5, sp=10, phyatk=8, phydef=8, athletics=7),
        "warrior_ring": Item("Warrior Ring", "equipment", level, weight=0.1, sp=8, phyatk=7, phydef=5, athletics=3),
        
        # Magic Caster
        "caster_hat": Item("Magic Caster Hat", "equipment", level, "light", 1, mp=10, phydef=5, magdef=10, magatk=10, resistance=5, special=5, investigation=3),
        "caster_robe": Item("Magic Caster Robe", "equipment", level, "light", 2, mp=8, phydef=8, magdef=15, magatk=15, resistance=5, special=5, investigation=2),
        "caster_leggings": Item("Magic Caster Leggings", "equipment", level, "light", 2.5, mp=5, phydef=8, magdef=15, magatk=8, resistance=5, special=5, investigation=2),
        "caster_boots": Item("Magic Caster Boots", "equipment", level, "light", 1, mp=3, phydef=4, magdef=8, magatk=8, agility=5, acrobatics=2, resistance=5, special=5, investigation=1),
        "caster_gloves": Item("Magic Caster Gloves", "equipment", level, "light", 1, mp=3, phydef=3, magdef=5, magatk=8, resistance=5, special=5, investigation=1),
        "magic_ring": Item("Magic Ring", "equipment", level, weight=0.1, mp=5, magatk=10, magdef=5, investigation=3),
        "caster_belt": Item("Magic Caster Belt", "equipment", level, "light", 1, hp=5, mp=5, magatk=8, magdef=8, athletics=3),
        
        # Rouge
        "leather_helmet": Item("Leather Helmet", "equipment", level, "light", 0.8, phydef=5, magdef=3, agility=8, perception=3, acrobatics=2, stealth=1),
        "leather_tunic": Item("Leather Tunic", "equipment", level, "light", 1.5, phydef=8, magdef=4, agility=3, perception=2, acrobatics=2, stealth=2),
        "leather_leggings": Item("Leather Leggings", "equipment", level, "light", 1, phydef=5, magdef=3, agility=10, perception=1, acrobatics=3, stealth=2),
        "leather_boots": Item("Leather Boots", "equipment", level, "light", 0.5, phydef=5, magdef=3, agility=10, stealth=2, perception=1, sleight=1, acrobatics=3),
        "leather_gloves": Item("Leather Gloves", "equipment", level, "light", 0.2, phydef=3, magdef=2, phyatk=5, sleight=5, stealth=2, finess=10),
        "leather_belt": Item("Leather Belt", "equipment", level, "light", 1, athletics=3, hp=5, sp=10, phydef=3, magdef=3, acrobatics=-1),

        # Tank
        "plate_helmet": Item("Full-Plate Helmet", "equipment", level, "heavy", 3, phydef=10, magatk=5, perception=3, stealth=-2, sleight=-2, acrobatics=-1, agility=-3),
        "plate_chestplate": Item("Full-Plate Chestplate", "equipment", level, "heavy", 6, phydef=15, magdef=8, perception=2, stealth=-4, sleight=-2, acrobatics=-3, agility=-5),
        "plate_leggings": Item("Full-Plate Leggings", "equipment", level, "heavy", 5, phydef=10, magdef=5, perception=2, acrobatics=-2, stealth=-5, sleight=-1, agility=-5),
        "plate_boots": Item("Full-Plate Boots", "equipment", level, "heavy", 2, phydef=8, magdef=4, perception=1, acrobatics=-2, agility=-5, stealth=-2, sleight=-1),
        "plate_gloves": Item("Full-Plate Gloves", "equipment", level, "heavy", 2, phydef=8, magdef=4, perception=1, acrobatics=-1, finess=-20, stealth=-1, sleight=-5, agility=-1),
        
        # Weapons
        "dwarvern_sword": Item("Dwarvern Sword", "equipment", level, "medium", 2, mp=5, phyatk=10, agility=-5, magatk=5, special=5, acrobatics=-2, intimidation=2),
        "steel_sword": Item("Steel Sword", "equipment", level, "medium", 2, phyatk=15, agility=-5, acrobatics=-2, intimidation=2),
        "steel_dagger": Item("Steel Dagger", "equipment", level, "light", 2, phyatk=7, agility=4, acrobatics=-1, intimidation=2),
        "steel_scythe": Item("Steel Scythe", "equipment", level, "medium", 2, phyatk=20, agility=-10, acrobatics=-2, intimidation=2),
        
        # Foods
        "apple": Item("Apple", "item", 2, weight=0.1),
        
        # Potions
        "mana_potion": Item("Potion of Mana", "consumable", level, weight=0.5, mp=25, resistance=-10),
        "stamina_potion": Item("Potion of Stamina", "consumable", level, weight=0.5, sp=25, resistance=-10),
        "strength_potion": Item("Potion of Strength", "consumable", level, weight=0.5, status_effects=[ef.effect_list("strength", 3, 1)]),
        "swiftness_potion": Item("Potion of Swiftness", "consumable", level, weight=0.5, status_effects=[ef.effect_list("swiftness", 3, 1)]),
        "healing_potion": Item("Healing Potion", "consumable", level, weight=0.5, hp=50, resistance=-10)

    }
    item = items_list[item_name]
    return item