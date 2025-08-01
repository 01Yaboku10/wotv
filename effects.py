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
                 religion: str = None,
                 interupt: list[str] = None,  # ["attacked", "attack"]
                 save: int = 0,  # Additional point for saving throw
                 activate_unique: list[str] = None,  # ["attacked", "attack", "attacked_after"]
                 c_effect_m: int = 0,
                 immunities: list[str] = None,
                 effect_type: str = "spell",
                 heal_tag: list[str] = None
                 ):
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
        self.interupt = interupt if interupt is not None else []
        self.save = save
        self.activate_unique = activate_unique if activate_unique is not None else []
        self.c_effect_m = c_effect_m
        self.immunities = immunities
        self.effect_type = effect_type
        self.heal_tag = heal_tag if heal_tag is not None else []
        self.applied = False

        if self.spell_effect != 0 and self.ept and self.is_effect:
            self.effect = self.effect * abs(self.spell_effect)
    
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
        if self.use_religion is not None and self.use_religion != p.religion:
            self.bonus = -self.bonus
        if self.c_effect_m != 0:
            self.bonus *= self.c_effect_m

        attributes = gl.SKILLS + gl.STATS + ["save", "karma"]

        for attr in attributes:
            if attr in ["save", "karma"]:
                if attr == "save":
                    self.save = round(self.save*self.bonus)
                else:
                    self.new_karma = round(self.karma*(p.max_karma if self.affect_max else self.bonus))
            else:
                new_val = round(getattr(self, attr)*(getattr(self, f"max_{attr}") if self.affect_max else self.bonus))
                effect, excession = fs.is_max(p, attr, new_val)
                effect = effect-excession  # If the spell will exceed level 100, it will reduce the potency to below 100
                setattr(self, f"new_{attr}", effect)

    def update_effect(self, effect: int) -> None:
        if self.ept:
            self.effect *= round(effect)
        else:
            self.effect = effect

class Effect_VulpineMirror(Effect):
    def init(self):  # Opponent = player who has the effect
        self.vulpine_mirror_multiplier = self.spell_effect*0.01
        self.vulpine_mirror_stack = 3
        print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} vulpine_mirror_multiplier = {self.vulpine_mirror_multiplier}")

    def attacked(self, player: object, opponent: object, game: object) -> str:  # Opponent = player who has the effect
        roll = fs.is_int(input("Save throw for Vulpine Mirror (D20): "))
        success: bool = 1-roll/20 <= self.vulpine_mirror_multiplier
        if success:
            print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} The Vulpine Fox absorbed the damage!")
            self.vulpine_mirror_stack -= 1
            if self.vulpine_mirror_stack <= 0:
                self.remove(opponent)
                opponent.status_effects.remove(self)
            else:
                print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} There are {self.vulpine_mirror_stack} Vulpine Mirror Foxes left.")
            return "spell"
        else:
            return "damage"

class Effect_LightEternal(Effect):
    def attacked_after(self, player: object):
        if player.new_hp <= 0:
            setattr(player, "new_hp", 1)
            print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} {player.prefix} {player.firstname} Resisted death with Light Eternal and now has {player.new_hp} HP")

class Effect_SoulLink(Effect):
    def attacked(self, player: object, opponent: object, game: object):
        gl.print_debugg("NOTE", f"{opponent.prefix} {opponent.firstname} has Soul Link!")
        print("--------=Soul Link=--------")
        while True:
            redirect: str = input("Redirect damage/heal [Y/N]: ").upper()
            if redirect not in ["Y", "N"]:
                continue
            if redirect == "N":
                return "damage"
            break
        while True:
            redirect: str = input("Redirect damage/heal to player with Prefix ID: ").upper().strip()
            if redirect not in game.player_prefixes:
                gl.print_debugg("ERROR", f"Player {redirect} not found...")
                continue
            break
        redirect: object = game.player_prefixes.get(redirect)
        if redirect is not None:
            return redirect
        else:
            return "damage"

