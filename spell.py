import effects as ef
import obstacle as ob
import failsafe as fs
import gamelogic as gl
import character as ch

from colorama import Fore, Style, init

init(autoreset=True)

class Spell():
    def __init__(self,
                 name: str,  #  Spell name
                 type: str,  #  e.g attack, buff, curse
                 tier: int,  #  Spell Tier 1-11
                 effect: int,  #  Damage/Heal amount
                 time: int,  #  Time spell is active (Not for effects)
                 multiplier: str,  #  magatk, phydef, special
                 attribute: str,  #  e.g water, fire, metal
                 use_mp: bool = False,  #  Does spell use MP?
                 use_sp: bool = False,  #  Does spell use SP?
                 target: str = "Single",  #  Use AOE for activation on all opponents in opponent list
                 enchant: str = None,  #  e.g pierce
                 status: list[object] = None,  #  List of status effects
                 karma: int = 0,  #  Karma consumed/added upon casted spell
                 cooldown: int = 0,
                 phydef: int = 0,
                 magdef: int = 0,
                 hp: int = 0,
                 is_max: bool = False,  #  Does the spell work it's affect as a % of max stats?
                 destroy: bool = False,  #  Extra Damage towards obstacles?
                 undead_b: bool = False,  # Extra Damange towards undead
                 floor: list[str] = None,  # Floor effect, e.g Fire, Acid etc
                 effect_is: str = "Effect",  # Is effect something else? e.g Effect is Range, Time etc
                 unique: bool = False,  # Does the spell have it's own function?
                 note: str = None,
                 obstacles: list[str] = None
                 ):
        self.name = name
        self.type = type
        self.tier = tier
        self.effect = effect
        self.time = time
        self.multiplier = multiplier
        self.attribute = attribute
        self.target = target
        self.enchant = enchant
        self.statuses = status
        self.karma = karma
        self.use_mp = use_mp
        self.use_sp = use_sp
        self.cooldown = cooldown
        self.hp = hp
        self.phydef = phydef
        self.magdef = magdef
        self.is_max = is_max
        self.destroy = destroy
        self.undead_b = undead_b
        self.floor = floor if floor is not None else []
        self.effect_is = effect_is
        self.unique = unique
        self.note = note
        self.obstacles = obstacles if obstacles is not None else []

    def __repr__(self) -> str:
        return (f"Name: {self.name}, Type: {self.type}, Tier: {self.tier}, Effect: {self.effect}, Duration: {self.time}, Attribute: {self.attribute}")
    
    def barrier_repr(self) -> str:
        return f"({self.name}, {self.time}, {self.new_hp}, {self.phydef}, {self.magdef})"

    def barrier(self, effect, player):
        if self.is_max:
            self.hp = effect*player.new_hp*0.01
            self.new_hp = self.hp
        else:
            self.new_hp = effect

    def purify(self, player: object, delete_list: list[object] = None) -> None:
        if player.status_effects:
            print("--------=Purify=--------")
            delete_list = delete_list if delete_list is not None else []
            for index, status in enumerate(player.status_effects):
                print(f"[{index+1}] {status.name} [{status.time_left}] turns")
            while True:
                delete = input("Remove status effect with index [D]one: ").upper()
                if delete == "D":
                    break
                delete = fs.is_int(delete)
                if 0 <= delete-1 <= len(player.status_effects):
                    effect = player.status_effects[delete-1]
                    if effect not in delete_list:
                        delete_list.append(effect)
            if delete_list:
                for effect in delete_list:
                    effect.remove(player)
                    player.status_effects.remove(effect)
                    print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} Effect {effect.name} has been purified from {player.prefix} {player.firstname}")

# UNIQUE LIGHT SPELLS
class Spell_CleansingLight(Spell):
    def init(self, player: object, opponent: object, save: float, caster_m: float, opponent_m: float, barrier_m: float, dice: int, players: dict[str, object], game: object):
        if opponent.race_type[1] == "undead":
            return "damage"
        else:
            self.purify(opponent)
            return "spell"

class Spell_FoxOfTheZenith(Spell):
    def init(self, player: object, opponent: object, save: float, caster_m: float, opponent_m: float, barrier_m: float, dice: int, players: dict[str, object], game: object):
        for index, (key, entity) in enumerate(players.items()):
            if entity.team != player.team:
                continue
            immunity = ef.effect_list("light_magic_immunity", 3, 1)
            game.status_effect_apply(immunity, entity, 1, 1)
        return "damage"
    
