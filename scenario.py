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

init(autoreset=True)

class Game():
    def __init__(self, mode: str):
        if mode == "N":
            print("---------=New Scenario=---------")
            name = input("Name of Scenario: ").lower()
            self.scenario = Scenario(name)
            self.assigned_players, self.player_objects, self.player_prefixes = gl.player_assign()
            self.spirits: list[object] = sl.load_spirits(self.player_objects)
            self.obstacle_prefixes: dict[str, object] = {}
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
                    self.gamemode_battle(False)
                    break
                elif gamemode == "A":
                    self.gamemode_adventure()
                    break
        elif mode == "L":
            print("---------=Load Scenario=---------")
            save = sl.disp_files("scenario_saves", "scenario_", ".txt")
            self.assigned_players, self.player_objects, self.player_prefixes, sc = sl.load_scenario(save)
            self.scenario = Scenario(*sc)
            self.spirits: list[object] = sl.load_spirits(self.player_objects)
            self.obstacle_prefixes: dict[str, object] = {}
            for spirit in self.spirits:
                self.player_prefixes[spirit.prefix] = spirit
                self.player_objects.append(spirit)
                sl.update_spirit(spirit, "not start")
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
                    print(f" ID:{player.id}  {player.prefix} {player.firstname}", end="")
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
            player.new_power_level = player.power_level
            player.barriers = []  # list[object]
            sl.update_sheet(player)
            print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} Added: {player.firstname}")

    def status_update(self, player: object):
        self.summon_update(player)
        if player.status_effects:
            player_effects = player.status_effects[:]
            for effect in player_effects:
                if effect.ept:
                    print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} Player {player.prefix} {player.firstname} took {round(effect.effect)} damage from {effect.name}")
                    player.new_hp += round(effect.effect)
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
            set_player = input("Player Prefix ID: ").upper()
            if set_player in self.player_prefixes:
                while True:
                    player = self.player_prefixes[set_player]
                    player.print_eq()
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
                print(f"---------=[{player.prefix}] {player.firstname}'s Turn=---------")
                if not start:
                    self.status_update(player)
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
                            choice = input("Are you sure you want to switch to Adventure Mode? [Y/N]").upper()
                            if choice == "Y":
                                self.gamemode_adventure()
                                break
                            elif choice == "N":
                                break
                        
                    elif choice == "N":
                        break
            tm.nextturn()

    def action(self, player: object):
        print("---------=Action Menu=---------")
        while True:
            choice = input("Cast [M]agic, [A]bility, [S]ummon, [C]ontrol Spirit: ").upper()
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
            choice = fs.is_int(input("Spirit ID: "))
            if 1<=choice<=len(player.spirits):
                spirit: object = player.spirits[choice-1]
                reversion = "[R]evert" if spirit.vassel else "[C]ome"
                while True:
                    choice = input(f"{reversion}, [S]kill: ").upper()
                    if choice == "R" and spirit.vassel:
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
            break

    def summon(self, player: object, entity: object, time: int):
        while True:
            prefix = input(f"Assign prefix for {entity.firstname}: ").upper()
            if prefix in self.player_prefixes:
                print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} The prefix {prefix} is already in use...")
            else:
                entity.prefix = prefix
                break
        print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} Summoning {entity.firstname} [{time}] for {player.prefix} {player.firstname}")
        player.summons.append((entity, time))
        self.player_objects.append(entity)
        self.player_prefixes[entity.prefix] = entity
        self.add_stats([entity])
        self.generate_initiative()

    def spell_action(self, player: object, cast_spell: str = None):
        if cast_spell is None:
            while True:
                cast_spell = input("Cast spell: ")
                if fs.is_spell(cast_spell):
                    cooldown = fs.is_cooldown(player, cast_spell)
                    if not cooldown:
                        break
                    else:
                        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Spell is on cooldown for [{cooldown}] more turns")
                        return
                else:
                    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Spell not found, Try again...")
        spell = sp.spell_list(cast_spell)

        #  ENCHANTMENT
        spell_enchantments = []
        while True:
            enchantment = input("Add Enchantments: [M]aximize, [E]xtend, [P]enetrate, [O]ver, [B]oosted, [D]elay, [S]ilent, [TWIN], [TRIPLET], [CON]centrated, [W]iden [C]ontinue: ").upper().strip()
            if enchantment == "C":
                break
            spell_enchantments.append(enchantment)
            print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} Added {enchantment}")
        
        #  SPELL ENCHANTMENTS
        extend = 1.5 if "E" in spell_enchantments else 0
        self.extend = extend
        maximize = 1.25 if "M" in spell_enchantments else 1
        boost = 2 if "B" in spell_enchantments else 0
        delay = 1.25 if "D" in spell_enchantments else 0
        over = 3 if "O" in spell_enchantments else 0
        penetrate = 0.66 if "P" in spell_enchantments else 0
        silent = 1.25 if "S" in spell_enchantments else 0
        twin = 3 if "TWIN" in spell_enchantments else 0
        triplet = 5 if "TRIPLET" in spell_enchantments else 0
        widen = 1.5 if "W" in spell_enchantments else 0
        concentrate = 2 if "CON" in spell_enchantments else 0
        pierce = 0.75 if spell.enchant == "pierce" else 1
        affinity = 1.25 if spell.attribute in player.attribute else 0.75

        #  MP AND SP COST
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
            if sp_cost > player.new_sp:
                print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} SP Cost will exceed available SP")
                spell_enchantments.clear()
                return
        else:
            sp_cost = 0
            
        #  OPPONENT SELECTION
        if spell.type == "self_buff":
            opponent = player.prefix
        else:
            opponent_list = []
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
            dice = fs.is_int(input(f"Dice Roll (D{fs.spell_dice(spell.tier)}): "))
            for opp in opponent_list:
                if getattr(opp, "character_type") != "Barrier":
                    save = input(f"Save throw for opponent {opp.prefix} {opp.firstname}. [S]pell: ").upper()
                    if save == "S":
                        self.spell_action(opp)
                    else:
                        opp.save = fs.is_int(save)
                else:
                    opp.save = 1

            #  STATUS EFFECT ROLL
            if not spell.statuses is None:
                for effect in spell.statuses:
                    if effect.success != 1:
                        status_dice = fs.is_int(input(f"Status roll for {effect.name} (D20): "))
                        if (status_dice/20)>=(1-effect.success):
                            effect.is_active = True
                    else:
                        effect.is_active = True
            
            #  DAMAGE DEALING
            for oppon in opponent_list:  #  Saving throw is either reduction or nullification
                if spell.multiplier == "phyatk":
                    caster_multiplier = player.new_phyatk
                    opponent_multiplier = oppon.new_phydef
                    barrier_multiplier = "phydef"
                else:
                    caster_multiplier = player.new_magatk
                    opponent_multiplier = oppon.new_magdef
                    barrier_multiplier = "magdef"

                save_reduction = (((int(dice) * 3) - int(oppon.save)) / (int(dice) * 3)) if (((int(dice) * 2) - int(oppon.save))) > 0 else 0
                self.save_reduction = save_reduction

                #  BARRIER DAMAGE
                extra_dmg = 0
                remove_bar = []
                if spell.type != "Barrier" or spell.type != "Buff":
                    if oppon.barriers:
                        for barrier in oppon.barriers:
                            bar_effect = (int(dice)/int(fs.spell_dice(spell.tier))) * int(spell.effect) * \
                            (1-(0.01*((getattr(barrier, barrier_multiplier)*penetrate*pierce) - caster_multiplier))) * affinity * maximize + extra_dmg
                            if barrier.new_hp >= bar_effect:
                                barrier.new_hp -= bar_effect
                                take_damage: bool = False
                                break
                            else:
                                extra_dmg = barrier.new_hp - bar_effect
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
                    if spell.type != "Buff":
                        effect = (int(dice)/int(fs.spell_dice(spell.tier))) * int(spell.effect) * \
                        (1-(0.01*((opponent_multiplier*penetrate*pierce) - caster_multiplier))) * affinity * maximize * save_reduction + extra_dmg
                        oppon.new_hp += round(effect)   #  Effect is DiceRoll/DiceTier * DefenceDiff * Affinities * Enchantments * Save Throw
                        print(oppon.new_hp, oppon.character_type)
                        if oppon.new_hp <= 0 and oppon.character_type == "Barrier":
                            del self.obstacle_prefixes[oppon.prefix]
                            print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} Obstacle {oppon.prefix} {oppon.firstname} has been destroyed.")
                    else:
                        effect = (int(dice)/int(fs.spell_dice(spell.tier))) * int(spell.effect) * \
                        (1+(0.01*caster_multiplier)) * affinity * maximize * save_reduction
                    self.effect = effect
                
                    #  STATUS EFFECTS
                    print("-------------------------")
                    self.status_effect(spell, oppon)
                    if not spell.type == "Buff":
                        print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} Dealt {round(effect)} damage to Player {oppon.prefix} {oppon.firstname}")
                    print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} {oppon.prefix} {oppon.firstname} now has {oppon.new_hp}/{oppon.max_hp} HP")
                    if oppon.prefix != player.prefix:
                        sl.update_sheet(oppon)

                    #  BARRIER APPLY
                    if spell.type == "Barrier":
                        spell.barrier(effect, oppon)
                        oppon.barriers.append(spell)
                    
                    #  UPDATE SPIRITS FOR OPPONENT
                    for o_spirits in oppon.spirits:
                        for spirits in self.spirits:
                            if o_spirits == spirits.id:
                                sl.update_spirit(spirits)

            player.new_mp -= mp_cost
            player.new_sp -= sp_cost
            if spell.target == "AOE" and spell.karma != 0:
                for opponent in opponent_list:
                    if opponent.religion == player.religion:
                        player.new_karma -= spell.karma
                    else:
                        player.new_karma += spell.karma
            else:
                player.new_karma += spell.karma
            if spell.use_mp:
                print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} {player.prefix} {player.firstname} used {mp_cost} MP, and now has {player.new_mp}/{player.max_mp} MP")
            if spell.use_sp:
                print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} {player.prefix} {player.firstname} used {sp_cost} SP, and now has {player.new_sp}/{player.max_sp} SP")
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

            opponent_list.clear()
            spell_enchantments.clear()
            self.power_check(player)
            sl.update_sheet(player)

            self.death_update()
    
    def death_update(self):
        for play in self.player_objects:
            if play.new_hp <= 0:
                self.removed_players.append(play)
                print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} {play.prefix} {play.firstname} has been slain")

    def status_effect(self, spell, opponent):
        if not spell.statuses is None:
            for status_effect in spell.statuses:
                if not status_effect.is_active:
                    continue
                if self.save_reduction == 0:
                    continue
                if status_effect.ept:
                    status_effect.effect *= round(self.effect)
                if self.extend == 1.5:
                    status_effect.time *= self.extend
                    status_effect.time = round(status_effect.time)
                for current_effect in opponent.status_effects:
                    if current_effect.name == status_effect.name:
                        print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} Replacing Status Effect")
                        opponent.status_effects.remove(current_effect)
                opponent.status_apply(status_effect, self.effect)
                opponent.status_effects.append(status_effect)
                print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} {opponent.prefix} {opponent.firstname} has recieved {status_effect.name} for {status_effect.time} turns")

    def god_action(self):
        choice = input("[D]amage/Heal, [P]layer, [B]ackpack, [E]ffect, [A]bilities, [I]nfo, [O]bstacle, [M]usic, [S]ave, [Q]uit, [C]ontinue\n").upper().strip()
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
            while True:
                choice = input("[A]dd, [R]emove: ").upper()
                if choice == "A":
                    obstacle = input("Add obstacle: ").lower()
                    if not fs.is_obstacle(obstacle):
                        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Obstacle not found...")
                        continue
                    obstacle: object = ob.obstacle_list(obstacle)
                    obstacle.effect = fs.is_int(input("Obstacle Effect: "))
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
                    break
                elif choice == "R":
                    if not self.obstacle_prefixes:
                        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Obstacle not found...")
                        return
                    for index, obstacle in enumerate(self.obstacle_prefixes):
                        print(f"[{obstacle.prefix}] {obstacle.name} {obstacle.hp}/{obstacle.max_hp} HP")
                    while True:
                        choice = fs.is_int(input("Remove obstacle with index: "))
                        if choice not in self.obstacle_prefixes:
                            continue
                        del self.obstacle_prefixes[choice]
                        break
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

            self.generate_initiative()
        elif choice == "M":
            sd.sound_menu()
        elif choice =="E":
            character = input("Character Prefix ID: ").upper()
            if character in self.player_prefixes:
                character = self.player_prefixes[character]
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
                                status_effect = player.status_effect[remove-1]
                                status_effect.remove(player)
                                del player.status_effects[remove-1]
                        elif choice == "A":
                            effect = input("Apply effect: ").lower()
                            time = input("Time: ")
                            extend = input("Is Extended? [Y/N]: ").upper()
                            extend = 1.5 if extend == "Y" else 1
                            use_effect = input("Use Effect [Y/N]: ").upper()
                            if use_effect == "Y":
                                use_effect = True
                            else:
                                use_effect = False
                            status_effect = ef.effect_list(effect, int(time), 1, use_effect)
                            if status_effect.ept:
                                damage_effect = fs.is_int(input("Damage/Heal Effect: "))
                                status_effect.effect *= int(damage_effect)
                            else:
                                damage_effect = 1
                            if extend == 1.5:
                                status_effect.time *= extend
                            if status_effect.is_effect:
                                effect_multiplier = fs.is_int(input("Damage/Heal Effect Multiplier: "))
                            else:
                                effect_multiplier = 1
                            for current_effect in player.status_effects:
                                if current_effect.name == status_effect.name:
                                    print(f"{Fore.GREEN}[DEBUGG]{Style.RESET_ALL} Replacing Status Effect")
                                    player.status_effects.remove(current_effect)
                            player.status_effects.append(status_effect)
                            player.status_apply(status_effect, effect_multiplier)
                            print(f"{Fore.BLUE}[NOTE]{Style.RESET_ALL} {player.id} {player.firstname} has recieved {status_effect.name} for {status_effect.time} turns")
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
            self.player_equipment()
        elif choice == "S":
            character = input("Save character with Prefix ID: ").upper()
            if character == "SA":
                sl.save_all("character_saves", self.player_objects)
            else:
                if character in self.player_prefixes:
                    character = self.player_prefixes[character]
                    sl.save_character("character_saves", character)
        elif choice == "I":
            character = input("Character Prefix ID: ").upper()
            if character in self.player_prefixes:
                character = self.player_prefixes[character]
                for player in self.player_objects:
                    summons = [(obj.firstname, turns) for obj, turns in player.summons]
                    if player.prefix == character.prefix:
                        print(f"---------={player.firstname} {player.surname}=---------")
                        print(f"Board Piece: {player.prefix}")
                        print(f"Power level: {player.new_power_level}/{player.power_level}")
                        print(f"Karma: {player.new_karma}/{player.karma}")
                        print(f"Religion: {player.religion}")
                        print(f"Armor Class: {player.armor_class}")
                        spirits = []
                        for spirit in player.spirits:
                            spirits.append(spirit.firstname)
                        print(f"Spirits: {spirits}")
                        print(f"Summons: {summons}")
                        print("---------=Effects=---------")
                        for current_effect in player.status_effects:
                            print(f"{current_effect.name} [{current_effect.time_left}]")
                        for ability in player.abilities:
                            print(f"{ability.name} [{ability.time}]")
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
                        player.print_eq()

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
        elif choice == "C":
            return
    

    def generate_initiative(self):
        print("---------=Initiative=---------")
        while True:
            choice = input("[R]andom or [S]elect: ").upper()
            if choice == "R":
                for player in (p for p in self.player_objects if p.character_type != "spirit"):
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

class Scenario():
    def __init__(self, name: str, turn: int = 1, players: list[object] = None, playerturn: int = 0, mode = "Adventure"):
        self.name = name
        self.turn = turn
        self.playerturn = playerturn
        self.mode = mode
        self.players = players if players is not None else []
