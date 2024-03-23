import math
import sys
import numpy as np
import random
import weapons
import actions
import items
import characters
from levels import LEVEL_MULTIPLIER
from typing import List, Dict

class MikkMakk(characters.Enemy):

    def __init__(self, level, hp_max, speed, phys_def, elem_def, phys_atk, elem_atk, attacks, guard, weaknesses, action_count):
        super().__init__(level, hp_max, speed, phys_def, elem_def, phys_atk, elem_atk, attacks, guard, weaknesses, action_count)

        self.boosted = False 
        self.ally_weak = False

    def take_action(self, action_num: int, target: List):
        if action_num == 0:
            #Attack, invocation_ratio = 100
        elif action_num == 1:
            #Slice, invocation_ratio = 130. This is technically a spread attack but doesnt matter for me
        elif action_num == 2:
            #Mutiny, invocation_ratio = 115
        elif action_num == 3:
            #We'll make ye walk the plank
            #Use on first turn below 50% hp, then do not use unless buffs wear out
        elif action_num == 4:
            #Me mates got me back
            #Use once when partner falls below 50% hp. Does not need to use an action
        elif action_num == 5:
            #Ye scurvy lubbers
            #Use at end of turn, does not need an action to cast
            #Unclear on the logic for choosing whether this is used, might be 50/50 at end of turn whilst under 50%
        elif action_num == 6:
            #Pirates pride, invocation_ratio = 225
            #Use if in boost mode, otherwise never called
    
    def calculate_damage(self, target, invocation_ratio) -> int:
        random_mult = random.uniform(0.98, 1.02)
        level_mult = LEVEL_MULTIPLIER.get(self.level)
        defence_ratio = 100 / invocation_ratio #not sure if this is technically correct, but i cant find any data, and this is the norm
        dmg = (self.phys_atk - (target.phys_def * defence_ratio / 2)) * (invocation_ratio / 100) * level_mult * random_mult
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
