import effects as ef

class Floor():
    def __init__(self, name: str, effect: int = 0, spell: str = None, caster: str = "Ulkaraz", time: int = -1, prefix: str = None, status_effects: list[object] = None):
        self.name = name
        self.effect = effect
        self.spell = spell  # spellname in lower
        self.caster = caster  # Prefix ID
        self.time = time  # -1 is infinite
        self.prefix = prefix
        self.status_effects = status_effects if status_effects is not None else []

def floor_list(floor_effect: str, effect: int = 0, spell: str = None, caster: str = "Ulkaraz", time: int = -1) -> object:
    floor_dict = {
        "fire": Floor("Fire", effect, spell, caster, time, status_effects=[ef.effect_list("ignite", 1, 1, True, spell_effect=effect)]),
        "illuminated_path": Floor("Illuminated Path", effect, spell, caster, 2, status_effects=[ef.effect_list("illuminated_path", 1, 1)]),
        "sanctified_ground": Floor("Sanctified Ground", effect, spell, caster, time, status_effects=[ef.effect_list("sanctified_ground_floor", 1, 1, spell_effect=effect), ef.effect_list("charm_immunity", 1, 1)]),
        "light_eternal": Floor("Light Eternal", effect, spell, caster, time, status_effects=[ef.effect_list("light_eternal", 1, 1)])
    }
    return floor_dict[floor_effect]