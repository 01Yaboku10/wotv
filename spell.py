import effects as ef

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
                 is_max: bool = False  #  Does the spell work it's affect as a % of max stats?
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

    def __repr__(self) -> str:
        return (f"Name: {self.name}, Type: {self.type}, Tier: {self.tier}, Effect: {self.effect}, Duration: {self.time}, Attribute: {self.attribute}")

    def barrier(self, effect, player):
        if self.is_max:
            self.hp = effect*player.new_hp*0.01
            self.new_hp = self.hp
        else:
            self.new_hp = effect

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
        "glimmering_shield": Spell("Glimmering Shield", "Barrier", 3, 10, 3, "magatk", "Mana", True, status=[ef.effect_list("glimmering_shield", 3, 1)], is_max=True)
    }
    spell = spells_list[spell_name]
    return spell