def effect_list(effect_name: str, tim: int, succ: float, use_effect: bool = False, use_religion: str = None, affect_max: bool = False, spell_effect: int = 0, ceff: int = 0, heal_tag: list[str] = None):
    error: bool = False
    heal_tag = heal_tag if heal_tag is not None else []
    effects_list = {
        "error": Effect("Error", 1, 1, 1),
        # Spell Effects
        "ignite": Effect("Ignite", time=tim, time_left=tim, ept=True, effect=-0.2, success=succ, is_effect=use_effect, spell_effect=spell_effect, effect_type="debuff"),
        "corrosion": Effect("Corrosion", time=tim, time_left=tim, phydef=-1, is_effect=True, success=succ, effect_type="debuff"),
        "shock": Effect("Shock", time=tim, time_left=tim, perception=-0.3, agility=-0.5, is_effect=use_effect, success=succ, affect_max=affect_max, effect_type="debuff"),
        "stun": Effect("Stun", time=tim, time_left=tim, acrobatics=-100, agility=-100, success=succ, effect_type="debuff"),
        "increase_all_stats": Effect("Increase All Stats", time=tim, time_left=tim, religion=use_religion, success=succ, is_effect=True, is_max=True, c_effect_m=ceff, effect=1, hp=1, sp=1, mp=1, phyatk=1, phydef=1, agility=1, finess=1, magatk=1, magdef=1, resistance=1, special=1),
        "increase_all_skills": Effect("Increase All Skills", time=tim, time_left=tim, religion=use_religion, success=succ, is_effect=True, is_max=True, c_effect_m=ceff, effect=1, athletics=1, acrobatics=1, stealth=1, sleight=1, investigation=1, insight=1, perception=1, deception=1, intimidation=1, persuasion=1, performance=1),
        "glimmering_shield": Effect("Glimmering Shield", time=tim, time_left=tim, success=succ),
        "foxfire_touch": Effect("Foxfire Touch", time=tim, time_left=tim, success=succ),
        "illuminated_path": Effect("Illuminated Path", time=tim, time_left=tim, success=succ, acrobatics=2),
        "spiritveil": Effect("Spiritveil", time=tim, time_left=tim, success=succ, is_effect=True, stealth=1, interupt=["attack","attacked"]),
        "blinded": Effect("Blinded", time=tim, time_left=tim, success=succ, effect_type="debuff"),
        "foxfire_pack": Effect("Foxfire Pack", time=tim, time_left=tim, success=succ, is_effect=True, save=1),
        "spirit_reversal": Effect("Spirit Reversal", time=tim, time_left=tim, success=succ),
        "cleansing_light": Effect("Cleansing Light", time=tim, time_left=tim, success=succ),
        "vulpine_mirror": Effect_VulpineMirror("Vulpine Mirror", time=tim, time_left=tim, success=succ, is_effect=True, activate_unique=["attacked"]),
        "halo_of_the_tamer": Effect("Halo of The Tamer", time=tim, time_left=tim, success=succ),
        "sanctified_ground": Effect("Sanctified Ground", time=tim, time_left=tim, success=succ, ept=True, effect=1, is_effect=True, heal_tag=heal_tag),
        "sanctified_ground_floor": Effect("Sanctified Ground Floor", time=tim, time_left=tim, success=succ, ept=True, effect=spell_effect, is_effect=True, heal_tag=heal_tag),
        "astral_tailwind": Effect("Astral Tailwind", time=tim, time_left=tim, success=succ),
        "soul_link": Effect_SoulLink("Soul Link", time=tim, time_left=tim, success=succ, activate_unique=["attacked"]),
        "suppressed": Effect("Suppresed", time=tim, time_left=tim, success=succ, effect_type="debuff"),
        "silenced": Effect("Suppresed", time=tim, time_left=tim, success=succ, effect_type="debuff"),
        "solar_cage": Effect("Solar Cage", time=tim, time_left=tim, success=succ, ept=True, effect=-10, effect_type="debuff"),
        "encumbered": Effect("Encumbered", time=tim, time_left=tim, success=succ, effect_type="debuff"),
        "luminous_rebirth": Effect("Luminous Rebirth", time=tim, time_left=tim, success=succ),
        "fox_of_the_zenith": Effect("Fox of The Zenith", time=tim, time_left=tim, success=succ),
        "purify": Effect("Purify", time=tim, time_left=tim, success=succ),
        "light_eternal": Effect_LightEternal("Light Eternal", time=tim, time_left=tim, success=succ, activate_unique=["attacked_after"]),
        "spirit_ascendant": Effect("Spirit Ascendant", time=tim, time_left=tim, success=succ),
        "flight": Effect("Flight", time=tim, time_left=tim, success=succ),
        
        # Immunites
        "charm_immunity": Effect("Charm Immunity", time=tim, time_left=tim, success=succ, immunities=["charm"]),
        "slow_immunity": Effect("Slow Immunity", time=tim, time_left=tim, success=succ, immunities=["slow"]),
        "debuff_immunity": Effect("Debuff Immunity", time=tim, time_left=tim, success=succ, immunities=["debuff"]),
        "light_magic_immunity": Effect("Light Magic Immunity", time=tim, time_left=tim, success=succ, immunities=["light"]),
        "insanity_immunity": Effect("Insanity Immunity", time=tim, time_left=tim, success=succ, immunities=["insanity"]),
        "fire_immunity": Effect("Fire Immunity", time=tim, time_left=tim, success=succ, immunities=["ignite", "fire"]),

        # Items
        "anti-resistance": Effect("Anti-Resistance", time=tim, time_left=tim, success=succ, resistance=-10),
        "strength": Effect("Strength", time=tim, time_left=tim, success=succ, phyatk=25, athletics=10, resistance=-10),
        "swiftness": Effect("Swiftness", time=tim, time_left=tim, success=succ, agility=25, acrobatics=10, resistance=-10)
    }
    try:
        effect = effects_list[effect_name]
    except KeyError:
        gl.print_debugg("ERROR", f"The effect '{effect_name}' could not be found...")
        error = True
    if error:
        return effects_list["error"]
    else:
        return effect