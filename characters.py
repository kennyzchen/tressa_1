import math
import sys
import numpy as np
import random
import weapons
import actions
import items
from levels import LEVEL_MULTIPLIER
from typing import List, Dict

class Player:

    def __init__(self, level: int, hp_max: int, sp_max: int, speed: int, phys_def: int, elem_def: int, phys_atk: int, elem_atk: int, weapons: List, spells: List, items: Dict, traits) -> None:

        #These will not change for the purposes of this battle
        self.level = level
        self.hp_max = hp_max
        self.sp_max = sp_max
        self.speed = speed
        self.weapons = weapons 
        self.spells = spells
        self.traits = traits

        #These could change
        self.phys_def = phys_def
        self.elem_def = elem_def
        self.phys_atk = phys_atk 
        self.elem_atk = elem_atk
        self.active_weapon = weapons[0]
        self.hp = hp_max 
        self.sp = sp_max
        self.items = items
        self.buffs = []
        self.debuffs = []
        self.defended = False

    def change_active_weapon(self, weapon: weapons.Weapon) -> bool:
        if weapon not in self.weapons:
            return False 
        else:
            self.active_weapon = weapon 
            return True
        
    def use_offensive_spell(self, spell: actions.offensiveSpell, targets: List, boosts: int = 0) -> bool:
        if not spell.check_usable(self):
            return False 
        else:
            self.sp = self.sp - spell.sp_cost
        i = 0
        while i < len(spell.num_hits[boosts]):
            random_multiplier = random.uniform(0.98, 1.02)
            kind = spell.kinds[boosts][i]
            for target in targets:
                dmg = spell.calc_individual_damage(self, target, kind, boosts, random_multiplier)
                target.hp = max(0, target.hp - dmg)
                target.apply_breaks(kind)
                target.check_breaks()
            i = i + 1

    def get_attack_damage(self, target) -> int:
        phys_atk = self.phys_atk + self.active_weapon.phys_atk
        level_mult = LEVEL_MULTIPLIER.get(self.level)
        if target.broken:
            weakness_mult = 2
        elif self.active_weapon.kind in target.active_weaknesses:
            weakness_mult = 1.3
        else:
            weakness_mult = 1
        random_mult = random.uniform(0.98, 1.02)
        dmg = 0.8 * (phys_atk - target.phys_def * 0.5) * level_mult * weakness_mult * random_mult 
        dmg = round(dmg)
        return dmg
    
    def attack(self, target, boosts: int = 0) -> None:
        hits = 1 + boosts 
        i = 0
        while i < hits:
            dmg = self.get_attack_damage(target)
            target.hp = max(0, target.hp - dmg)
            target.apply_breaks(self.active_weapon.kind)
            target.check_breaks()
            i = i + 1

    def use_item(self, item) -> bool:
        if item not in self.items.keys():
            return False 
        elif self.items[item] == 0:
            return False 
        else:
            item.use(self)
            self.items[item] = self.items[item] - 1

    def defend(self):
        self.defended = True 

    def reset_defend(self):
        if self.defended:
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
        self.guard = guard
        self.broken = False

    def check_break(self) -> None:
        if self.guard == 0 and not self.broken:
            self.broken = True

    def apply_breaks(self, kind: str) -> None:
        if not self.broken:
            if kind in self.active_weaknesses:
                self.guard = self.guard - 1

    def recover_break(self) -> None:
        if self.broken:
            self.broken = False 
            self.guard = self.max_guard

    

