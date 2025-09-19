import failsafe as fs
import gamelogic as gl
from colorama import Fore, Style, init
init(autoreset=True)

class Ability():
    def __init__(self,
                 name: str,
                 time: int = -1,  #  -1 indicates infinate time
                 cooldown: int = 0,
                 surrounding_amount: int = 0,
                 surrounding_boost: int = 1,
                 damage_boost: int = 1,
                 is_max: bool = False,  #  Does it affect the max stats?
                 is_per: bool = False,  #  Is percentage of player's stats?
                 use_self: bool = False,  #  Does the spell use the characters stats?
                 use_max: bool = False,  #  Does the spell use the MAX stat form the player?
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
                 boost: int = 1):
        self.name = name
        self.time = time
        self.cooldown = cooldown
        self.surrounding_amount = surrounding_amount
        self.surrounding_boost = surrounding_boost
        self.damage_boost = damage_boost
        self.is_max = is_max
        self.is_per = is_per
        self.use_self = use_self
        self.use_max = use_max
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
        self.karma = karma
        self.boost = boost

    def edit(self, player: object) -> None:
        while True:
            choices = ["T", "C", "S"]
            choice = input("[T]ime, [C]ooldown, [S]urounding Amount: ").upper().strip()
            if choice not in choices:
                print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Option does no exist.")
                continue
            value = fs.is_int(input("New value: "))
            if choice == "T":
                self.time = value
                break
            elif choice == "C":
                self.cooldown = value
                break
            elif choice == "S":
                player.ability_remove(self)
                self.surrounding_amount = value
                player.ability_apply(self)
                break

    def apply_per(self, player: object) -> None:
        self.boost_update()
        for stat in gl.STATS + gl.SKILLS:
            if getattr(self, stat) == 0:  # Skip if 0
                continue
            if self.use_self:
                if self.use_max:
                    setattr(self, stat, round(getattr(player, f"max_{stat}")*(self.boost-1)))
                setattr(self, stat, round(getattr(player, f"new_{stat}")*(self.boost-1)))
    
    def boost_update(self) -> None:
        if str(self.surrounding_boost).startswith("1") or str(self.surrounding_boost).startswith("2"):
            self.boost: int = 1+(self.surrounding_amount*(self.surrounding_boost-1))
        else:
            self.boost: int = 1-(self.surrounding_amount*(1-self.surrounding_boost))


def ability_list(ability: str) -> object:
    abilites = {
        # Goblin
        "mob_muscle": Ability("Mob Muscle", surrounding_amount=1, surrounding_boost=1.05, is_max=True, is_per=True, use_self=True, hp=1, mp=1, sp=1, phyatk=1, phydef=1, agility=1, finess=1, magatk=1, magdef=1, resistance=1, special=1, athletics=1, acrobatics=1, stealth=1, sleight=1, investigation=1, insight=1, perception=1, deception=1, intimidation=1, persuasion=1, performance=1),
        
        # Fairy King
        "disaster": Ability("Disaster")
    }
    return abilites[ability]