import gamelogic as gl
import random
import spell as sp
import failsafe as fs
import math
import effects as ef
import racial_classes as rc
import job_classes as jc
import saveloader as sl
import manu as menu

class Game():
    def __init__(self):
        print("---------=New Scenario=---------")
        name = input("Name of Scenario: ").lower()
        self.scenario = Scenario(name)
        self.assigned_players, self.player_objects, self.player_prefixes = gl.player_assign()
        gl.team_assign(self.player_objects)
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
                self.gamemode_battle()
                break
            elif gamemode == "A":
                self.gamemode_adventure()
                break

    def add_stats(self, player: list[object] = None):
        print("DEBUGG: Adding characters...")
        if player is not None:
            player_list = player
        else:
            player_list = self.player_objects

        for player in player_list:
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
            player.new_power_level = player.power_level
            sl.update_sheet(player)
            print(f"DEBUGG: Added: {player.firstname}")

    def status_update(self, player: object):
        if not player.status_effects is None:
            for effect in player.status_effects:
                if effect.ept:
                    print(f"Player {player.prefix} {player.firstname} took {round(effect.effect)} damage from {effect.name}")
                    player.new_hp += round(effect.effect)
                if effect.time_left == 0:
                    player.new_hp -= effect.new_hp
                    player.new_mp -= effect.new_mp
                    player.new_sp -= effect.new_sp
                    player.new_phyatk -= effect.new_phyatk
                    player.new_phydef -= effect.new_phydef
                    player.new_agility -= effect.new_agility
                    player.new_finess -= effect.new_finess
                    player.new_magatk -= effect.new_magatk
                    player.new_magdef -= effect.new_magdef
                    player.new_resistance -= effect.new_resistance
                    player.new_special -= effect.new_special
                    player.new_athletics -= effect.new_athletics
                    player.new_acrobatics -= effect.new_acrobatics
                    player.new_stealth -= effect.new_stealth
                    player.new_sleight-= effect.new_sleight
                    player.new_investigation -= effect.new_investigation
                    player.new_insight -= effect.new_insight
                    player.new_perception -= effect.new_perception
                    player.new_deception -= effect.new_deception
                    player.new_intimidation -= effect.new_intimidation
                    player.new_persuasion -= effect.new_persuasion
                    player.new_performance -= effect.new_performance
                    player.new_karma -= effect.new_karma
                    if effect.is_max:
                        player.max_hp -= effect.new_hp
                        player.max_mp -= effect.new_mp
                        player.max_sp -= effect.new_sp
                        player.max_phyatk -= effect.new_phyatk
                        player.max_phydef -= effect.new_phydef
                        player.max_agility -= effect.new_agility
                        player.max_finess -= effect.new_finess
                        player.max_magatk -= effect.new_magatk
                        player.max_magdef -= effect.new_magdef
                        player.max_resistance -= effect.new_resistance
                        player.max_special -= effect.new_special
                        player.max_athletics -= effect.new_athletics
                        player.max_acrobatics -= effect.new_acrobatics
                        player.max_stealth -= effect.new_stealth
                        player.max_sleight -= effect.new_sleight
                        player.max_investigation -= effect.new_investigation
                        player.max_insight -= effect.new_insight
                        player.max_perception -= effect.new_perception
                        player.max_deception -= effect.new_deception
                        player.max_intimidation -= effect.new_intimidation
                        player.max_persuasion -= effect.new_persuasion
                        player.max_performance -= effect.new_performance
                        player.max_karma -= effect.new_karma

                    player.status_effects.remove(effect)
                    print(f"DEBUGG: {effect.name} removed")
                else:
                    effect.time_left -= 1
        sl.update_sheet(player)
    
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
        print(f"Character [ID:{player.prefix}] {player.firstname}'s power level set to {player.new_power_level}")

    def player_equipment(self):
        while True:
            set_player = input("Player Prefix ID: ").upper()
            if set_player in self.player_prefixes:
                while True:
                    player = self.player_prefixes[set_player]
                    player.print_eq()
                    choice = input("[A]dd, [R]emove, [U]se, [E]quip, [T]ransfer, [D]one: ").upper()
                    if choice == "A":
                        player.equipment_add()
                    elif choice == "U":
                        player.inventory_use()
                        sl.update_sheet(player)
                    elif choice == "T":
                        if not player.inventory:
                            print("ERROR: Inventory Empty")
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
                                    if fs.is_tuple(item):
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
                                    print("ERROR: Player not found...")
                        
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
                                player.equipment_remove()
                                break
                    elif choice == "E":
                        player.inventory_equip()
                    elif choice == "D":
                        break
                break

    def gamemode_adventure(self):
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

    def gamemode_battle(self, start = False):
        print(f"---------=Scenario {self.scenario.name}=---------")
        self.generate_initiative()
        tm = gl.Turnmeter()
        while True:
            print(f"---------=Scenario {self.scenario.name}, Turn {tm.currentturn}=---------")
            for player in self.initative_list:
                print(f"---------=[{player.prefix}] {player.firstname}'s Turn=---------")
                if not start:
                    self.status_update(player)
                start = False
                self.power_check(player)
                if player.status_effects:
                    print("Currently Active Effects:")
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

    def action(self, player):
        while True:
            cast_spell = input("Cast spell: ")
            if fs.is_spell(cast_spell):
                break
            else:
                print("Try again...")
        spell = sp.spell_list(cast_spell)

        #  ENCHANTMENT
        spell_enchantments = []
        while True:
            enchantment = input("Add Enchantments: [M]aximize, [E]xtend, [P]enetrate, [O]ver, [B]oosted, [D]elay, [S]ilent, [TWIN], [TRIPLET], [CON]centrated, [W]iden [C]ontinue: ").upper().strip()
            if enchantment == "C":
                break
            spell_enchantments.append(enchantment)
            print(f"DEBUGG: Added {enchantment}")
        
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
                print("ERROR: MP Cost will exceed available MP")
                spell_enchantments.clear()
                return
        else:
            mp_cost = 0
        if spell.use_sp:
            sp_cost = math.ceil(spell.tier*((1.5 if maximize == 1.25 else 1)+over+boost+silent+concentrate+widen+twin+triplet+delay))
            if sp_cost > player.new_sp:
                print("ERROR: SP Cost will exceed available SP")
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
                if opponent in self.player_prefixes:
                    opponent = self.player_prefixes[opponent]
                    for oppo in self.player_objects:
                        if oppo.prefix == opponent.prefix:
                            opponent_list.append(oppo)
                            print(f"DEBUGG: {opponent.prefix} {opponent.firstname} added to opponent_list")

            #  ATTACK AND SAVE ROLL
            dice = fs.is_int(input(f"Dice Roll (D{fs.spell_dice(spell.tier)}): "))
            for opp in opponent_list:
                save = fs.is_int(input(f"Save throw for opponent {opp.prefix} {opp.firstname}: "))
                opp.save = save

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
                else:
                    caster_multiplier = player.new_magatk
                    opponent_multiplier = oppon.new_magdef

                save_reduction = (((int(dice) * 3) - int(oppon.save)) / (int(dice) * 3)) if (((int(dice) * 2) - int(oppon.save))) > 0 else 0
                self.save_reduction = save_reduction
                if spell.type != "Buff":
                    effect = (int(dice)/int(fs.spell_dice(spell.tier))) * int(spell.effect) * \
                    (1-(0.01*((opponent_multiplier*penetrate*pierce) - caster_multiplier))) * affinity * maximize * save_reduction
                    oppon.new_hp += round(effect)   #  Effect is DiceRoll/DiceTier * DefenceDiff * Affinities * Enchantments * Save Throw
                else:
                    effect = (int(dice)/int(fs.spell_dice(spell.tier))) * int(spell.effect) * \
                    (1+(0.01*caster_multiplier)) * affinity * maximize * save_reduction
                self.effect = effect
                
                #  STATUS EFFECTS
                print("-------------------------")
                self.status_effect(spell, oppon)
                if not spell.type == "Buff":
                    print(f"Dealt {round(effect)} damage to Player {oppon.prefix} ID:{oppon.id}")
                print(f"Player {oppon.prefix} ID:{oppon.id} now has {oppon.new_hp}/{oppon.max_hp} HP")
                sl.update_sheet(oppon)
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
                print(f"Player {player.prefix} ID:{player.id} used {mp_cost} MP, and now has {player.new_mp}/{player.max_mp} MP")
            if spell.use_sp:
                print(f"Player {player.prefix} ID:{player.id} used {sp_cost} SP, and now has {player.new_sp}/{player.max_sp} SP")
            if spell.karma != 0:
                print(f"Player {player.prefix} ID:{player.id} used {spell.karma} Karma, and now has {player.new_karma} Karma")
            
            opponent_list.clear()
            spell_enchantments.clear()
            self.power_check(player)
            sl.update_sheet(player)

            for play in self.player_objects:
                if play.new_hp <= 0:
                    self.player_objects.remove(play)
                    self.initative_list.remove(play)
                    print(f"DEBUGG: {play.firstname} has been slain")
    
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
                for current_effect in opponent.status_effects:
                    if current_effect.name == status_effect.name:
                        print("DEBUGG: Replacing Status Effect")
                        opponent.status_effects.remove(current_effect)
                opponent.status_effects.append(status_effect)
                opponent.status_apply(status_effect, self.effect)
                print(f"Player {opponent.prefix} ID:{opponent.id} has recieved {status_effect.name} for {status_effect.time} turns")

    def god_action(self):
        choice = input("[D]amage/Heal, [P]layer, [B]ackpack, [E]ffect, [I]nfo, [S]ave, [Q]uit, [C]ontinue\n").upper().strip()
        if choice == "D":
            character = input("Character Prefix ID: ").upper()
            if character in self.player_prefixes:
                character = self.player_prefixes[character]
                for player in self.player_objects:
                    if not fs.is_attrib(player, "prefix"):
                        continue
                    if player.prefix == character.prefix:
                        damage = input("Deal damage(-)/heal(+) equal to: ")
                        player.new_hp += int(damage)
                        print(f"{player.firstname} took damage equal to {damage} and now has {player.new_hp} HP")
                        sl.update_sheet(player)
            else:
                print("ERROR: No player found")
        elif choice == "P":
            assigned, objects, prefixes = gl.player_assign(self.player_objects)

            for i in objects:
                if i.id not in self.assigned_players:
                    print(f"ADDING STATS FOR {i.firstname}")
                    self.add_stats([i])

            self.assigned_players = assigned
            self.player_objects = objects
            self.player_prefixes = prefixes
        elif choice =="E":
            character = input("Character Prefix ID: ").upper()
            if character in self.player_prefixes:
                character = self.player_prefixes[character]
                character = character.id
                for player in self.player_objects:
                    if player.id == int(character):
                        choice = input("[A]dd, [E]dit: ").upper()
                        if choice == "E":
                            if not player.status_effects:
                                print("No Status Effects applied")
                                return
                            for index, status in enumerate(player.status_effects):
                                print(f"[{index+1}] {status.name} [{status.time_left}]")
                            
                            choice = input("Edit id: ").upper()
                            if not choice.isdigit():
                                print("ERROR: Not integer")
                                return
                            choice = int(choice)
                            if 1 <= choice <= len(player.status_effects):
                                status_effect = player.status_effects[choice-1]
                                status_effect.edit()
                                self.status_update(player)
                            else:
                                print("Choice out of bounce")
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
                                    print("DEBUGG: Replacing Status Effect")
                                    player.status_effects.remove(current_effect)
                            player.status_effects.append(status_effect)
                            player.status_apply(status_effect, effect_multiplier)
                            print(f"Player {player.id} has recieved {status_effect.name} for {status_effect.time} turns")
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
                character = character.id
                for player in self.player_objects:
                    if player.id == int(character):
                        print(f"---------={player.firstname} {player.surname}=---------")
                        print(f"Board Piece: {player.prefix}")
                        print(f"Power level: {player.new_power_level}/{player.power_level}")
                        print(f"Karma: {player.new_karma}/{player.karma}")
                        print(f"Religion: {player.religion}")
                        print("---------=Effects=---------")
                        for current_effect in player.status_effects:
                            print(f"{current_effect.name} [{current_effect.time_left}]")
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
            print("Returning to Main Menu...")
            menu.main_menu()
        elif choice == "C":
            return
    

    def generate_initiative(self):
        self.initative_list = []
        for player in self.player_objects:
            player.initiative = random.randint(1, 20)
            self.initative_list.append(player)
        self.initative_list.sort(key=lambda x: x.initiative, reverse=True)

class Scenario():
    def __init__(self, name):
        self.name = name
