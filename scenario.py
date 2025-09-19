import gamelogic as gl
from colorama import Fore, Style, init
import random
import spell as sp
import failsafe as fs
import math
import effects as ef
import racial_classes as rc
import job_classes as jc
import saveloader as sl
import manu as menu
import sound as sd
import obstacle as ob
import flooreffect as fe
import item as it

init(autoreset=True)

class Game():
    def __init__(self, mode: str):
        self.hit_player = -1
        self.new_dice = 0
        if mode == "N":
            print("---------=New Scenario=---------")
            name = input("Name of Scenario: ").lower()
            self.scenario = Scenario(name)
            self.assigned_players, self.player_objects, self.player_prefixes = gl.player_assign()
            self.spirits: list[object] = sl.load_spirits(self.player_objects)
            self.obstacle_prefixes: dict[str, object] = {}
            self.floor_prefixes: dict[str, object] = {}
            for spirit in self.spirits:
                self.player_prefixes[spirit.prefix] = spirit
                self.player_objects.append(spirit)
                sl.update_spirit(spirit, "not start")
            self.summons: list[object] = sl.load_summons()
            gl.team_assign(self.player_objects)
            self.initiative_list = []
            print("---------=Teams=---------")
            print("Team 1:", end="")
            for player in self.player_objects:
                if player.team == 1:
                    print(f" ID:{player.id} {player.prefix} {player.firstname}", end="")
            print(".")
            print("Team 2:", end="")
            for player in self.player_objects:
                if player.team == 2:
                    print(f" ID:{player.id}  {player.prefix} {player.firstname}", end="")
            print(".")
            self.add_stats()
            while True:
                gamemode = input("Choose gamemode: [A]dventure, [B]attle: ").upper()
                if gamemode == "B":
                    self.scenario.mode = "battle"
                    self.gamemode_battle(False)
                    break
                elif gamemode == "A":
                    self.gamemode_adventure()
                    break
        elif mode == "L":
            print("---------=Load Scenario=---------")
            save = sl.disp_files("scenario_saves", "scenario_", ".txt")
            print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} Loading save {save}")
            self.assigned_players, self.player_objects, self.player_prefixes, sc = sl.load_scenario(save)
            self.scenario = Scenario(*sc)
            self.spirits: list[object] = sl.load_spirits(self.player_objects, True)
            self.obstacle_prefixes: dict[str, object] = self.scenario.obstacles
            self.floor_prefixes: dict[str, object] = self.scenario.floor
            self.summons: list[object] = sl.load_summons()
            self.initiative_list = []
            print("---------=Teams=---------")
            print("Team 1:", end="")
            for player in self.player_objects:
                if player.team == 1:
                    print(f" ID:{player.id} {player.prefix} {player.firstname}", end="")
            print(".")
            print("Team 2:", end="")
            for player in self.player_objects:
                if player.team == 2:
                    print(f" ID:{player.id} {player.prefix} {player.firstname}", end="")
            print(".")
            self.add_stats(load=True)
            if self.scenario.mode == "Adventure":
                self.gamemode_adventure()
            else:
                self.gamemode_battle(False, True)

    def add_stats(self, player: list[object] = None, load: bool = False):
        print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} Adding characters...")
        if player is not None:
            player_list = player
        else:
            player_list = self.player_objects

        for player in player_list:
            if not load:
                player.new_hp = player.hp
                player.new_mp = player.mp
                player.new_sp = player.sp
                player.new_phyatk = player.phyatk
                player.new_phydef = player.phydef
                player.new_agility = player.agility
                player.new_finess = player.finess
                player.new_magatk = player.magatk
                player.new_magdef = player.magdef
                player.new_resistance = player.resistance
                player.new_special = player.special
                player.new_athletics = player.athletics
                player.new_acrobatics = player.acrobatics
                player.new_stealth = player.stealth
                player.new_sleight = player.sleight
                player.new_investigation = player.investigation
                player.new_insight = player.insight
                player.new_perception = player.perception
                player.new_deception = player.deception
                player.new_intimidation = player.intimidation
                player.new_persuasion = player.persuasion
                player.new_performance = player.performance
                player.new_karma = player.karma
                player.max_hp = player.hp
                player.max_mp = player.mp
                player.max_sp = player.sp
                player.max_phyatk = player.phyatk
                player.max_phydef = player.phydef
                player.max_agility = player.agility
                player.max_finess = player.finess
                player.max_magatk = player.magatk
                player.max_magdef = player.magdef
                player.max_resistance = player.resistance
                player.max_special = player.special
                player.max_athletics = player.athletics
                player.max_acrobatics = player.acrobatics
                player.max_stealth = player.stealth
                player.max_sleight = player.sleight
                player.max_investigation = player.investigation
                player.max_insight = player.insight
                player.max_perception = player.perception
                player.max_deception = player.deception
                player.max_intimidation = player.intimidation
                player.max_persuasion = player.persuasion
                player.max_performance = player.performance
                player.max_karma = player.karma
                player.status_effects = []
                player.cooldowns = {}  # dict[str, int]
                player.barriers = []  # list[object]
            player.new_power_level = player.power_level
            sl.update_sheet(player)
            print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} Added: {player.firstname}")

    def status_update(self, player: object):
        self.summon_update(player)
        if player.status_effects:
            player_effects = player.status_effects[:]
            for effect in player_effects:
                if effect.ept:
                    for target in effect.ept_target:
                        print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} Player {player.prefix} {player.firstname} took {round(effect.effect)} to {target} from {effect.name}")
                        # player.new_hp += round(effect.effect)
                        player.attribute_add(target, round(effect.effect), False, effect)
                if effect.activate_unique:
                    if hasattr(effect, "update") and callable(getattr(effect, "update")):
                        effect.update()
                if effect.time_left <= 0:
                    effect.remove(player)
                    player.status_effects.remove(effect)
                else:
                    effect.time_left -= 1
                    print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} {player.prefix} {player.firstname} has {effect.name} for {effect.time_left} more turns")
        
        #  Cooldowns
        del_list = []
        for spell in player.cooldowns:
            if player.cooldowns[spell] != 0:
                player.cooldowns[spell] = player.cooldowns[spell]-1
            else:
                del_list.append(spell)
        if del_list:
            for spell in del_list:
                del player.cooldowns[spell]
                print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} {player.prefix} {player.firstname} can now use {spell} again")
        sl.update_sheet(player)
    
    def floor_update(self):
        del_list: list[str] = []
        for key, floor in self.floor_prefixes.items():
            if floor.time > 0:
                floor.time -= 1
            elif floor.time != -1:
                del_list.append(key)
        if not del_list:
            return
        for floor in del_list:
            del self.floor_prefixes[floor]
            print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} The Floor Effect {floor} has vanished.§")
    
    def summon_update(self, player: object):
        if player.summons:
            remove = []
            player_summons = player.summons[:]
            for index, summon in enumerate(player_summons):
                entity, time = summon
                if time <= 0:
                    remove.append((entity, time))
                    self.removed_players.append(entity)
                    del self.player_prefixes[entity.prefix]
                    self.player_objects.remove(entity)
                else:
                    time -= 1
                    player.summons[index] = (entity, time)
            for summon in remove:
                entity, time = summon
                print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} Player {player.prefix} {player.firstname}'s summon [{entity.prefix} {entity.firstname}] has run out")
                player.summons.remove(summon)
    
    def power_check(self, player: object):
        player.new_power_level = 0
        for raceclass in player.racial_classes:
            name, level = raceclass
            race = rc.race_list(name, level)
            player.new_power_level += race.power_level*level
        for jobclass in player.job_classes:
            name, level = jobclass
            job = jc.job_list(name, level)
            player.new_power_level += job.power_level*level
        player.new_power_level += (player.new_hp+player.new_mp+player.new_phyatk+player.new_phydef+player.new_agility+player.new_finess+player.new_magdef+player.new_magatk+player.new_resistance+player.new_special+ \
                            10*(player.new_athletics+player.new_acrobatics+player.new_stealth+player.new_sleight+player.new_deception+player.new_perception+player.new_performance+player.new_persuasion+player.new_insight+player.new_investigation+player.new_intimidation))

    def player_equipment(self):
        while True:
            set_player = input("Player Prefix ID [Q]uit: ").upper().strip()
            if set_player == "Q":
                return
            if set_player in self.player_prefixes:
                while True:
                    player = self.player_prefixes[set_player]
                    print(f"{player:equipment}")
                    choice = input("[A]dd, [R]emove, [U]se, [E]quip, [T]ransfer, [G]old, [D]one: ").upper()
                    if choice == "A":
                        player.equipment_add()
                    elif choice == "G":
                        while True:
                            choice = input("[A]dd, [R]emove, [T]ransfer: ").upper()
                            type = input("Type [G]old, [S]ilver, [B]ronze: ").lower()
                            amount = fs.is_int(input(f"{type.upper()} amount: "))
                            if choice == "A" or choice == "R":
                                if choice == "A":
                                    player.gold_add(type, amount)
                                    break
                                else:
                                    player.gold_remove(type, amount)
                                    break
                            elif choice == "T":
                                while True:
                                    transfer_to = input("Transfer to player with Prefix ID: ").upper()
                                    if transfer_to in self.player_prefixes:
                                        opponent = self.player_prefixes[transfer_to]
                                        player.gold_transfer(type, amount, opponent)
                                        sl.update_sheet(opponent)
                                        break
                                break
                        sl.update_sheet(player)
                        break
                    elif choice == "U":
                        scroll: str = player.inventory_use()
                        if fs.is_type(scroll, str):
                            self.spell_action(player, scroll)
                        else:
                            sl.update_sheet(player)
                    elif choice == "T":
                        if not player.inventory:
                            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Inventory Empty")
                            continue
                        for index, item in enumerate(player.inventory):
                            print(f"[{index+1}] {item}")
                        while True:
                            transfer = fs.is_int(input("Transfer item with ID: "))
                            if 1 <= transfer <= len(player.inventory):
                                transfer_item: tuple[str, int] = player.inventory[transfer-1]
                                item, amount = transfer_item
                                if amount > 1:
                                    amount = fs.is_int(input(f"Transfer Amount [{amount}]: "))
                                transfer_to = input("Transfer to player with prefix ID: ").upper()
                                if transfer_to in self.player_prefixes:
                                    if fs.is_type(item, tuple):
                                        send_item = item
                                        item, level = item
                                    else:
                                        send_item = item
                                        level = 0
                                    transfer_to = self.player_prefixes[transfer_to]
                                    transfer_to.inventory_add(send_item, amount)
                                    player.inventory_remove(item, amount, level)
                                    sl.update_sheet(transfer_to)
                                    break
                                else:
                                    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Player not found...")
                        
                    elif choice == "R":
                        while True:
                            remove = input("Remove from [I]nventory, [E]quipment: ").upper()
                            if remove == "I":
                                remove_item = input("Remove Item: ")
                                remove_amount = fs.is_int(input("Remove Amount: "))
                                player.equipment_reset()
                                player.inventory_remove(remove_item, remove_amount)
                                player.equipment_check()
                                break
                            elif remove == "E":
                                while True:
                                    mode = input("[R]emove, [A]ll, [B]ack: ").upper()
                                    if mode ==  "R":
                                        player.equipment_remove()
                                        sl.update_sheet(player)
                                        break
                                    elif mode == "A":
                                        while True:
                                            discard = input("Discard? Y/N: ").upper()
                                            if discard == "Y":
                                                player.equipment_all_unequip(True)
                                                sl.update_sheet(player)
                                                break
                                            elif discard == "N":
                                                player.equipment_all_unequip(False)
                                                sl.update_sheet(player)
                                                break
                                        break
                                break
                    elif choice == "E":
                        while True:
                            mode = input("[E]quip, [A]ll, [B]ack: ").upper()
                            if mode == "E":
                                player.inventory_equip()
                                sl.update_sheet(player)
                                break
                            elif mode == "A":
                                player.equipment_all_equip()
                                sl.update_sheet(player)
                                break
                            elif mode == "B":
                                self.player_equipment()
                                break
                    elif choice == "D":
                        break
                    player.weight_check()
                break

    def gamemode_adventure(self):
        self.removed_players = []
        sd.sound_menu("ambiance")
        while True:
            print("---------=Adventure=---------")
            action = input("[A]ction, [E]quipment, [U]pdate Effects, [B]attle: ").upper()
            if action == "A":
                while True:
                    choice = input("[A]ction or [G]od Action?: ").upper()
                    if choice == "G":
                        self.god_action()
                        break
                    elif choice == "A":
                        while True:
                            player = input("Player Prefix ID: ").upper()
                            if player in self.player_prefixes:
                                player = self.player_prefixes[player]
                                self.action(player)
                                break
                        break
            elif action == "E":
                self.player_equipment()
            elif action == "U":
                while True:
                    player = input("Player Prefix ID: ").upper()
                    if player == "UA":
                        for player in self.player_objects:
                            self.status_update(player)
                        break
                    elif player in self.player_prefixes:
                        player = self.player_prefixes[player]
                        self.status_update(player)
                        break
            elif action == "B":
                while True:
                    confirm = input("Are you sure you want to exit Adventure mode? [Y/N]: ").upper()
                    if confirm == "Y":
                        self.gamemode_battle(True)
                        break
                    elif confirm == "N":
                        break

    def gamemode_battle(self, start: bool = False, load: bool = False):
        print(f"---------=Scenario {self.scenario.name}=---------")
        if not load:
            self.generate_initiative()
        sd.sound_menu("battle")
        tm = gl.Turnmeter()
        if load:
            tm.setturn(self.scenario.turn)
            self.initiative_list = self.player_objects
            self.initiative_list.sort(key=lambda x: x.initiative, reverse=True)
        self.removed_players = []
        while True:
            self.removed_players.clear()
            print(f"---------=Scenario {self.scenario.name}, Turn {tm.currentturn}=---------")
            active_players = [player for player in self.player_objects if player.new_hp > 0]
            for index, player in enumerate(active_players):
                if load:
                    if index != self.scenario.playerturn:
                        continue
                    else:
                        load = False
                if player in self.removed_players:
                    continue
                if fs.is_attrib(player, "vassel"):
                    if player.vassel:
                        continue
                self.scenario.playerturn = index
                print(f"---------=[{player.prefix}] {player.firstname}'s Turn=---------")
                if not start:
                    self.status_update(player)
                    self.floor_update()
                start = False
                self.power_check(player)
                if player.status_effects:
                    print("---------=Currently Active Effects=---------")
                    for stat_eff in player.status_effects:
                        print(f"{stat_eff.name} [{stat_eff.time_left}]")
                while True:
                    print("-------------------------")
                    choice = input("[G]od action, [A]ction, [ADVENTURE], [N]ext\n").upper().strip()
                    if choice == "G":
                        self.god_action()
                    elif choice == "A":
                        self.action(player)
                    elif choice == "ADVENTURE":
                        while True:
                            choice = input("Are you sure you want to switch to Adventure Mode? [Y/N]: ").upper()
                            if choice == "Y":
                                self.gamemode_adventure()
                                break
                            elif choice == "N":
                                break
                        
                    elif choice == "N":
                        break
            tm.nextturn()
            self.scenario.turn = tm.currentturn

    def action(self, player: object):
        print("---------=Action Menu=---------")
        while True:
            choice = input("Cast [M]agic, [A]bility, [S]ummon, [C]ontrol Spirit, [CR]aft, [D]one: ").upper()
            if choice == "M":
                self.spell_action(player)
                break
            elif choice == "A":
                self.ability_action(player)
                break
            elif choice == "S":
                if not self.summons:
                    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} No summons are registered...")
                    continue
                print("---------=Summons=---------")
                for index, entity in enumerate(self.summons):
                    print(f"[{index+1}] {entity.firstname}")
                while True:
                    choice = fs.is_int(input("Summon entity with id: "))
                    if 1 <= choice <= len(self.summons):
                        time = fs.is_int(input("For how many turns: "))
                        self.summon(player, self.summons[choice-1], time)
                        break
                break
            elif choice == "C":
                self.spirit_control(player)
                break
            elif choice == "CR":
                self.craft_menu(player)
                break
            elif choice == "D":
                break
    
    def ability_action(self, player: object) -> None:
        while True:
            cast_ability = input("Cast Ability: ")
            if not fs.is_ability(cast_ability):
                continue
            else:
                ability: object = fs.is_ability(cast_ability)
                break
        if player.abilities:
            for i in player.abilities:
                if i.cooldown == 0:
                    continue
                if gl.uncapitalize_string(i.name, " ") == cast_ability:
                    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Spell is on cooldown for another {i.cooldown} turns...")
                    return
        if ability.surrounding_amount != 0:
            amount = fs.is_int(input("Surrounding amount: "))
            ability.surrounding_amount = amount
        player.abilities.append(ability)
        player.ability_apply(ability)
        print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} Player {player.prefix} {player.firstname} has recieved {ability.name} for {ability.time} turns.")

        if ability.cooldown != 0:
            player.cooldowns[cast_ability] = ability.cooldown
        
        sl.update_sheet(player)

    def spirit_control(self, player: object):
        for index, spirit in enumerate(player.spirits):
            print(f"[{index+1}] {spirit.firstname} Vassel: {spirit.vassel}")
        
        while True:
            choice = input("Spirit ID [B]ack: ").upper().strip()

            if choice == "B":
                return

            choice = fs.is_int(choice)
            if 1<=choice<=len(player.spirits):
                spirit: object = player.spirits[choice-1]
                reversion = "[R]evert" if spirit.vassel else "[C]ome"
                while True:
                    choice = input(f"{reversion}, [S]kill, [B]ack: ").upper().strip()
                    if choice == "B":
                        break
                    elif choice == "R" and spirit.vassel:
                        spirit.vassel = False
                        print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} {spirit.surname} ({spirit.firstname}) Has been reverted back into their natural form.")
                        if not spirit.equip_slot:
                            break
                        for attrib in spirit.equip_slot:
                            slot = f"equipment_{attrib}"
                            setattr(player, slot, None)
                        sl.update_sheet(player)
                        break
                    elif choice == "C" and not spirit.vassel:
                        spirit.vassel = True
                        print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} {spirit.surname} ({spirit.firstname}) Has been called forward.")
                        if not spirit.equip_slot:
                            break
                        for attrib in spirit.equip_slot:
                            slot = f"equipment_{attrib}"
                            player_slot = getattr(player, slot)
                            if player_slot is not None:
                                name, level = player_slot
                                player.inventory_add((name, level), 1)
                            setattr(player, slot, spirit.firstname)
                        sl.update_sheet(player)
                        break
                    elif choice == "S":
                        self.spell_action(spirit)
                        break
            if choice == "B":
                continue
            else:
                break

    def summon(self, player: object, entity: object, time: int):
        while True:
            prefix = input(f"Assign prefix for {entity.firstname}: ").upper()
            if any(prefix in lst for lst in [self.player_prefixes, self.obstacle_prefixes, self.floor_prefixes]):
                print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} The prefix {prefix} is already in use...")
            else:
                entity.prefix = prefix
                break
        print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} Summoning {entity.firstname} [{time}] for {player.prefix} {player.firstname}")
        player.summons.append((entity, time))
        self.player_objects.append(entity)
        self.player_prefixes[entity.prefix] = entity
        self.add_stats([entity])
        if self.scenario.mode == "battle":
            self.generate_initiative()

    def spell_action(self, player: object, cast_spell: str = None):
        if cast_spell is None:
            while True:
                cast_spell = input("Cast spell: ").lower().strip()
                if fs.is_spell(cast_spell):
                    cooldown = fs.is_cooldown(player, cast_spell)
                    if not cooldown:
                        break
                    else:
                        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Spell is on cooldown for [{cooldown}] more turns")
                        return
                else:
                    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Spell not found, Try again...")
        spell: object = sp.spell_list(cast_spell)

        #  NOTE
        if spell.note is not None:
            gl.print_debugg("NOTE", spell.note)

        #  ENCHANTMENT
        if self.hit_player < 0:
            spell_enchantments = []
            while True:
                enchantment = input("Add Enchantments: [M]aximize, [E]xtend, [P]enetrate, [O]ver, [B]oosted, [D]elay, [S]ilent, [TWIN], [TRIPLET], [CON]centrated, [W]iden [C]ontinue: ").upper().strip()
                if enchantment == "C":
                    break
                spell_enchantments.append(enchantment)
                print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} Added {enchantment}")
            
            self.spell_enchantments = spell_enchantments

        #  SPELL ENCHANTMENTS
        extend = 1.5 if "E" in self.spell_enchantments else 0
        self.extend = extend
        maximize = 1.25 if "M" in self.spell_enchantments else 1
        boost = 2 if "B" in self.spell_enchantments else 0
        delay = 1.25 if "D" in self.spell_enchantments else 0
        over = 3 if "O" in self.spell_enchantments else 0
        penetrate = 0.66 if "P" in self.spell_enchantments else 0
        silent = 1.25 if "S" in self.spell_enchantments else 0
        twin = 3 if "TWIN" in self.spell_enchantments else 0
        triplet = 5 if "TRIPLET" in self.spell_enchantments else 0
        widen = 1.5 if "W" in self.spell_enchantments else 0
        concentrate = 2 if "CON" in self.spell_enchantments else 0
        pierce = 0.75 if spell.enchant == "pierce" else 1
        affinity = 1.25 if any(attr in player.attribute for attr in spell.attribute) else 0.75

        #  MP AND SP COST
        if self.hit_player < 0:
            if spell.use_mp:
                mp_cost = math.ceil(spell.tier*((1.5 if maximize == 1.25 else 1)+over+boost+silent+concentrate+widen+twin+triplet+delay))
                if mp_cost > player.new_mp:
                    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} MP Cost will exceed available MP")
                    spell_enchantments.clear()
                    return
            else:
                mp_cost = 0
            if spell.use_sp:
                sp_cost = math.ceil(spell.tier*((1.5 if maximize == 1.25 else 1)+over+boost+silent+concentrate+widen+twin+triplet+delay))
                self.sp_cost = sp_cost
                if sp_cost > player.new_sp:
                    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} SP Cost will exceed available SP")
                    spell_enchantments.clear()
                    return
            else:
                sp_cost = 0
            self.sp_cost = sp_cost
            self.mp_cost = mp_cost
            
        loop = 1
        if "TWIN" in self.spell_enchantments:
            loop = 2
        elif "TRIPLET" in self.spell_enchantments:
            loop = 3

        for lop in range(1, loop+1):
            #  OPPONENT SELECTION
            opponent_list = []
            if spell.type == "self_buff":
                opponent_list.append = player.prefix
            else:
                if spell.type != "Obstacle":
                    while True:
                        opponent = input("Opponent Prefix ID ([D]one): ").upper()
                        if opponent == "D":
                            break
                        if opponent in self.player_prefixes or opponent in self.obstacle_prefixes:
                            if opponent in self.player_prefixes:
                                opponent: object = self.player_prefixes[opponent]
                            else:
                                opponent: object = self.obstacle_prefixes[opponent]
                            opponent_list.append(opponent)
                            print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} {opponent.prefix} {opponent.firstname} added to opponent_list")

            #  ATTACK AND SAVE ROLL
            if self.hit_player < 0 and lop == 1:
                dice = fs.is_int(input(f"Dice Roll (D{fs.spell_dice(spell.tier)}): "))
            else:
                dice = self.new_dice

            if opponent_list and spell.type != "Obstacle":
                while True:
                    add_targets: list[object] = []
                    remove_targets: list[object] = []
                    new_targets = None
                    for opp in opponent_list:
                        if getattr(opp, "character_type") != "Barrier" and spell.type != "Barrier":
                            if opp.save != 1:  # Skip opponents who's save has already been set
                                continue
                            save = input(f"Save throw for opponent {opp.prefix} {opp.firstname}. [S]pell: ").upper().strip()
                            if save == "S":
                                self.spell_action(opp)
                                opp.save = 1
                                new_targets, remove_target = self.save_spell(opp)
                                add_targets.extend(new_targets)
                                if remove_target is not None:
                                    remove_targets.append(remove_target)
                            else:
                                opp.save = fs.is_int(save)
                        else:
                            opp.save = 1
                    opponent_list.extend(add_targets) # Add the new targets
                    for removal in remove_targets:
                        opponent_list.remove(removal)
                    if new_targets is None:
                        break # Stop asking for saves if there are no new targets


            #  STATUS EFFECT ROLL
            if not spell.statuses is None:
                for effect in spell.statuses:
                    if effect.success != 1:
                        status_dice = fs.is_int(input(f"Status roll for {effect.name} (D20): "))
                        if (status_dice/20)>=(1-effect.success):
                            effect.is_active = True
                    else:
                        effect.is_active = True

            if spell.type == "Obstacle":
                for obs in spell.obstacles:
                    effect = self.calc_effect(dice, spell, 1, 0, 0, player.new_magatk, affinity, maximize, 1, 0)
                    self.add_obstacle(obs, effect)

            #  DAMAGE DEALING
            for oppon in opponent_list:  #  Saving throw is either reduction or nullification
                if spell.multiplier == "phyatk":
                    caster_multiplier = player.new_phyatk
                    opponent_multiplier = oppon.new_phydef
                    barrier_multiplier = "phydef"
                elif spell.multiplier == "magatk":
                    caster_multiplier = player.new_magatk
                    opponent_multiplier = oppon.new_magdef
                    barrier_multiplier = "magdef"
                elif spell.type == "Debuff":
                    caster_multiplier = player.new_magatk
                    opponent_multiplier = oppon.new_resistance
                    barrier_multiplier = "magdef"
                else:
                    caster_multiplier = player.new_magatk
                    opponent_multiplier = oppon.new_magdef
                    barrier_multiplier = "magdef"

                save_reduction = (((int(dice) * 3) - int(oppon.save)) / (int(dice) * 3)) if (((int(dice) * 2) - int(oppon.save))) > 0 else 0

                #  CHECK FOR UNIQUE SPELL (CASTER)
                if spell.unique:
                    unique = spell.init(player, oppon, save_reduction, caster_multiplier, opponent_multiplier, barrier_multiplier, dice, self.player_prefixes, self, self.spell_enchantments)
                else:
                    unique: str = "damage"

                #  CHECK FOR UNIQUE EFFECT (OPPONENT)
                spell_dmg_multi: float = 1
                if oppon.status_effects:
                    new_oppon = None
                    for s_effect in oppon.status_effects:
                        spell_dmg_multi += s_effect.effect_multiplier
                        if "attacked" in s_effect.activate_unique:
                            unique = s_effect.attacked(player, oppon, self)  # -> "damage" or "spell"
                            if not fs.is_type(unique, str):
                                new_oppon: object = unique
                                unique: str = "damage"
                    if new_oppon is not None:
                        oppon = new_oppon
                if unique == "damage":
    
                    #  BARRIER DAMAGE
                    extra_dmg = 0
                    remove_bar = []
                    if spell.type not in ["Barrier", "Buff", "Debuff"]:
                        if oppon.barriers and spell.effect <= 0:
                            for barrier in oppon.barriers:
                                bar_effect = (int(dice)/int(fs.spell_dice(spell.tier))) * int(spell.effect) * \
                                (1-(0.01*((getattr(barrier, barrier_multiplier)*penetrate*pierce) - caster_multiplier))) * affinity * maximize + extra_dmg
                                if barrier.new_hp >= -bar_effect:
                                    barrier.new_hp += bar_effect
                                    print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} Dealt {round(bar_effect)} damage to Barrier {barrier.name} ({barrier.new_hp}/{barrier.hp} HP)")
                                    take_damage: bool = False
                                    break
                                else:
                                    extra_dmg = barrier.new_hp + bar_effect
                                    print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} Barrier {barrier.name} Broke!")
                                    remove_bar.append(barrier)
                                    take_damage: bool = True
                            if remove_bar:
                                for barrier in remove_bar:
                                    oppon.barriers.remove(barrier)
                                remove_bar.clear()
                        else:
                            take_damage = True
                    else:
                        take_damage = False

                    #  DAMAGE APPLY
                    if take_damage:
                        if spell.type not in ["Buff", "Barrier"]:
                            effect = self.calc_effect(dice, spell, opponent_multiplier, penetrate, pierce, caster_multiplier, affinity, maximize, save_reduction, extra_dmg)
                            effect *= spell_dmg_multi
                            # Check for damage immunities
                            immune: bool = False
                            if oppon.status_effects:
                                for s_effect in oppon.status_effects:
                                    # Check for attribute
                                    for immunity in s_effect.immunities:
                                        for attribute in spell.attribute:
                                            if immunity == attribute.lower():
                                                immune: bool = True
                                        if immunity == "damage":
                                            immune: bool = True
                            
                            if immune:
                                effect: int = 0

                            old_hp = oppon.new_hp
                            if oppon.character_type == "Barrier" and spell.destroy:
                                effect *= 1.5

                            if spell.name in ["Spirit Reversal"]:  # Effect is SET instead of ADDED/SUBTRACTED
                                oppon.new_hp = round(effect)
                            else:
                                # oppon.new_hp += round(effect)   #  Effect is DiceRoll/DiceTier * DefenceDiff * Affinities * Enchantments * Save Throw
                                oppon.attribute_add("hp", round(effect), False, spell)

                            if oppon.new_hp <= 0 and oppon.character_type == "Barrier":
                                del self.obstacle_prefixes[oppon.prefix]
                                print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} Obstacle {oppon.prefix} {oppon.firstname} has been destroyed.")
                                while True:
                                    hit_player = input("Hit player(s)? Y/N: ").upper()
                                    if hit_player == "Y":
                                        if self.hit_player == -1:
                                            self.hit_player += 2
                                        else:
                                            self.hit_player += 1
                                        new_effect = old_hp+effect
                                        self.new_dice = self.calc_dice(new_effect, extra_dmg, int(fs.spell_dice(spell.tier)), spell, opponent_multiplier, penetrate, pierce, caster_multiplier, affinity, maximize, save_reduction)
                                        break
                                    elif hit_player == "N":
                                        self.hit_player = -1
                                        break
                                    else:
                                        continue
                            elif oppon.character_type == "Barrier":
                                print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} Obstacle {oppon.prefix} {oppon.firstname} Took damage equal to {effect}, and now has {oppon.new_hp}/{oppon.max_hp} HP")
                            elif lop == 1:
                                self.new_dice = dice
                        else:
                            effect = (int(dice)/int(fs.spell_dice(spell.tier))) * int(spell.effect) * \
                            (1+(0.01*caster_multiplier)) * affinity * maximize * save_reduction
                    
                    else:
                        if spell.type in ["Buff"]:
                            effect = round((int(dice)/int(fs.spell_dice(spell.tier))) * int(spell.effect) * \
                            (1+(0.01*caster_multiplier)) * affinity * maximize * save_reduction)
                        if spell.type in ["Debuff"]:
                            effect = self.calc_effect(dice, spell, opponent_multiplier, penetrate, pierce, caster_multiplier, affinity, maximize, save_reduction, 0)

                        # INTERUPTIONS
                    if player.status_effects:
                        for status in player.status_effects:
                            if status.interupt:
                                if "attack" not in status.interupt:
                                    continue
                                status.remove(player)
                                player.status_effects.remove(status)
                                print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} {player.prefix} {player.firstname} attacked and has thus removed the status effect {status.name}")
                    if oppon.status_effects:
                        for status in oppon.status_effects:
                            if status.interupt:
                                if "attacked" not in status.interupt:
                                    continue
                                status.remove(oppon)
                                oppon.status_effects.remove(status)
                                print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} {oppon.prefix} {oppon.firstname} was attacked and has thus removed the status effect {status.name}")

                    #  STATUS EFFECTS
                    if oppon.new_hp > 0 and oppon.character_type != "Barrier":
                        print("-------------------------")
                        self.status_effect(spell, oppon, save_reduction, effect)
                        if spell.type not in ["Buff", "Barrier", "Debuff"]:
                            print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} Dealt {round(effect)} damage/heal to Player {oppon.prefix} {oppon.firstname}")
                        print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} {oppon.prefix} {oppon.firstname} now has {oppon.new_hp}/{oppon.max_hp} HP")
                        #if oppon.prefix != player.prefix:
                            #sl.update_sheet(oppon)

                        #  BARRIER APPLY
                        if spell.type == "Barrier":
                            spell.barrier(effect, oppon)
                            oppon.barriers.append(spell)
                            print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} Gave a Barrier with {round(effect)} HP to Player {oppon.prefix} {oppon.firstname}")
                        
                        #  UPDATE SPIRITS FOR OPPONENT
                        for o_spirits in oppon.spirits:
                            for spirits in self.spirits:
                                if o_spirits == spirits.id:
                                    sl.update_spirit(spirits)
                    
                    # SECOND UNIQUE CHECK
                    if oppon.status_effects:
                        for status in oppon.status_effects:
                            if "attacked_after" not in status.activate_unique:
                                continue
                            status.attacked_after(oppon)
                    
            #  FLOOR APPLY
            if spell.floor is not None:
                for flo in spell.floor:
                    floor: object = fe.floor_list(flo, effect, cast_spell, player.prefix)
                    while True:
                        prefix = input(f"Floor Effect [{floor.name}] Prefix ID: ").upper().strip()
                        if prefix in self.player_prefixes or prefix in self.obstacle_prefixes or prefix in self.floor_prefixes:
                            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Prefix is already registered.")
                            continue
                        else:
                            floor.prefix = prefix
                            self.floor_prefixes[prefix] = floor
                            break

            # Notes
            if spell.effect_is != "Effect":
                if spell.effect_is == "Range":
                    print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} Range of spell is {round(effect)}m")
                if spell.effect_is == "Save":
                    print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} Player should have {round(effect)} to all saving throws")
                    
        if self.hit_player > 0:
            self.hit_player -= 1
            self.spell_action(player, cast_spell)
        else:
            self.hit_player = -1

            if self.mp_cost == 0:
                player.new_mp -= mp_cost
            else:
                player.new_mp -= self.mp_cost
            if self.sp_cost == 0:
                player.new_sp -= sp_cost
            else:
                player.new_sp -= self.sp_cost
            player.new_sp -= self.sp_cost
            if spell.target == "AOE" and spell.karma != 0:
                for opponent in opponent_list:
                    if opponent.religion == player.religion:
                        player.new_karma -= spell.karma
                    else:
                        player.new_karma += spell.karma
            else:
                player.new_karma += spell.karma
            if spell.use_mp:
                print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} {player.prefix} {player.firstname} used {self.mp_cost} MP, and now has {player.new_mp}/{player.max_mp} MP")
            if spell.use_sp:
                print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} {player.prefix} {player.firstname} used {self.sp_cost} SP, and now has {player.new_sp}/{player.max_sp} SP")
            if spell.karma != 0:
                print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} {player.prefix} {player.firstname} used {spell.karma} Karma, and now has {player.new_karma} Karma")
            
            #  UPDATE SPIRITS FOR CASTER
            for p_spirits in player.spirits:
                for spirits in self.spirits:
                    if p_spirits == spirits.id:
                        sl.update_spirit(spirits)
            
            #  Apply Cooldowns
            if spell.cooldown != 0:
                player.cooldowns[cast_spell] = spell.cooldown

            for opponent in opponent_list:
                opponent.save = 1 # Reset all saves
                sl.update_sheet(opponent)
            opponent_list.clear()
            self.spell_enchantments.clear()
            self.power_check(player)
            sl.update_sheet(player)

            self.death_update()
            self.mp_cost = self.sp_cost = 0

    def add_obstacle(self, obstacle: str = None, effect: int = None):
        if obstacle is None:
            while True:
                obstacle = input("Add obstacle: ").lower()
                if not fs.is_obstacle(obstacle):
                    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Obstacle not found...")
                    continue
                break
        obstacle: object = ob.obstacle_list(obstacle)
        if effect is None:
            obstacle.effect = fs.is_int(input("Obstacle Effect: "))
        else:
            obstacle.effect = effect
        while True:
            prefix = input("Obstacle Prefix ID: ").upper().strip()
            if prefix in self.player_prefixes or prefix in self.obstacle_prefixes:
                print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Prefix is already registered.")
                continue
            else:
                obstacle.prefix = prefix
                self.obstacle_prefixes[prefix] = obstacle
                self.add_stats([obstacle])
                obstacle.barrier()
                print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} Obstacle {obstacle.firstname} has been created with Prefix {obstacle.prefix}")
                break

    def save_spell(self, player: object):
        targets: list[object] = []
        r_target: object = None
        while True:
            target = input("Inital spell targets: [S]ame, [D]ifferent, [N]one: ").upper().strip()
            if target == "S":
                targets.append(player)
                break
            elif target == "D":
                while True:
                    while True:
                        new_target = input("Target new player prefix ID [D]one: ").upper().strip()
                        if new_target == "D":
                            break
                        if not any(new_target in lst for lst in [self.player_prefixes, self.obstacle_prefixes]):
                            continue
                        break
                    if new_target == "D":
                        break
                    result: object = self.player_prefixes.get(new_target)
                    if result is None:
                        result = self.obstacle_prefixes.get(new_target)
                    if result is None:
                        gl.print_debugg("ERROR", f"Could not find any player, floor effect or obstacle with prefix id {new_target}")
                    else:
                        targets.append(result)
                break
            elif target == "N":
                break
        if player not in targets:
            r_target = player
        return targets, r_target

    def death_update(self):
        for play in self.player_objects:
            if play.new_hp <= 0:
                self.removed_players.append(play)
                print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} {play.prefix} {play.firstname} has been slain")

    def calc_effect(self, dice: int, spell: object, opponent_multiplier: int, penetrate: float, pierce: float, caster_multiplier: int, affinity: float, maximize: float, save_reduction: float, extra_dmg: int):
        effect = (int(dice)/int(fs.spell_dice(spell.tier))) * int(spell.effect) * \
                    (1-(0.01*((opponent_multiplier*penetrate*pierce) - caster_multiplier))) * affinity * maximize * save_reduction + extra_dmg
        #print(f"effect: {effect}")
        return round(effect)
    
    def calc_dice(self, effect: int, extra: int, tier: int, spell: object, oppo_multi:int, penetrate: float, pierce: float, cast_multi: int, affinity: float, maximize: float, save: float):
        dice = ((effect-extra)*tier)/(spell.effect*(1-(0.01*((oppo_multi*penetrate*pierce)-cast_multi)))*affinity*maximize*save)
        #print(f"Dice: {dice}, Effect: {effect}, Tier: {tier}")
        return dice

    def status_effect_apply(self, status_effect: object, opponent: object, save_reduction: float, effect: int, mode = "d", spell: object = None):
        #if not status_effect.is_active:
        #    return
        if save_reduction == 0:
            return
        if not status_effect.is_active:
            return
        if status_effect.ept and status_effect.is_effect and not status_effect.applied:
            status_effect.effect *= abs(round(effect))
        if self.extend == 1.5 and not status_effect.applied:
            status_effect.time *= self.extend
            status_effect.time = round(status_effect.time)
        if mode != "d":
            if spell.type in ["Debuff"]:
                print(f"Effect[{effect}] vs Resistance[{opponent.new_resistance*(1+(opponent.save-10)*0.01)}]")
                if effect < opponent.new_resistance*(1+(opponent.save-10)*0.01):
                    print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} {opponent.prefix} {opponent.firstname} resisted {status_effect.name}")
                    return
        opponent.status_apply(status_effect, effect)
        print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} {opponent.prefix} {opponent.firstname} has recieved {status_effect.name} for {status_effect.time} turns")
        status_effect.applied = True

    def status_effect(self, spell: object, opponent: object, save_reduction: float, effect: int):
        def check_immunity(opponent: object, sent_status_effect, save_reduction, effect, mode, spell):
            immune: bool = False
            for p_status in opponent.status_effects:
                if not p_status.immunities:
                    continue
                for p_immunity in p_status.immunities:
                    if gl.uncapitalize_string(sent_status_effect.name, " ") == p_immunity:  # Check from name OBS! only if the spell name = immunity
                        immune: bool = True
                    if p_immunity == "debuff" and sent_status_effect.effect_type == "debuff":
                        immune: bool = True
                    if p_immunity == "slow" and sent_status_effect.new_agility < 0 or sent_status_effect.new_acrobatics < 0:
                        immune: bool = True
            if immune:
                return
            
            # Check for debuffs if spell gives immunity
            if sent_status_effect.immunities:
                remove: list[object] = []
                for immunity in sent_status_effect.immunities:
                    for p_effect in opponent.status_effects:
                        if p_effect.effect_type != "debuff":
                            continue
                        if gl.uncapitalize_string(p_effect.name, " ") != immunity:
                            continue
                        remove.append(p_effect)
                        p_effect.remove(opponent)
                if remove:
                    for effect in remove:
                        opponent.status_effects.remove(effect)

            # Update effect_mulitpier
            if sent_status_effect.is_effect:
                sent_status_effect.effect_multiplier *= effect
                print(f"Multiplier set to: {sent_status_effect.effect_multiplier}")

            self.status_effect_apply(sent_status_effect, opponent, save_reduction, effect, mode, spell)
        
        if hasattr(spell, "immunities"):
            gl.print_debugg("DEBUGG", "Status Effect Detected")
            check_immunity(opponent, spell, 1, effect, "d", None)
        else:
            if spell.statuses is None:
                return
            for status_effect in spell.statuses:
                check_immunity(opponent, status_effect, save_reduction, effect, "stat", spell)
                
    def god_action(self):
        choice = input("[D]amage/Heal, [P]layer, [B]ackpack, [E]ffect, [A]bilities, [I]nfo, [O]bstacle, [F]loor, [M]usic, [S]ave, [Q]uit, [C]ontinue\n").upper().strip()
        if choice == "D":
            while True:
                character = input("Character Prefix ID: ").upper()
                if character in self.player_prefixes:
                    character = self.player_prefixes[character]
                    for player in self.player_objects:
                        if not fs.is_attrib(player, "prefix"):
                            continue
                        if player.prefix == character.prefix:
                            while True:
                                dmg_type = input("Affect skill/stat type: ").lower()
                                if dmg_type in gl.SKILLS or dmg_type in gl.STATS:
                                    damage = fs.is_int(input("Deal debuff(-)/buff(+) equal to: "))
                                    dmg_type = f"new_{dmg_type}"
                                    old_val = getattr(player, dmg_type)
                                    new_damage = old_val+damage
                                    setattr(player, dmg_type, new_damage)
                                    new_dmg_type = dmg_type.removeprefix("new_")
                                    print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} {player.firstname} took damage equal to {damage} and now has {getattr(player, dmg_type)} {new_dmg_type.upper()}")
                                    sl.update_sheet(player)
                                    self.death_update()
                                    break
                            break
                    break
                else:
                    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} No player found")
        elif choice == "O":
            print("---------=Obstacles Menu=---------")
            while True:
                choice = input("[A]dd, [R]emove, [L]ist, [B]ack: ").upper()
                if choice == "A":
                    self.add_obstacle()
                    break
                elif choice == "R":
                    if not self.obstacle_prefixes:
                        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Obstacle not found...")
                        return
                    for index, (key, obstacle) in enumerate(self.obstacle_prefixes.items()):
                        print(f"[{obstacle.prefix}] {obstacle.name} {obstacle.hp}/{obstacle.max_hp} HP")
                    while True:
                        choice = input("Remove obstacle with prefix index: ").upper().strip()
                        if choice not in self.obstacle_prefixes:
                            continue
                        del self.obstacle_prefixes[choice]
                        break
                    break
                elif choice == "L":
                    print("---------=Obstacles=---------")
                    for index, (key, obstacle) in enumerate(self.obstacle_prefixes.items()):
                        print(f"[{index+1}] {key} {obstacle.firstname}, HP:{obstacle.new_hp}, PHY.DEF:{obstacle.new_phydef}, MAG.DEF:{obstacle.magdef}")
                elif choice == "B":
                    break
        elif choice == "P":
            assigned, objects, prefixes = gl.player_assign(self.player_objects)
            gl.team_assign(objects)

            for i in objects:
                if i.prefix not in self.player_prefixes:
                    print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} ADDING STATS FOR {i.firstname}")
                    self.add_stats([i])

            self.assigned_players = assigned
            self.player_objects = objects
            self.player_prefixes = prefixes

            if self.scenario.mode == "battle":
                self.generate_initiative()
        elif choice == "M":
            sd.sound_menu()
        elif choice =="E":
            character = input("Character Prefix ID: ").upper()
            if character in self.player_prefixes:
                character: object = self.player_prefixes[character]
                for player in self.player_objects:
                    if player.prefix == character.prefix:
                        choice = input("[A]dd, [E]dit, [R]emove: ").upper()
                        if choice == "E":
                            if not player.status_effects:
                                print("No Status Effects applied")
                                return
                            for index, status in enumerate(player.status_effects):
                                print(f"[{index+1}] {status.name} [{status.time_left}]")
                            
                            choice = fs.is_int(input("Edit id: "))
                            if 1 <= choice <= len(player.status_effects):
                                status_effect = player.status_effects[choice-1]
                                status_effect.edit(player)
                                self.status_update(player)
                            else:
                                print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Choice out of bounce")
                        elif choice == "R":
                            if not player.status_effects:
                                print(f"{Fore.RED}ERROR]{Style.RESET_ALL} No Status Effects applied")
                                return
                            for index, effect in enumerate(player.status_effects):
                                print(f"[{index+1}] {effect.name} [Time left: {effect.time_left}]")
                            remove = fs.is_int(input("Remove effect with index: "))
                            if 1 <= remove <= len(player.status_effects):
                                status_effect = player.status_effects[remove-1]
                                status_effect.remove(player)
                                del player.status_effects[remove-1]
                        elif choice == "A":
                            effect: str = input("Apply status effect: ").lower()
                            time = input("Time: ")
                            extend = input("Is Extended? [Y/N]: ").upper()
                            extend = 1.5 if extend == "Y" else 1
                            use_effect = input("Use Effect [Y/N]: ").upper()
                            use_effect = True if use_effect == "Y" else False
                            spell_effect = 0
                            if use_effect:
                                spell_effect = fs.is_int(input("Spell Effect: "))
                            status_effect: object = ef.effect_list(effect, time, 1, use_effect)
                            self.status_effect(status_effect, player, 1, spell_effect)
                            
                            sl.update_sheet(player)
        elif choice == "A":
            character = input("Character Prefix ID: ").upper()
            if character in self.player_prefixes:
                character = self.player_prefixes[character]
                for player in self.player_objects:
                    if player.prefix == character.prefix:
                        if not player.abilities:
                            return
                        choice = input("[E]dit, [R]emove: ").upper()
                        if choice == "E":
                            for index, ability in enumerate(player.abilities):
                                print(f"[{index+1}] {ability.name} [Time left: {ability.time}]")

                            choice = fs.is_int(input("Edit id: "))
                            if 1 <= choice <= len(player.abilities):
                                ability = player.abilities[choice-1]
                                ability.edit(player)
                            else:
                                print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Choice out of bounce")
                        elif choice == "R":
                            for index, ability in enumerate(player.abilities):
                                print(f"[{index+1}] {ability.name} [Time left: {ability.time}]")

                            choice = fs.is_int(input("Remove id: "))
                            if 1 <= choice <= len(player.abilities):
                                ability = player.abilities[choice-1]
                                player.ability_remove(ability)
                                player.abilities.remove(ability)
                            else:
                                print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Choice out of bounce")
                        sl.update_sheet(player)
        elif choice == "B":
            while True:
                choice = input("[P]layer, [C]hest: ").upper().strip()
                if choice == "P":
                    self.player_equipment()
                elif choice == "C":
                    self.scenario.chest_menu()
                if choice in ["P", "C"]:
                    break
        elif choice == "S":
            while True:
                mode = input("[C]haracter, [S]cenario: ").upper()
                if mode == "C":
                    character = input("Save character with Prefix ID: ").upper()
                    if character == "SA":
                        sl.save_all("character_saves", self.player_objects)
                    else:
                        if character in self.player_prefixes:
                            character = self.player_prefixes[character]
                            sl.save_character("character_saves", character)
                    break
                elif mode == "S":
                    sl.save_all("character_saves", self.player_objects)  # SAVE ALL CHARACTERS
                    self.scenario.players = self.player_objects
                    self.scenario.obstacles = self.obstacle_prefixes
                    sl.save_scenario(self.scenario)
                    break
        elif choice == "I":
            character = input("Character Prefix ID: ").upper()
            if character in self.player_prefixes:
                character = self.player_prefixes[character]
                for player in self.player_objects:
                    summons = [(obj.firstname, turns) for obj, turns in player.summons]
                    if player.prefix == character.prefix:
                        print(f"---------={player.firstname} {player.surname}=---------")
                        print(f"Board Piece: {player.prefix}")
                        print(f"Team: {player.team}")
                        print(f"Power level: {player.new_power_level}/{player.power_level}")
                        print(f"Karma: {player.new_karma}/{player.karma}")
                        print(f"Religion: {player.religion}")
                        print(f"Armor Class: {player.armor_class}")
                        print(f"Race Type: {player.race_type}")
                        spirits = []
                        for spirit in player.spirits:
                            spirits.append([spirit.firstname, spirit.vassel])
                        print(f"Spirits: {spirits}")
                        print(f"Summons: {summons}")
                        print("---------=Effects=---------")
                        for current_effect in player.status_effects:
                            print(f"{current_effect.name} [{current_effect.time_left}]")
                        for ability in player.abilities:
                            print(f"{ability.name} [{ability.time}]")
                        print("---------=Cooldowns=---------")
                        for spell, cooldown in player.cooldowns.items():
                            print(f"{spell} [{cooldown}]")
                        print("---------=Stats=---------")
                        print(f"HP:{player.new_hp}/{player.max_hp}, MP:{player.new_mp}/{player.max_mp}, SP:{player.new_sp}/{player.max_sp}\n"
                              f"Agility:{player.new_agility}/{player.max_agility}, Finess:{player.new_finess}/{player.max_finess}\n"
                              f"PHY.ATK:{player.new_phyatk}/{player.max_phyatk}, PHY.DEF:{player.new_phydef}/{player.max_phydef}\n"
                              f"MAG.ATK:{player.new_magatk}/{player.max_magatk}, MAG.DEF:{player.new_magdef}/{player.max_magdef}\n"
                              f"Resistance:{player.new_resistance}/{player.max_resistance}, Special:{player.new_special}/{player.max_special}")
                        print("---------=Skills=---------")
                        print(f"ATH:{player.new_athletics}/{player.max_athletics}, ACRO:{player.new_acrobatics}/{player.max_acrobatics}\n"
                              f"STE:{player.new_stealth}/{player.max_stealth}, SOH:{player.new_sleight}/{player.max_sleight}\n"
                              f"INV:{player.new_investigation}/{player.max_investigation}, PER:{player.new_perception}/{player.max_perception}\n"
                              f"DEC:{player.new_deception}/{player.max_deception}, INTI:{player.new_intimidation}/{player.max_intimidation}\n"
                              f"PERS:{player.new_persuasion}/{player.max_persuasion}, PERF:{player.new_performance}/{player.max_performance}")
                        print(f"{player:equipment}")
        elif choice == "Q":
            while True:
                choice = input("Would you like to save a character? [Y/N]: ").upper()
                if choice == "Y":
                    character = input("Save character with Prefix ID: ").upper()
                    if character == "SA":
                        sl.save_all("character_saves", self.player_objects)
                    else:
                        if character in self.player_prefixes:
                            character = self.player_prefixes[character]
                            sl.save_character("character_saves", character)
                    break
                elif choice == "N":
                    break
            print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} Returning to Main Menu...")
            sd.sound_stop()
            sd.sound_play("menu_theme", 0.2, -1)
            menu.main_menu()
        elif choice == "F":
            print("---------=Floor Menu=---------")
            while True:
                choice = input("[A]dd, [R]emove, [T]rigger, [L]ist, [B]ack: ").upper()
                if choice == "A":
                    floor = input("Add floor effect: ").lower()
                    if not fs.is_floor(floor):
                        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Floor effect not found...")
                        continue
                    floor: object = fe.floor_list(floor)
                    floor.effect = fs.is_int(input("Floor Effect: "))
                    caster = input("Floor Caster: ").upper()
                    floor.caster = caster if caster != "" else "Ulkaraz"
                    spell = input("Floor Spell: ").lower()
                    floor.spell = spell if spell != "" else "God Action"
                    floor.time = fs.is_int(input("Floor Time: "))
                    while True:
                        prefix = input("Floor Effect Prefix ID: ").upper().strip()
                        if prefix in self.player_prefixes or prefix in self.obstacle_prefixes or prefix in self.floor_prefixes:
                            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Prefix is already registered.")
                            continue
                        else:
                            floor.prefix = prefix
                            self.floor_prefixes[prefix] = floor
                            print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} Floor effect {floor.name} has been created with Prefix {floor.prefix}")
                            break
                    break
                elif choice == "R":
                    if not self.floor_prefixes:
                        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Floor effect not found...")
                        return
                    for index, (key, floor) in enumerate(self.floor_prefixes.items()):
                        print(f"[{floor.prefix}] {floor.name} casted by {floor.caster}'s {floor.spell}")
                    while True:
                        choice = input("Remove floor effect with prefix index: ").upper().strip()
                        if choice not in self.floor_prefixes:
                            continue
                        del self.floor_prefixes[choice]
                        break
                    break
                elif choice == "L":
                    print("---------=Floor Effects=---------")
                    for index, (key, floor) in enumerate(self.floor_prefixes.items()):
                        print(f"[{key}] {floor.name}, casted by: {floor.caster}, spell: {floor.spell}")
                elif choice == "T":
                    if not self.floor_prefixes:
                        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Floor effects not found...")
                        continue
                    for index, (key, floor) in enumerate(self.floor_prefixes.items()):
                        print(f"[{index+1}] {key} {floor.name}, casted by: {floor.caster}, spell: {floor.spell}")
                    while True:
                        trigger = input("Trigger floor effect with prefix ID: ").upper().strip()
                        if trigger in self.floor_prefixes:
                            floor: object = self.floor_prefixes.get(trigger)
                            break
                    players = []
                    while True:
                        append = input("Append to player prefix ([D]one): ").upper().strip()
                        if append == "D":
                            break
                        if append in self.player_prefixes and append not in players:
                            players.append(append)
                    
                    if players:
                        for effect in floor.status_effects:
                            for p in players:
                                player: object = self.player_prefixes.get(p)
                                player.status_effects.append(effect)
                            print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} Added status effect to {player.prefix}")
                        
                elif choice == "B":
                    break
        elif choice == "C":
            return
    

    def generate_initiative(self):
        print("---------=Initiative=---------")
        while True:
            choice = input("[R]andom or [S]elect: ").upper()
            if choice == "R":
                for player in (p for p in self.player_objects if p.character_type != "spirit"):
                    if player in self.initiative_list:
                        continue
                    player.initiative = random.randint(1, 20)
                    self.initiative_list.append(player)
                break
            elif choice == "S":
                for player in (p for p in self.player_objects if p.character_type != "spirit"):
                    if player in self.initiative_list:
                        continue
                    player.initiative = fs.is_int(input(f"Initiative for {player.prefix} {player.firstname}: "))
                    self.initiative_list.append(player)
                break
        self.initiative_list.sort(key=lambda x: x.initiative, reverse=True)

    def craft_menu(self, player: object):
        while True:
            gl.print_menu("Craft Menu")
            choice = input("[C]raft, [S]earch, [D]one: ").upper()
            if choice == "C":
                while True:
                    item = input("Craft item: ").lower().strip()
                    if fs.is_item(item):
                        break
                amount = fs.is_int(input("Craft amount: ").strip())
                self.craft_craft(player, item, amount)
            elif choice == "S":
                while True:
                    search: str = input("Search recipe for item: ")
                    if it.item_list(search, 2) is not None:
                        break
                self.craft_search(search)
            elif choice == "D":
                break
    
    def craft_craft(self, player: object, craft_item: str, craft_amount: int):
        """
        Crafts X amount of an item if the player has the required ingredients on hand.
        """
        ingredients: list[tuple[str, int]] = it.item_list(craft_item, 2).ingredients
        missing: list[tuple[str, int, int]] = [] # name, has_amount, req_amount
        available: list[tuple[str, int]] = [] # name, amount

        # Check if player has ingredients
        for ingredient in ingredients:
            ing_name, ing_amount = ingredient
            if not player.inventory:
                missing.append((ing_name, 0, ing_amount*craft_amount))
            for item in player.inventory:
                item_name, item_amount = item
                if fs.is_type(item_name, tuple):
                    continue
                if item_name != ing_name:
                    continue
                if ing_amount*craft_amount > item_amount:
                    missing.append((ing_name, ing_amount*craft_amount-item_amount, ing_amount*craft_amount))
                else:
                    available.append((ing_name, item_amount))
        
        # Check if player has all required ingredients
        if missing:
            for miss in missing:
                gl.print_debugg("ERROR", f"{player.firstname} is missing {gl.capitalize_string(miss[0], '_')}. Has {miss[1]}/{miss[2]}")
            return
        
        # Check if player has all equipment
        has_equipment: bool = True
        for equip in it.item_list(craft_item, 2).equipment:
            has_equip: bool = False
            for inv_item in player.inventory:
                if fs.is_type(inv_item[0], tuple):
                    continue
                if inv_item[0] == equip[0] and inv_item[1] >= equip[1]:
                    has_equip = True
            if not has_equip:
                has_equipment = False
                gl.print_debugg("ERROR", f"{player.firstname} is missing {equip[1]} {gl.capitalize_string(equip[0], '_')}.")
        if not has_equipment:
            return

        # Determine level
        alchemy: int = 0  # Alchemy Score
        for job in player.job_classes:
            if job[0] in ["alchemist", "greater_alchemist"]:
                alchemy += job[1]
        add_level: int = min(5, 1 + alchemy // 10)

        # Add crafted item
        player.inventory_add((craft_item, add_level), craft_amount)

        # Remove ingredients
        for ing in ingredients:
            ing_name, ing_amount = ing
            player.inventory_remove(ing_name, ing_amount*craft_amount)
        
        gl.print_debugg("NOTE", f"{craft_amount} {craft_item} crafted!")
        sl.update_sheet(player)

    def craft_search(self, item: str):
        """
        Displays the reciepe for a craftable item
        """
        item_obj: object = it.item_list(item, 2)
        if not item_obj:
            gl.print_debugg("ERROR", f"Item '{item}' has no recipe.")
            return
        gl.print_menu(gl.capitalize_string(f"Recipe for {item}", "_"))
        for ing in item_obj.ingredients:
            print(f"{ing[1]} {ing[0]}")

class Scenario():
    def __init__(self, name: str, turn: int = 1, players: list[object] = None, playerturn: int = 0, mode = "Adventure", obstacles: dict = None, floor: dict = None, chests: dict[str, list[list[str, int, int]]] = None):
        self.name = name
        self.turn = turn
        self.playerturn = playerturn
        self.mode = mode
        self.players = players if players is not None else []
        self.obstacles = obstacles if obstacles is not None else {}
        self.floor = floor if floor is not None else {}
        self.chests = chests if chests is not None else {}
        self.player_prefixes = {}
        self.update_dict()

    def update_players(self, players):
        self.players.clear()
        self.players = players
        self.update_dict()
    
    def update_dict(self):
        if not self.players:
            return
        for player in self.players:
            self.player_prefixes[player.prefix] = player

    def chest_create(self):
        """
        Creates a container with the option to add items to it.
        """
        gl.print_menu("Add Chest")
        
        # Check if bag exists
        while True:
            name = input("Bag name, [Q]uit: ").lower().strip()
            if name == "q":
                return
            if name not in self.chests:
                break
            else:
                gl.print_debugg("ERROR", f"{name} is already registered as a bag.")
        gl.print_debugg("DEBUGG", "Creaing bag...")
        self.chests[name] = []

        gl.print_menu(name)
        gl.print_menu("Add Items")
        while True:
            while True:
                item_name = input("Add item with name, [D]one: ").lower().strip()
                if item_name == "d":
                    break
                if not fs.is_item(item_name):
                    continue
                break
            if item_name == "d":
                break
            item_level = fs.is_int(input("Item level: "))
            item_amount = fs.is_int(input("Item Amount: "))
            self.chest_add(name, item_name, item_level, item_amount)
            self.chest_disp(name)
            
    def chest_add(self, bag: str, item_name: str, item_level: int, item_amount: int):
        """Will add an item to a chest. If the item is already in the bag, it will change the amount accordingly."""
        chest: list[list] = self.chests.get(bag, [])
        if chest:
            have_item = False
            have_index = -1
            for index, c_item in enumerate(chest):
                c_name, c_level, c_amount = c_item
                if c_name == item_name and c_level == item_level:
                    have_item = True
                    have_index = index
            if have_item:
                chest[have_index][2] = c_amount+item_amount
            else:
                chest.append([item_name, item_level, item_amount])
        else:
            chest.append([item_name, item_level, item_amount])
        self.chests[bag] = chest
        gl.print_debugg("DEBUGG", f"{item_amount} {item_name} added to {bag}")

    def chest_remove(self, bag: str, remove: str = None, amount: int = 0, level: int = 0, mode: str = "d"):
        """Will remove an item from a chest. If there are two items with the same name but different levels,
        the user will be asked which one to remove. Note that you can use the 'level' parameter if you want
        to skip the 'choose' which item part."""
        if mode == "d":
            found = False
            while not found:
                remove = input("Remove item: ").lower().strip()
                found = self.chest_search(bag, remove)
            amount: int = fs.is_int(input("Remove item amount: "))
            level = input("Remove level [Leave blank if none]: ")
            if level != "":
                level = fs.is_int(level)
            else:
                level = 0
        
        remove_item: list[int] = []  # List of index where item is found
        bag_iter: list = self.chests.get(bag)
        if bag_iter is None:
            gl.print_debugg("ERROR", f"'{bag}' could not be found in the chests.")
            return
        for index, item in enumerate(bag_iter):
            item_name, item_level, item_amount = item
            if item_name == remove:
                remove_item.append(index)
                gl.print_debugg("DEBUGG", "Found item...")
                if level != 0 and level == item_level:
                    break
        if len(remove_item) > 1:
            gl.print_menu("Remove Item")
            for index in remove_item:
                item_name, item_level, item_amount = bag_iter[index]
                print(f"[{index+1}] {item_name}, level: {item_level}, amount: {item_amount}")
            while True:
                choice = fs.is_int(input("Remove item with index: "))
                if 0 <= choice-1 < len(remove_item):
                    removed: int = remove_item[choice-1]
                    break
        else:
            removed: int = remove_item[0]
        item_name, item_level, item_amount = bag_iter[removed]
        if bag_iter[removed][2] > amount:
            bag_iter[removed][2] -= amount
            self.chests[bag][removed] = bag_iter[removed]
            gl.print_debugg("DEBUGG", f"{amount} {item_name} removed from {bag}")
        elif bag_iter[removed][2] == amount:
            gl.print_debugg("DEBUGG", f"Removed {item_name} from container {bag}")
            del self.chests[bag][removed]
        else:
            gl.print_debugg("ERROR", "Tried to remove more items than what exists in the chest...")

        if not self.chests[bag]:
            del self.chests[bag]
            gl.print_debugg("DEBUGG", f"Removed the container '{bag}' since it was empty.")

    def chest_search(self, chest: str, item_name: str) -> bool:
        """Will search a chest and return a bool if the item is found"""
        found = False
        for item in self.chests.get(chest):
            if item[0] == item_name:
                found = True
        if not found:
            return False
        else:
            return True

    def chest_edit(self, chest: str):
        """
        chest: str; key to the container to be edited

        Menu for editing items, capable of Adding, Removing and Editing items.
        """
        self.chest_disp(chest)
        while True:
            choice = input("[A]dd, [R]emove, [E]dit, [D]one: ").upper().strip()
            if choice == "A":
                while True:
                    item_name = input("Item name: ").lower().strip()
                    if not fs.is_item(item_name):
                        continue
                    break
                item_level = fs.is_int(input("Item level: "))
                item_amount = fs.is_int(input("Item amount: "))
                self.chest_add(chest, item_name, item_level, item_amount)
            elif choice == "R":
                self.chest_remove(chest)
            elif choice == "E":
                while True:
                    edit = fs.is_int(input("Edit item with index: "))
                    if 0 <= edit-1 < len(self.chests[chest]):
                        break
                while True:
                    mode = input("Mode: [L]evel, [A]mount: ").upper().strip()
                    if mode == "L":
                        mode = "level"
                        mode_int = 1
                        break
                    elif mode == "A":
                        mode = "amount"
                        mode_int = 2
                        break
                    else:
                        continue
                value = fs.is_int(input(f"Edit value from '{self.chests[chest][edit-1][mode_int]}' to: "))
                gl.print_debugg("DEBUGG", f"Edited {mode} for {chest} from {self.chests[chest][edit-1][mode_int]} to {value}")
                self.chest_change(chest, mode, value, edit-1)
            elif choice == "D":
                pass
            if choice in ["A", "R", "E", "D"]:
                break

    def chest_open(self, chest: str):
        """
        chest: str; key to the chest to be opened

        Opens a chest where items can be added and/or removed to players
        -> Choose which chest to open -> Menu to deposit/take items -> deposit/take to player (note: Remember custom amount if amount > 1)
        """
        container: list[list] = self.chests.get(chest)
        if container is None:
            gl.print_debugg("ERROR", f"'{container}' could not be found and therefore cannot be opened.")
            return
        self.chest_disp(chest)
        while True:
            choice = input("[T]ake, [D]eposit, [C]ontinue: ").upper().strip()
            if choice == "T":
                while True:
                    if not container:
                        break
                    while True:
                        self.chest_disp(chest)
                        take: int = input("Take item with index, [A]ll, [D]one: ").upper().strip()
                        if take in ["D", "A"]:
                            break
                        take = fs.is_int(take)
                        if 0 <= take-1 <= len(container):
                            break
                    if take == "D":
                        break
                    while True:
                        player_id: str = input("Give to player with Prefix ID: ").upper().strip()
                        if player_id in self.player_prefixes:
                            break
                    player: object = self.player_prefixes.get(player_id)
                    if take == "A":
                        for _ in range(len(container)):
                            self.chest_transfer(container, 1, chest, "take", player, True)
                    else:
                        self.chest_transfer(container, take, chest, "take", player)
            elif choice == "D":
                while True:
                    player_id: str = input("Deposit item from player with Prefix ID: ").upper().strip()
                    if player_id in self.player_prefixes:
                        break
                player: object = self.player_prefixes.get(player_id)
                while True:
                    if not player.inventory:
                        break
                    print(f"{player:inventory}")
                    while True:
                        deposit = input("Deposit item with index, [A]ll, [D]one: ").upper().strip()
                        if deposit in ["D", "A"]:
                            break
                        deposit = fs.is_int(deposit)
                        if 0 <= deposit-1 <= len(player.inventory):
                            break
                    if deposit == "D":
                        break
                    if deposit == "A":
                        inv_range: int = len(player.inventory)
                        for _ in range(inv_range):
                            self.chest_transfer(container, 1, chest, "deposit", player, True)
                    else:
                        self.chest_transfer(container, deposit, chest, "deposit", player)
            elif choice == "C":
                break

    def chest_transfer(self, container: list[list], item_index: int, chest: str, mode: str, player: object = None, all: bool = False):
        """
        Takes or deposits items from a container/chest
        """
        if mode == "take":
            amount: int = 1
            amount_bypass = True if container[item_index-1][2] == 1 else False
            amount_bypass = True if all else amount_bypass
            if not amount_bypass:
                while True:
                    amount = fs.is_int(input("Take amount: "))
                    if amount == container[item_index-1][2]:
                        amount_bypass: bool = True
                        break
                    elif amount < container[item_index-1][2]:
                        break
                    else:
                        continue
            if amount_bypass:
                item: list = container.pop(item_index-1)
                amount: int = item[2]
            else:
                item: list = container[item_index-1]
                container[item_index-1][2] -= amount
            self.chests[chest] = container
            
            update: bool = True if len(self.chests[chest]) <= 0 and all else False
            item_obj = it.item_list(item[0], item[1])
            is_equipment = True if item_obj.type == "equipment" else False
            if is_equipment:
                if amount > 1:
                    for i in range(amount):
                        player.equipment_add(item[0], item[1], 1, update)
                else:
                    player.equipment_add(item[0], item[1], amount, update)
            else:
                player.equipment_add(item[0], item[1], amount, update)
        elif mode == "deposit":
            item, amount = player.inventory[item_index-1] # Note that the item CAN be a string or a tuple
            if fs.is_type(item, tuple):
                item_name, item_level = item
            else:
                item_name = item
                item_level = 2
            if not all:
                if amount != 1:
                    while True:
                        item_amount = fs.is_int(input("Choose amount: "))
                        if amount <= item_amount:
                            break
                else:
                    item_amount = amount
            else:
                item_amount = amount
            self.chest_add(chest, item_name, item_level, item_amount)
            player.equipment_reset()
            player.inventory_remove(item_name, item_amount, item_level)
            if len(player.inventory) == 0:
                player.equipment_check()
            else:
                player.equipment_check(False)

            if not all:
                self.chest_disp(chest)

    def chest_disp(self, chest: str):
        """
        chest: str; the key to the chest which is to be displayed

        Displays the contents of one or more chests, with their index, name, level and amount.
        """
        if chest == "all":
            gl.print_menu("All Chests")
            for key in self.chests.keys():
                gl.print_menu(key)
                for index, item in enumerate(self.chests.get(key)):
                    print(f"[{index+1}] name: {item[0]}: level: {item[1]}, amount: {item[2]}")
        else:
            if chest not in self.chests:
                gl.print_debugg("ERROR", f"Cannot display '{chest}' as it could not be found...")
                return
            gl.print_menu(gl.capitalize_string(chest, "_"))
            for index, item in enumerate(self.chests.get(chest)):
                print(f"[{index+1}] Name: {item[0]}, Level: {item[1]}, Amount: {item[2]}")
    
    def chest_change(self, chest: str, mode: str, value: int, item: int):
        """
        chest: str; the key for the container
        mode: str; 'amount', 'level', the thing to be changed/edited
        value: int; the value to which it will be changed to
        item: int; the index of the item to be edited
        """
        bag: list[list] = self.chests.get(chest)
        if bag is None:
            gl.print_debugg("ERROR", f"'{bag}' container could not be found when trying to change a value.")
            return

        if mode == "amount":
            bag[item][2] = value
        elif mode == "level":
            bag[item][1] = value
        else:
            gl.print_debugg("ERROR", f"Mode '{mode}' has not been registered in the chest_change.")
            return
        self.chests[chest] = bag

    def chest_menu(self):
        """
        A menu from where you can choose to Create, Add, Remove, Edit, Open and Display containers.
        """
        while True:
            gl.print_menu("Chest Menu")
            choice = input("[C]reate, [A]dd, [R]emove, [E]dit, [O]pen, [D]isplay, [Q]uit: ").upper().strip()
            if choice == "C":
                self.chest_create()
            elif choice == "A":
                if not self.chests:
                    gl.print_debugg("ERROR", "No containers are registered.")
                    continue
                chest = fs.is_in_iterable("Add to container: ", self.chests)
                while True:
                    item = it.item_list(input("Add item: "), 2)
                    if item is not None:
                        break
                item_level = fs.is_int(input("Item level: "))
                amount = fs.is_int(input("Item amount: "))
                self.chest_add(chest, gl.uncapitalize_string(item.name, " "), item_level, amount)
            elif choice == "R":
                if not self.chests:
                    gl.print_debugg("ERROR", "No containers are registered.")
                    continue
                chest = fs.is_in_iterable("Remove from container: ", self.chests)
                self.chest_remove(chest)
            elif choice == "E":
                self.chest_disp("all")
                while True:
                    chest = input("Edit chest: ")
                    if chest in self.chests.keys():
                        break
                self.chest_edit(chest)
                self.chest_disp(chest)
            elif choice == "O":
                chest = fs.is_in_iterable("Open container with name: ", self.chests)
                self.chest_open(chest)
            elif choice == "D":
                bag = input("Display bag: ").lower()
                self.chest_disp(bag)
            if choice in ["C", "A", "R", "E", "O", "D"]:
                continue
            if choice == "Q":
                break