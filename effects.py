import failsafe as fs

class Effect():
    def __init__(self,
                 name: str,
                 time: int = None,
                 time_left: int = None,
                 success: int = 0,
                 is_active: bool = False,
                 ept: bool = False,  #  Effect Per Turn, is the effect activated once per turn?
                 effect: int = 0,  #  Damage/Heal
                 is_effect: bool = False,
                 affect_max: bool = False,
                 is_max: bool = False,
                 spell_effect: int = 0,
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
                 karma: int = 0,
                 religion: str = None):
        self.name = name
        self.time = time
        self.time_left = time_left
        self.success = success
        self.is_active = is_active
        self.ept = ept
        self.effect = effect
        self.is_effect = is_effect
        self.affect_max = affect_max
        self.is_max = is_max
        self.spell_effect = spell_effect
        self.bonus = 1
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
        self.new_hp = hp
        self.new_mp = mp
        self.new_sp = sp
        self.new_phyatk = phyatk
        self.new_phydef = phydef
        self.new_agility = agility
        self.new_finess = finess
        self.new_magatk = magatk
        self.new_magdef = magdef
        self.new_resistance = resistance
        self.new_special = special
        self.new_athletics = athletics
        self.new_acrobatics = acrobatics
        self.new_stealth = stealth
        self.new_sleight = sleight
        self.new_investigation = investigation
        self.new_insight = insight
        self.new_perception = perception
        self.new_deception = deception
        self.new_intimidation = intimidation
        self.new_persuasion = persuasion
        self.new_performance = performance
        self.new_karma = karma
        self.karma = karma
        self.use_religion = religion
    
    def edit(self):
        choice = input("Edit [T]ime, [E]ffect").upper()
        if choice == "E":
            print(f"Current Spell Effect: {self.spell_effect}")
            value = fs.is_int(input("New Effect: "))
            self.spell_effect = value
        elif choice == "T":
            print(f"Current Time: {self.time_left}/{self.time}")
            value = fs.is_int(input("New Time: "))
            self.time = value
            self.time_left = value
            self.time_left = value

    def apply_bonus(self, p: object):
        self.bonus = abs(self.spell_effect if self.is_effect else 1)
        if self.use_religion is not None:
            print("DEBUGG: USING RELIGION")
            if self.use_religion != p.religion:
                bonus = -bonus
        self.new_hp = round(self.hp*(p.max_hp if self.affect_max else self.bonus))
        self.new_mp = round(self.mp*(p.max_sp if self.affect_max else self.bonus))
        self.new_sp = round(self.sp*(p.max_mp if self.affect_max else self.bonus))
        self.new_phyatk = round(self.phyatk*(p.max_phyatk if self.affect_max else self.bonus))
        self.new_phydef = round(self.phydef*(p.max_phydef if self.affect_max else self.bonus))
        self.new_agility = round(self.agility*(p.max_agility if self.affect_max else self.bonus))
        self.new_finess = round(self.finess*(p.max_finess if self.affect_max else self.bonus))
        self.new_magatk = round(self.magatk*(p.max_magatk if self.affect_max else self.bonus))
        self.new_magdef = round(self.magdef*(p.max_magdef if self.affect_max else self.bonus))
        self.new_resistance = round(self.resistance*(p.max_resistance if self.affect_max else self.bonus))
        self.new_special = round(self.special*(p.max_special if self.affect_max else self.bonus))
        self.new_athletics = round(self.athletics*(p.max_athletics if self.affect_max else self.bonus))
        self.new_acrobatics = round(self.acrobatics*(p.max_acrobatics if self.affect_max else self.bonus))
        self.new_stealth = round(self.stealth*(p.max_stealth if self.affect_max else self.bonus))
        self.new_sleight = round(self.sleight*(p.max_sleight if self.affect_max else self.bonus))
        self.new_investigation = round(self.investigation*(p.max_investigation if self.affect_max else self.bonus))
        self.new_insight = round(self.insight*(p.max_insight if self.affect_max else self.bonus))
        self.new_perception = round(self.perception*(p.max_preception if self.affect_max else self.bonus))
        self.new_deception = round(self.deception*(p.max_deception if self.affect_max else self.bonus))
        self.new_intimidation = round(self.intimidation*(p.max_intimidation if self.affect_max else self.bonus))
        self.new_persuasion = round(self.persuasion*(p.max_persuasion if self.affect_max else self.bonus))
        self.new_performance = round(self.performance*(p.max_performance if self.affect_max else self.bonus))
        self.new_karma = round(self.karma*(p.max_karma if self.affect_max else self.bonus))


def effect_list(effect_name: str, tim: int, succ: float, use_effect: bool = False, use_religion: str = None, affect_max: bool = False):
    effects_list = {
        "ignite": Effect("Ignite", time=tim, time_left=tim, ept=True, effect=-0.2, success=succ),
        "corrosion": Effect("Corrosion", time=tim, time_left=tim, phydef=-1, is_effect=True, success=succ),
        "shock": Effect("Shock", time=tim, time_left=tim, perception=-0.3, agility=-0.5, is_effect=use_effect, success=succ, affect_max=affect_max),
        "stun": Effect("Stun", time=tim, time_left=tim, acrobatics=-100, agility=-100, success=succ),
        "increase_all_stats": Effect("Increase All Stats", time=tim, time_left=tim, religion=use_religion, success=succ, is_effect=True, is_max=True, effect=1, hp=1, mp=1, phyatk=1, phydef=1, agility=1, finess=1, magatk=1, magdef=1, resistance=1, special=1),
        "increase_all_skills": Effect("Increase All Skills", time=tim, time_left=tim, religion=use_religion, success=succ, is_effect=True, is_max=True, effect=1, athletics=1, acrobatics=1, stealth=1, sleight=1, investigation=1, insight=1, perception=1, deception=1, intimidation=1, persuasion=1, performance=1)
    }
    effect = effects_list[effect_name]
    return effect