class Spell_StarlitBenediction(Spell):
    def init(self, player: object, opponent: object, save: float, caster_m: float, opponent_m: float, barrier_m: float, dice: int, players: dict[str, object], game: object, spell_enchants: list[str]):
        affinity = 1.25 if self.attribute in player.attribute else 1
        maximize = 1.25 if "M" in spell_enchants else 1
        for index, (key, entity) in enumerate(players.items()):
            if player.team != entity.team:
                continue
            effect = game.calc_effect(dice, self, 1, 1, 1, player.new_magatk, affinity, maximize, save, 0)
            if effect <= 10:
                entity.attribute_add("hp", 10)
            else:
                entity.attribute_add("hp", effect)
            self.purify(entity)
        return "spell"

class Spell_SunderingRadiance(Spell):
    def init(self, player: object, opponent: object, save: float, caster_m: float, opponent_m: float, barrier_m: float, dice: int, players: dict[str, object], game: object, spell_enchants: list[str]):
        max_level = 0
        race = opponent.race_type[1] if opponent.race_type[1] == "undead" else "alive"
        if race == "undead":
            race = 1.5
        else:
            race = 0.5
        if opponent.racial_classes:
            for clas in opponent.racial_classes:
                name, level = clas
                max_level += level
        if opponent.job_classes:
            for clas in opponent.job_classes:
                name, level = clas
                max_level += level
        print(max_level)
        if max_level <= 50:
            if race == 0.5:
                damage = -10
            else:
                damage = -100
        else:
            affinity = 1.25 if self.attribute in player.attribute else 1
            maximize = 1.25 if "M" in spell_enchants else 1
            damage = game.calc_effect(dice, self, opponent_m, 1, 1, caster_m, affinity, maximize, save, 0)*race
        opponent.attribute_add("hp", damage, True)
        return "spell"

class Spell_HaloOfTheTamer(Spell):
    def init(self, player: object, opponent: object, save: float, caster_m: float, opponent_m: float, barrier_m: float, dice: int, players: dict[str, object], game: object, spell_enchants: list[str]):
        print("---------=Halo of The Tamer=---------")
        affinity = 1.25 if self.attribute in player.attribute else 1
        maximize = 1.25 if "M" in spell_enchants else 1
        time = 2
        effect = game.calc_effect(dice, self, 1, 1, 1, caster_m, affinity, maximize, save, 0)
        print(effect)
        opponents = gl.opponent_assign(players)
        immunity = False

        if effect >= 0:
            print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} Halo of The Tamer gives +2 to attack rolls")
        if effect >= 2:
            print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} Halo of The Tamer gives night vision")
        if effect >= 3:
            print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} Halo of The Tamer gives insanity immunity")
            immunity = True
        if effect >= 4:
            print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} Halo of The Tamer lasts for 3 turns")
            time = 3
        
        for oppo in opponents:
            if immunity:
                game.status_effect_apply(ef.effect_list("insanity_immunity", time, 1), oppo, 1, 1)
            game.status_effect_apply(ef.effect_list("halo_of_the_tamer", time, 1), oppo, 1, 1)

class Spell_BeaconOfTheFox(Spell):
    def init(self, player: object, opponent: object, save: float, caster_m: float, opponent_m: float, barrier_m: float, dice: int, players: dict[str, object], game: object, spell_enchants: list[str]):
        affinity = 1.25 if self.attribute in player.attribute else 1
        maximize = 1.25 if "M" in spell_enchants else 1
        time = game.calc_effect(dice, self, 1, 1, 1, caster_m, affinity, maximize, save, 0)
        ch.list_combine(ch.character_list("5001", opponent.racial_classes, opponent.job_classes))
        entity = ch.character_dic.get("5001")
        if entity is not None:
            game.summon(player, entity, time)
        else:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Character 5001 could not be found... Cancelling Summoning")

