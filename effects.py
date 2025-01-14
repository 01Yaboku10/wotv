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
                 is_max: bool = False,
                 spell_effect: int = 0,
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
                 performance: int = 0,
                 karma: int = 0):
        self.name = name
        self.time = time
        self.time_left = time_left
        self.success = success
        self.is_active = is_active
        self.ept = ept
        self.effect = effect
        self.is_effect = is_effect
        self.is_max = is_max
        self.spell_effect = spell_effect
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
        self.karma = karma

def effect_list(effect_name: str, tim: int, succ: float, use_effect: bool = False):
    effects_list = {
        "ignite": Effect("Ignite", time=tim, time_left=tim, ept=True, effect=-0.2, success=succ),
        "corrosion": Effect("Corrosion", time=tim, time_left=tim, phydef=-1, is_effect=True, success=succ),
        "shock": Effect("Shock", time=tim, time_left=tim, perception=-0.3, agility=-0.5, is_effect=use_effect, success=succ),
        "stun": Effect("Stun", time=tim, time_left=tim, acrobatics=-100, agility=-100, success=succ),
        "increase_all_stats": Effect("Increase All Stats", time=tim, time_left=tim, success=succ, is_effect=True, is_max=True, effect=1, hp=1, mp=1, phyatk=1, phydef=1, agility=1, finess=1, magatk=1, magdef=1, resistance=1, special=1),
        "increase_all_skills": Effect("Increase All Skills", time=tim, time_left=tim, success=succ, is_effect=True, is_max=True, effect=1, athletics=1, acrobatics=1, stealth=1, sleight=1, investigation=1, insight=1, perception=1, deception=1, intimidation=1, persuasion=1, performance=1)
    }
    effect = effects_list[effect_name]
    return effect