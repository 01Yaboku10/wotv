import gamelogic as gl
import random
import spell as sp
import failsafe as fs
import math
import effects as ef
import racial_classes as rc
import job_classes as jc

class Game():
    def __init__(self):
        print("---------=New Scenario=---------")
        name = input("Name of Scenario: ").lower()
        self.scenario = Scenario(name)
        self.assigned_players, self.player_objects = gl.player_assign()
        self.team_1, self.team_2 = gl.team_assign(self.player_objects)
        print("---------=Teams=---------")
        print("Team 1:", end="")
        for player in self.team_1:
            print(f" ID:{player.id} {player.firstname}", end="")
        print(".")
        print("Team 2:", end="")
        for player in self.team_2:
            print(f" ID:{player.id} {player.firstname}", end="")
        print(".")
        self.game()

    def add_stats(self):
        print("DEBUGG: Adding characters...")
        for player in self.player_objects:
            player.new_hp = player.hp
            player.new_mp = player.mp
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
            print(f"DEBUGG: Added: {player.firstname}")

    def status_apply(self, player: object, effect: object, spell_effect: int):
        if effect.is_effect:
            effect.spell_effect=spell_effect
        bonus = spell_effect if effect.is_effect else 1
        bonus = abs(bonus)
        player.new_hp += round(effect.hp*bonus)
        player.new_mp += round(effect.mp*bonus)
        player.new_phyatk += round(effect.phyatk*bonus)
        player.new_phydef += round(effect.phydef*bonus)
        player.new_agility += round(effect.agility*bonus)
        print(f"EFFECT AGILITY: {effect.agility}")
        print(f"BONUS: {bonus}")
        player.new_finess += round(effect.finess*bonus)
        player.new_magatk += round(effect.magatk*bonus)
        player.new_magdef += round(effect.magdef*bonus)
        player.new_resistance += round(effect.resistance*bonus)
        player.new_special += round(effect.special*bonus)
        player.new_athletics += round(effect.athletics*bonus)
        player.new_acrobatics += round(effect.acrobatics*bonus)
        player.new_stealth += round(effect.stealth*bonus)
        player.new_sleight += round(effect.sleight*bonus)
        player.new_investigation += round(effect.investigation*bonus)
        player.new_insight += round(effect.insight*bonus)
        player.new_perception += round(effect.perception*bonus)
        player.new_deception += round(effect.deception*bonus)
        player.new_intimidation += round(effect.intimidation*bonus)
        player.new_persuasion += round(effect.persuasion*bonus)
        player.new_performance += round(effect.performance*bonus)
        player.new_karma += round(effect.karma*bonus)
        if effect.is_max:
            player.max_hp += round(effect.hp*bonus)
            player.max_mp += round(effect.mp*bonus)
            player.max_phyatk += round(effect.phyatk*bonus)
            player.max_phydef += round(effect.phydef*bonus)
            player.max_agility += round(effect.agility*bonus)
            player.max_finess += round(effect.finess*bonus)
            player.max_magatk += round(effect.magatk*bonus)
            player.max_magdef += round(effect.magdef*bonus)
            player.max_resistance += round(effect.resistance*bonus)
            player.max_special += round(effect.special*bonus)
            player.max_athletics += round(effect.athletics*bonus)
            player.max_acrobatics += round(effect.acrobatics*bonus)
            player.max_stealth += round(effect.stealth*bonus)
            player.max_sleight += round(effect.sleight*bonus)
            player.max_investigation += round(effect.investigation*bonus)
            player.max_insight += round(effect.insight*bonus)
            player.max_perception += round(effect.perception*bonus)
            player.max_deception += round(effect.deception*bonus)
            player.max_intimidation += round(effect.intimidation*bonus)
            player.max_persuasion += round(effect.persuasion*bonus)
            player.max_performance += round(effect.performance*bonus)
            player.max_karma += round(effect.karma*bonus)

    def status_update(self, player: object):
        if not player.status_effects is None:
            for effect in player.status_effects:
                if effect.ept:
                    print(f"Player {player.id} took {round(effect.effect)} damage from {effect.name}")
                    player.new_hp += round(effect.effect)
                bonus = effect.spell_effect if effect.is_effect else 1
                if effect.time_left == 0:
                    player.new_hp -= round(effect.hp*bonus)
                    player.new_mp -= round(effect.mp*bonus)
                    player.new_phyatk -= round(effect.phyatk*bonus)
                    player.new_phydef -= round(effect.phydef*bonus)
                    player.new_agility -= round(effect.agility*bonus)
                    player.new_finess -= round(effect.finess*bonus)
                    player.new_magatk -= round(effect.magatk*bonus)
                    player.new_magdef -= round(effect.magdef*bonus)
                    player.new_resistance -= round(effect.resistance*bonus)
                    player.new_special -= round(effect.special*bonus)
                    player.new_athletics -= round(effect.athletics*bonus)
                    player.new_acrobatics -= round(effect.acrobatics*bonus)
                    player.new_stealth -= round(effect.stealth*bonus)
                    player.new_sleight -= round(effect.sleight*bonus)
                    player.new_investigation -= round(effect.investigation*bonus)
                    player.new_insight -= round(effect.insight*bonus)
                    player.new_perception -= round(effect.perception*bonus)
                    player.new_deception -= round(effect.deception*bonus)
                    player.new_intimidation -= round(effect.intimidation*bonus)
                    player.new_persuasion -= round(effect.persuasion*bonus)
                    player.new_performance -= round(effect.performance*bonus)
                    if effect.is_max:
                        player.max_hp -= round(effect.hp*bonus)
                        player.max_mp -= round(effect.mp*bonus)
                        player.max_phyatk -= round(effect.phyatk*bonus)
                        player.max_phydef -= round(effect.phydef*bonus)
                        player.max_agility -= round(effect.agility*bonus)
                        player.max_finess -= round(effect.finess*bonus)
                        player.max_magatk -= round(effect.magatk*bonus)
                        player.max_magdef -= round(effect.magdef*bonus)
                        player.max_resistance -= round(effect.resistance*bonus)
                        player.max_special -= round(effect.special*bonus)
                        player.max_athletics -= round(effect.athletics*bonus)
                        player.max_acrobatics -= round(effect.acrobatics*bonus)
                        player.max_stealth -= round(effect.stealth*bonus)
                        player.max_sleight -= round(effect.sleight*bonus)
                        player.max_investigation -= round(effect.investigation*bonus)
                        player.max_insight -= round(effect.insight*bonus)
                        player.max_perception -= round(effect.perception*bonus)
                        player.max_deception -= round(effect.deception*bonus)
                        player.max_intimidation -= round(effect.intimidation*bonus)
                        player.max_persuasion -= round(effect.persuasion*bonus)
                        player.max_performance -= round(effect.performance*bonus)
                        player.max_karma -= round(effect.karma*bonus)

                    player.status_effects.remove(effect)
                    print(f"DEBUGG: {effect.name} removed")
                else:
                    effect.time_left -= 1
    
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
        print(f"Character [ID:{player.id}] {player.firstname}'s power level set to {player.new_power_level}")

    def game(self):
        print(f"---------=Scenario {self.scenario.name}=---------")
        self.add_stats()
        self.generate_initiative()
        tm = gl.Turnmeter()
        while True:
            print(f"---------=Scenario {self.scenario.name}, Turn {tm.currentturn}=---------")
            for player in self.initative_list:
                print(f"---------={player.firstname}'s Turn=---------")
                self.status_update(player)
                self.power_check(player)
                if player.status_effects:
                    print("Currently Active Effects:")
                    for stat_eff in player.status_effects:
                        print(f"{stat_eff.name} [{stat_eff.time_left}]")
                while True:
                    choice = input("[G]od action, [A]ction, [N]ext\n").upper().strip()
                    if choice == "G":
                        self.god_action()
                    elif choice == "A":
                        self.action(player)
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

        #  MP COST
        mp_cost = math.ceil(spell.tier*((1.5 if maximize == 1.25 else 1)+over+boost+silent+concentrate+widen+twin+triplet+delay))
        if mp_cost > player.new_mp:
            print("ERROR: MP Cost will exceed available MP")
            spell_enchantments.clear()
            return

        #  OPPONENT SELECTION
        if spell.type == "self_buff":
            opponent = player.id
        else:
            opponent_list = []
            while True:
                opponent = input("Opponent ID ([D]one): ").upper()
                if opponent == "D":
                    break
                if opponent in self.assigned_players:
                    for oppo in self.player_objects:
                        if oppo.id == int(opponent):
                            opponent_list.append(oppo)
                            print(f"DEBUGG: {opponent} added to opponent_list")

            #  ATTACK AND SAVE ROLL
            dice = fs.is_int(input(f"Dice Roll (D{fs.spell_dice(spell.tier)}): "))
            for opp in opponent_list:
                save = fs.is_int(input(f"Save throw for opponent {opp.id}: "))
                opp.save = save

            #  STATUS EFFECT ROLL
            if not spell.statuses is None:
                for effect in spell.statuses:
                    if effect.success != 1:
                        status_dice = fs.is_int(input(f"Status roll for {effect.name}: "))
                        if round(status_dice/fs.spell_dice(spell.tier))>=(1-effect.success):
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
                self.status_effect(spell, oppon)
                """if not spell.statuses is None:
                    for status_effect in spell.statuses:
                        if not status_effect.is_active:
                            continue
                        if save_reduction == 0:
                            continue
                        if status_effect.ept:
                            status_effect.effect *= round(effect)
                        if extend == 1.5:
                            status_effect.time *= extend
                        for current_effect in oppon.status_effects:
                            if current_effect.name == status_effect.name:
                                print("DEBUGG: Replacing Status Effect")
                                oppon.status_effects.remove(current_effect)
                        oppon.status_effects.append(status_effect)
                        self.status_apply(oppon, status_effect, effect)
                        print(f"Player {oppon.id} has recieved {status_effect.name} for {status_effect.time} turns")"""
                
                if not spell.type == "Buff":
                    print(f"Dealt {round(effect)} damage to Player {oppon.id}")
                print(f"Player {oppon.id} now has {oppon.new_hp}/{oppon.max_hp} HP")
            player.new_mp -= mp_cost
            print(f"Player {player.id} used {mp_cost} MP, and now has {player.new_mp}/{player.max_mp} MP")
            
            opponent_list.clear()
            spell_enchantments.clear()
            self.power_check(player)

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
                self.status_apply(opponent, status_effect, self.effect)
                print(f"Player {opponent.id} has recieved {status_effect.name} for {status_effect.time} turns")

    def god_action(self):
        choice = input("[D]amage/Heal, [E]ffect, [I]nfo, [C]ontinue\n").upper().strip()
        if choice == "D":
            character = input("Character ID: ")
            if str(character) in self.assigned_players:
                for player in self.player_objects:
                    if player.id == int(character):
                        damage = input("Deal damage(-)/heal(+) equal to: ")
                        player.new_hp += int(damage)
                        print(f"{player.firstname} took damage equal to {damage} and now has {player.new_hp} HP")
            else:
                print("ERROR: No player found")
        elif choice =="E":
            character = input("Character ID: ")
            if str(character) in self.assigned_players:
                for player in self.player_objects:
                    if player.id == int(character):
                        effect = input("Apply effect: ").lower()
                        time = input("Time: ")
                        extend = input("Is Extended? (Y/N): ").upper()
                        extend = 1.5 if extend == "Y" else 1
                        status_effect = ef.effect_list(effect, int(time), 1)
                        if status_effect.ept:
                            damage_effect = input("Damage Effect Multiplier: ")
                            status_effect.effect *= int(damage_effect)
                        else:
                            damage_effect = 1
                        if extend == 1.5:
                            status_effect.time *= extend
                        for current_effect in player.status_effects:
                            if current_effect.name == status_effect.name:
                                print("DEBUGG: Replacing Status Effect")
                                player.status_effects.remove(current_effect)
                        player.status_effects.append(status_effect)
                        self.status_apply(player, status_effect, damage_effect)
                        print(f"Player {player.id} has recieved {status_effect.name} for {status_effect.time} turns")
        elif choice == "I":
            character = input("Character ID: ")
            if str(character) in self.assigned_players:
                for player in self.player_objects:
                    if player.id == int(character):
                        print(f"---------={player.firstname} {player.surname}=---------")
                        print(f"Power level: {player.new_power_level}/{player.power_level}")
                        print("---------=Effects=---------")
                        for current_effect in player.status_effects:
                            print(f"{current_effect.name} [{current_effect.time_left}]")
                        print("---------=Stats=---------")
                        print(f"HP:{player.new_hp}/{player.max_hp}, MP:{player.new_mp}/{player.max_mp}\n"
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