class Spell_LuminousRebirth(Spell):
    def init(self, player: object, opponent: object, save: float, caster_m: float, opponent_m: float, barrier_m: float, dice: int, players: dict[str, object], game: object, spell_enchants: list[str]):
        affinity = 1.25 if self.attribute in player.attribute else 1
        maximize = 1.25 if "M" in spell_enchants else 1
        effect: int = game.calc_effect(dice, self, 1, 1, 1, caster_m, affinity, maximize, save, 0)*0.01
        opponent.new_hp = round(opponent.max_hp*effect)
        opponent.new_mp = round(opponent.max_mp*effect)
        gl.print_debugg("NOTE", f"{opponent.prefix} {opponent.firstname} revived with {opponent.new_hp} HP")

def spell_list(spell_name):
    spells_list = {
        #  SPELLS
        "magic_arrow": Spell("Magic Arrow", "Magical", 1, -2, 1, "magatk", "Mana", True),
        "acid_arrow": Spell("Acid Arrow", "Magical", 2, -4, 1, "magatk", "Acid", True, status=[ef.effect_list("corrosion", 2, 1)]),
        "shockwave": Spell("Shockwave", "Magical", 1, -2, 1, "magatk", "Air", True),
        "fireball": Spell("Fireball", "Magical", 3, -6, 2, "magatk", "Fire", True, status=[ef.effect_list("ignite", 2, 1)]),
        "earth_blast": Spell("Earth Blast", "Magical", 2, -4, 1, "magatk", "Earth", True),
        "thunderlance": Spell("Thunderlance", "Magical", 3, -8, 2, "magatk", "Thunder", True, status=[ef.effect_list("shock", 2, 1, True), ef.effect_list("stun", 1, 0.3)]),
        "greater_pact": Spell("Greater Pact", "Buff", 5, 5, 3, "magatk", "Holy", True, status=[ef.effect_list("increase_all_stats", 3, 1), ef.effect_list("increase_all_skills", 3, 1)], karma=-30, cooldown=3),
        "doomed_prophecy": Spell("Doomed Prophecy", "Magical", 6, 5, 3, "magatk", "Holy", True, "AOE", status=[ef.effect_list("increase_all_stats", 3, 1, use_religion="Vorgoth"), ef.effect_list("increase_all_skills", 3, 1, use_religion="Vorgoth")], karma=-20),
        "glimmering_shield": Spell("Glimmering Shield", "Barrier", 3, 10, 3, "magatk", "Mana", True, status=[ef.effect_list("glimmering_shield", 3, 1)], is_max=True),
        "stone_wall": Spell("Stone Wall", "Obstacle", 3, 15, 3, "magatk", "Earth", True, obstacles=["stone_wall"]),
        
        # Light Magic"
        "foxfire_touch": Spell("Foxfire Touch", "Buff", 1, 4, 3, "magatk", "Light", True, status=[ef.effect_list("foxfire_touch", 3, 1)]),
        "glimmer_dart": Spell("Glimmer Dart", "Magical", 1, -2, 1, "magatk", "Light", True, undead_b=True),
        "illuminated_path": Spell("Illuminated Path", "Buff", 1, 10, 1, "magatk", "Light", True, status=[ef.effect_list("illuminated_path", 2, 1)], effect_is="Range", floor=["illuminated_path"]),
        "spiritveil": Spell("Spiritveil", "Buff", 2, 10, 3, "magatk", "Light", True, status=[ef.effect_list("spiritveil", 2, 1, True)], effect_is="Stealth"),
        "sunburst_step": Spell("Sunburst Step", "Magical", 2, -4, 1, "magatk", "Light", True),
        "blinding_light": Spell("Blinding Light", "Debuff", 2, 20, 1, "Light", "magatk", True, status=[ef.effect_list("blinded", 1, 1)]),
        "foxfire_pack": Spell("Foxfire Pack", "Buff", 3, 2, 2, "magatk", "Light", True, status=[ef.effect_list("foxfire_pack", 2, 1, True)], effect_is="Save"),
        "blinding_flare": Spell("Blinding Flare", "Magical", 3, -5, 1, "magatk", "Light", True, status=[ef.effect_list("blinded", 1, 0.3)]),
        "spirit_reversal": Spell("Spirit Reversal", "Magical", 4, 10, 1, "magatk", "Light", True, status=[ef.effect_list("spirit_reversal", 3, 1, True)]),
        "cleansing_light": Spell_CleansingLight("Cleansing Light", "Magical", 4, -6, 1, "magatk", "Light", True, undead_b=True, status=[ef.effect_list("cleansing_light", 1, 1)], unique=True),
        "flash_step": Spell("Flash Step", "Buff", 4, 10, 1, "magatk", "Light", True, effect_is="Range"),
        "vulpine_mirror": Spell("Vulpine Mirror", "Buff", 5, 25, 3, "magatk", "Light", True, status=[ef.effect_list("vulpine_mirror", 3, 1, True)]),
        "solar_bloom": Spell("Solar Bloom", "Magical", 5, -8, 2, "magatk", "Light", True, status=[ef.effect_list("ignite", 2, 1, True)]),
        "halo_of_the_tamer": Spell_HaloOfTheTamer("Halo of The Tamer", "Buff", 5, 3, 1, "magatk", "Light", True, unique=True),
        "sanctified_ground": Spell("Sanctified Ground", "Buff", 6, 8, 2, "magatk", "Light", True, status=[ef.effect_list("sanctified_ground", 2, 1, True), ef.effect_list("charm_immunity", 2, 1)], floor=["sanctified_ground"]),
        "beacon_of_the_fox": Spell_BeaconOfTheFox("Beacon of The Fox", "Summon", 6, 3, 1, "magatk", "Light", True, unique=True, note="Opponent is the spirit of which the spell copies stats."),
        "nova_fang": Spell("Nova Fang", "Magical", 6, -10, 1, "magatk", "Light", True, enchant="pierce"),
        "astral_tailwind": Spell("Astral Tailwind", "Buff", 7, 4, 3, "magatk", "Light", True, status=[ef.effect_list("astral_tailwind", 3, 1, True), ef.effect_list("light_magic_immunity", 3, 1)], effect_is="Range"),
        "soul_link": Spell("Soul Link", "Buff", 7, 8, 3, "magatk", "Light", True, status=[ef.effect_list("soul_link", 3, 1)], effect_is="Range", note="Opponent should be both the caster and the target."),
        "radiant_silence": Spell("Radiant Silence", "Debuff", 7, 70, 1, "magatk", "Light", True, status=[ef.effect_list("blinded", 1, 1), ef.effect_list("silenced", 1, 1)]),
        "solar_cage": Spell("Solar Cage", "Debuff", 8, 60, 1, "magatk", "Light", True, status=[ef.effect_list("solar_cage", 1, 1), ef.effect_list("encumbered", 1, 1)]),
        "luminous_rebirth": Spell_LuminousRebirth("Luminous Rebirth", "Buff", 8, 50, 1, "magatk", "Light", True, status=[ef.effect_list("luminous_rebirth", 1, 1)], unique=True),
        "firefox": Spell("Firefox", "Magical", 8, -14, 1, "magatk", "Light", True, status=[ef.effect_list("ignite", 1, 1, True)], floor=["fire"]),
        "fox_of_the_zenith": Spell_FoxOfTheZenith("Fox of The Zenith", "Buff", 9, 4, 4, "magatk", "Light", True, status=[ef.effect_list("fox_of_the_zenith", 4, 1), ef.effect_list("increase_all_stats", 3, 1, True)], unique=True),
        "light_beam": Spell("Light Beam", "Magical", 6, -10, 1, "magatk", "Light", True),
        "starlit_benediction": Spell_StarlitBenediction("Starlit Benediction", "Buff", 9, 16, 1, "magatk", "Light", True, unique=True),
        "prismatic_tailstorm": Spell("prismatic_tailstorm", "Magical", 9, -16, 1, "magatk", "Light", True, undead_b=True),
        "light_eternal": Spell("Light Eternal", "Buff", 10, 10, 2, "magatk", "Light", True, status=[ef.effect_list("light_eternal", 2, 1)], effect_is="Range", floor=["light_eternal"]),
        "sundering_radiance": Spell_SunderingRadiance("Sundering Radiance", "Magical", 10, -18, 1, "magatk", "Light", True, undead_b=True, unique=True),
        "spirit_ascendant": Spell("Spirit Ascendant", "Buff", 10, 10, 1, "magatk", "Light", True, status=[ef.effect_list("spirit_ascendant", 3, 1), ef.effect_list("flight", 3, 1), ef.effect_list("increase_all_stats", 3, 1, True, ceff=2), ef.effect_list("increase_all_skills", 3, 1, True)])
    }
    spell: object = spells_list.get(spell_name)
    if spell is None:
        raise KeyError(f"'{spell_name}' not found in spell list.")
    return spell