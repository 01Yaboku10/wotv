import failsafe as fs
import gamelogic as gl
from colorama import Fore, Style, init
init(autoreset=True)

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
    
    def __repr__(self):
        name = gl.uncapitalize_string(self.name, " ")
        return f"['{name}', {self.time}, {self.success}, {self.is_effect}, {self.use_religion}, {self.affect_max}, {self.effect}, {self.spell_effect}]"
    
    def edit(self, player: object):
        while True:
            choice = input("Edit [T]ime, [E]ffect, [R]emove: ").upper()
            if choice == "E":
                print(f"Current Spell Effect: {self.spell_effect}")
                value = fs.is_int(input("New Effect: "))
                self.spell_effect = value
                self.apply_bonus(player)
                break
            elif choice == "T":
                print(f"Current Time: {self.time_left}/{self.time}")
                value = fs.is_int(input("New Time: "))
                self.time = value
                self.time_left = value
                self.time_left = value
                break
            elif choice == "R":
                self.remove(player, "r")
                break
    
    def remove(self, p: object, mode="d"):    #  p: player
        while True:
            if mode == "d":
                choice = "Y"
            else:
                choice = input("Are you sure? [Y/N]: ").upper()

            if choice == "N":
                break
            elif choice == "Y":
                p.new_hp -= self.new_hp
                p.new_mp -= self.new_mp
                p.new_sp -= self.new_sp
                p.new_phyatk -= self.new_phyatk
                p.new_phydef -= self.new_phydef
                p.new_agility -= self.new_agility
                p.new_finess -= self.new_finess
                p.new_magatk -= self.new_magatk
                p.new_magdef -= self.new_magdef
                p.new_resistance -= self.new_resistance
                p.new_special -= self.new_special
                p.new_athletics -= self.new_athletics
                p.new_acrobatics -= self.new_acrobatics
                p.new_stealth -= self.new_stealth
                p.new_sleight -= self.new_sleight
                p.new_investigation -= self.new_investigation
                p.new_insight -= self.new_insight
                p.new_perception -= self.new_perception
                p.new_deception -= self.new_deception
                p.new_intimidation -= self.new_intimidation
                p.new_persuasion -= self.new_persuasion
                p.new_performance -= self.new_performance
                p.new_karma -= self.new_karma
                if self.is_max:
                    p.max_hp -= self.new_hp
                    p.max_mp -= self.new_mp
                    p.max_sp -= self.new_sp
                    p.max_phyatk -= self.new_phyatk
                    p.max_phydef -= self.new_phydef
                    p.max_agility -= self.new_agility
                    p.max_finess -= self.new_finess
                    p.max_magatk -= self.new_magatk
                    p.max_magdef -= self.new_magdef
                    p.max_resistance -= self.new_resistance
                    p.max_special -= self.new_special
                    p.max_athletics -= self.new_athletics
                    p.max_acrobatics -= self.new_acrobatics
                    p.max_stealth -= self.new_stealth
                    p.max_sleight -= self.new_sleight
                    p.max_investigation -= self.new_investigation
                    p.max_insight -= self.new_insight
                    p.max_perception -= self.new_perception
                    p.max_deception -= self.new_deception
                    p.max_intimidation -= self.new_intimidation
                    p.max_persuasion -= self.new_persuasion
                    p.max_performance -= self.new_performance
                    p.max_karma -= self.new_karma
                
                print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} Removed {self.name}")
                break
        
    def apply_bonus(self, p: object) -> None:
        self.bonus = abs(self.spell_effect if self.is_effect else 1)
        if self.use_religion is not None:
            if self.use_religion != p.religion:
                self.bonus = -self.bonus
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
        self.new_perception = round(self.perception*(p.max_perception if self.affect_max else self.bonus))
        self.new_deception = round(self.deception*(p.max_deception if self.affect_max else self.bonus))
        self.new_intimidation = round(self.intimidation*(p.max_intimidation if self.affect_max else self.bonus))
        self.new_persuasion = round(self.persuasion*(p.max_persuasion if self.affect_max else self.bonus))
        self.new_performance = round(self.performance*(p.max_performance if self.affect_max else self.bonus))
        self.new_karma = round(self.karma*(p.max_karma if self.affect_max else self.bonus))

    def update_effect(self, effect: int) -> None:
        if self.ept:
            self.effect *= round(effect)
        else:
            self.effect = effect

def effect_list(effect_name: str, tim: int, succ: float, use_effect: bool = False, use_religion: str = None, affect_max: bool = False):
    effects_list = {
        # Spell Effects
        "ignite": Effect("Ignite", time=tim, time_left=tim, ept=True, effect=-0.2, success=succ),
        "corrosion": Effect("Corrosion", time=tim, time_left=tim, phydef=-1, is_effect=True, success=succ),
        "shock": Effect("Shock", time=tim, time_left=tim, perception=-0.3, agility=-0.5, is_effect=use_effect, success=succ, affect_max=affect_max),
        "stun": Effect("Stun", time=tim, time_left=tim, acrobatics=-100, agility=-100, success=succ),
        "increase_all_stats": Effect("Increase All Stats", time=tim, time_left=tim, religion=use_religion, success=succ, is_effect=True, is_max=True, effect=1, hp=1, sp=1, mp=1, phyatk=1, phydef=1, agility=1, finess=1, magatk=1, magdef=1, resistance=1, special=1),
        "increase_all_skills": Effect("Increase All Skills", time=tim, time_left=tim, religion=use_religion, success=succ, is_effect=True, is_max=True, effect=1, athletics=1, acrobatics=1, stealth=1, sleight=1, investigation=1, insight=1, perception=1, deception=1, intimidation=1, persuasion=1, performance=1),
        "glimmering_shield": Effect("Glimmering Shield", time=tim, time_left=tim, success=succ),

        # Items
        "anti-resistance": Effect("Anti-Resistance", time=tim, time_left=tim, success=succ, resistance=-10),
        "strength": Effect("Strength", time=tim, time_left=tim, success=succ, phyatk=25, athletics=10, resistance=-10),
        "swiftness": Effect("Swiftness", time=tim, time_left=tim, success=succ, agility=25, acrobatics=10, resistance=-10)
    }
    effect = effects_list[effect_name]
    return effect