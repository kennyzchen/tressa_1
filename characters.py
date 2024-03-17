import math
import sys
import numpy as np

class Player:

    def __init__(self, level, hp_max, sp_max, speed, phys_def, elem_def, phys_atk, elem_atk, weapons, spells, items) -> None:

        #These will not change for the purposes of this battle
        self.level = level
        self.hp_max = hp_max
        self.sp_max = sp_max
        self.speed = speed
        self.weapons = weapons 
        self.spells = spells

        #These could change
        self.phys_def = phys_def
        self.elem_def = elem_def
        self.phys_atk = phys_atk 
        self.elem_atk = elem_atk
        self.hp = hp_max 
        self.sp = sp_max
        self.items = items
        self.buffs = []
        self.debuffs = []
        self.defended = False

class Enemy:

    def __init__(self, level, hp_max, speed, phys_def, elem_def, phys_atk, elem_atk, attacks, guard, weaknesses, action_count = 1) -> None:
        
        self.level = level
        self.hp_max = hp_max
        self.max_guard = guard
        self.speed = speed
        self.weaknesses = weaknesses
        self.attacks = attacks 

        self.hp = hp_max 
        self.phys_def = phys_def 
        self.elem_def = elem_def
        self.phys_atk = phys_atk 
        self.elem_atk = elem_atk 
        self.active_weaknesses = weaknesses
        self.buffs = [] 
        self.debuffs = []
        self.action_count = action_count
        self.broken  = False

    

