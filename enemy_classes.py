import math
import sys
import numpy as np
import random
import weapons
import actions
import items
import characters
from levels import LEVEL_MULTIPLIER
from atk_categories import PHYSICAL_ATTACKS, ELEMENTAL_ATTACKS
from typing import List, Dict

class MikkMakk(characters.Enemy):

    def __init__(self, level, hp_max, speed, phys_def, elem_def, phys_atk, elem_atk, attacks, guard, weaknesses, action_count, ally):
        super().__init__(level, hp_max, speed, phys_def, elem_def, phys_atk, elem_atk, attacks, guard, weaknesses, action_count)

        self.boosted = False
        self.ally_weak = False
        self.ally_alive = True
        self.ally = None 

    def set_ally(self, ally):
        self.ally = ally

    def take_action(self, action_num: int, targets: List):
        random.shuffle(targets)
        if action_num == 0:
            #Attack, invocation_ratio = 100
            dmg = self.get_attacK_damage(targets[0])
            targets[0].hp = max(0, targets[0].hp - dmg)
        elif action_num == 1:
            #Slice, invocation_ratio = 130. This is technically a spread attack but doesnt matter for me
            i = 0
            while i < len(targets):
                dmg = self.get_slice_damage(targets[i])
                targets[i].hp = max(0, targets[i].hp - mdg)
        elif action_num == 2:
            #Mutiny, invocation_ratio = 115
            dmg = self.get_mutiny_damage(targets[0])
            targets[0].hp = max(0, targets[0].hp - dmg)
        elif action_num == 3:
            #We'll make ye walk the plank
            #Use on first turn below 50% hp, then do not use unless buffs wear out
            self.apply_phys_atk_buff(5)
            self.apply_phys_def_buff(5)
        elif action_num == 4:
            #Me mates got me back
            #Use once when partner falls below 50% hp. Does not need to use an action
            self.ally_weak = True
        elif action_num == 5:
            #Ye scurvy lubbers
            #Use at end of turn, does not need an action to cast
            #Unclear on the lo gic for choosing whether this is used, might be 50/50 at end of turn whilst under 50%
            self.boosted = True # need to somehow handle boost being reset on breaks, probably do it the same way in the game when we handle turn order movement
        elif action_num == 6:
            #Pirates pride, invocation_ratio = 225
            #Use if in boost mode, otherwise never called
            dmg = self.get_pride_damage(targets[0])
            targets[0].hp = max(0, targets[0].hp - dmg)
            self.boosted = False
    
    def calculate_damage(self, target: characters.Player, invocation_ratio) -> int:
        random_mult = random.uniform(0.98, 1.02)
        level_mult = LEVEL_MULTIPLIER.get(self.level)
        defence_ratio = 100 / invocation_ratio #not sure if this is technically correct, but i cant find any data, and this is the norm

        if 'phys_atk_buff' in self.buffs.keys(): #All Mikk/Makk atks are physical, but should probably handle this better
            buff_mult = 1.5
        else:
            buff_mult = 1

        if 'phys_def_debuff' in target.debuffs.keys():
            debuff_mult = 1.5
        else:
            debuff_mult = 1

        dmg = (self.phys_atk - (target.phys_def * defence_ratio / 2)) * (invocation_ratio / 100) * level_mult * random_mult * buff_mult * debuff_mult
        dmg = round(dmg)
        return dmg
    
    def get_attacK_damage(self, target) -> int:
        dmg = self.calculate_damage(target, invocation_ratio = 100)
        return dmg 
    
    def get_slice_damage(self, target) -> int:
        dmg = self.calculate_damage(self, target, invocation_ratio = 130)
        return dmg 
    
    def get_mutiny_damage(self, target) -> int:
        dmg = self.calculate_damage(self, target, invocation_ratio = 115)
        return dmg 
    
    def get_pride_damage(self, target) -> int:
        dmg = self.calculate_damage(self, target, invocation_Ratio = 225)
        return dmg
    
    def apply_phys_atk_buff(self, duration: int):
        if 'phys_atk_buff' not in self.buffs.keys():
            if 'phys_atk_debuff' in self.debuffs.keys():
                self.debuffs.pop('phys_atk_debuff')
            else:
                self.buffs['phys_atk_buff'] = duration
        elif 'phys_atk_buff' in self.buffs:
            self.buffs['phys_atk_buff'] = duration 

    def apply_phys_def_buff(self, duration: int):
        if 'phys_def_buff' not in self.buffs.keys():
            if 'phys_def_debuff' in self.debuffs.keys():
                self.debuffs.pop('phys_def_debuff')
            else:
                self.buffs['phys_def_buff'] = duration 
        elif 'phys_def_buff' in self.buffs:
            self.buffs['phys_def_buff'] = duration

    def remove_buffs(self, buff):
        self.buffs.pop(buff)

    def remove_debuffs(self, debuff):
        self.debuffs.pop(debuff)

    def countdown_buffs_debuffs(self):
        for i in self.buffs.keys():
            self.buffs[i] = self.buffs[i] - 1
            if self.buffs[i] == 0:
                self.remove_buffs(i)
        for i in self.debuffs.keys():
            self.debuffs[i] = self.debuffs[i] - 1
            if self.debuffs[i] == 0:
                self.remove_debuffs(i)

    def roll_action(self) -> int:
        #Choose the action
        if self.boosted: #If boosted, it will use pirates pride
            return 6
        elif self.ally_alive and self.ally.hp <= 0: #on the first turn after the ally is dead, it will buff itself
            self.ally_alive = False
            return 3
        elif not self.ally_alive and 'phys_atk_buff' not in self.buffs.keys() and 'phys_def_buff' not in self.buffs.keys(): #When ally is dead, and none of the buffs are present, can try to rebuff itself
            return random.randint(0,3)
        else: #All other circumstances, it will cycle between the first 3 attacks
            return random.randint(0,2) 
        
    def make_additional_acton(self) -> int: #choose an additional action, or return -1 if no additional action
        if not self.ally_weak and self.ally.hp / self.ally.max_hp < 0.5:
            self.ally_weak = True 
            return 4
        elif not self.ally_alive and not self.boosted:
            decision = random.randint(0,1)
            if decision == 1:
                return 5
            else:
                return -1
        else:
            return -1

    

