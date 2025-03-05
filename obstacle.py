import character as ch

def obstacle_list(obstacle: str) -> object:
    obstacle_dict = {
        "stone_wall": ch.Character(10000, "Stone Wall", "", character_type="Barrier", hp=1, phydef=75, magdef=75)
    }
    return obstacle_dict[obstacle]