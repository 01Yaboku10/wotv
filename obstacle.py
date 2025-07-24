import character as ch

def obstacle_list(obstacle: str) -> object:
    obstacle_dict = {
        "stone_wall": ch.Character(9000, "Stone Wall", "", ["earth"], character_type="Barrier", hp=1, phydef=75, magdef=75)
    }
    return obstacle_dict[obstacle]