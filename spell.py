import effects as ef

class Spell():
    def __init__(self, 
                 name: str, 
                 type: str,  #  e.g attack, buff, curse
                 tier: int, 
                 effect: int, 
                 time: int,
                 multiplier: str,  #  magatk, phydef, special
                 attribute: str,  #  e.g water, fire, metal
                 target: str = "Single",
                 enchant: str = None,  #  e.g pierce
                 status: list[object] = None,
                 karma: int = 0
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

    def __repr__(self) -> str:
        return (f"Name: {self.name}, Type: {self.type}, Tier: {self.tier}, Effect: {self.effect}, Duration: {self.time}, Attribute: {self.attribute}")

def spell_list(spell_name):
    spells_list = {
        "magic_arrow": Spell("Magic Arrow", "Magical", 1, -5, 1, "magatk", "Mana"),
        "acid_arrow": Spell("Acid Arrow", "Magical", 2, -7, 1, "magatk", "Acid", status=[ef.effect_list("corrosion", 2, 1)]),
        "shockwave": Spell("Shockwave", "Magical", 1, -5, 1, "magatk", "Air"),
        "fireball": Spell("Fireball", "Magical", 3, -8, 2, "magatk", "Fire", "1", status=[ef.effect_list("ignite", 2, 1)]),
        "earth_blast": Spell("Earth Blast", "Magical", 2, -7, 1, "magatk", "Earth"),
        "thunderlance": Spell("Thunderlance", "Magical", 3, -12, 2, "magatk", "Thunder", status=[ef.effect_list("shock", 2, 1, True), ef.effect_list("stun", 1, 0.3)]),
        "greater_pact": Spell("Greater Pact", "Buff", 5, 5, 3, "magatk", "Holy", status=[ef.effect_list("increase_all_stats", 3, 1), ef.effect_list("increase_all_skills", 3, 1)], karma=-30),
        "doomed_prophecy": Spell("Doomed Prophecy", "Magical", 6, 5, 3, "magatk", "Holy", "AOE", status=[ef.effect_list("increase_all_stats", 3, 1, use_religion="Vorgoth"), ef.effect_list("increase_all_skills", 3, 1, use_religion="Vorgoth")], karma=-20)
    }
    spell = spells_list[spell_name]
    return spell
