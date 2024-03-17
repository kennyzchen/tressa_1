import math
import sys
import numpy as np
import random
from pydantic import List
import characters
from levels import LEVEL_MULTIPLIER

def Spell():

    def __init__(self, defence_ratio: float, invocation_ratio: float, sp_cost: int, boost_ratio = List[int], num_hits = List[int], kinds = List[Tuple[str]]) -> None:
        
        self.defence_ratio = defence_ratio 
        self.invocation_ratio = invocation_ratio 
        self.sp_cost = sp_cost
        self.boost_ratio = boost_ratio #Length 4 list, each index corresponds to boost multiplier for that level of boost.
        self.num_hits = num_hits #Length 4 list, each index corresponds to the number of attacks occurring for that level of boost
        self.kinds = kinds #List of length 4, with each index being a tuple with length corresponding to the number of hits at that boost. Each index of this list contains the kind of dmg each spell inflicts

    def check_usable(self, user: characters.Player) -> bool:
        if user.sp >= self.sp_cost:
            return True 
        else:
            return False

    def calc_individual_damage(self, user: characters.Player, target: characters.Enemy, kind: str, boosts: int = 0, random_multipler: float = random.uniform(0.98, 1.02)) -> int:
        #Calcs damage for one instance of a spell usage (e.g. if multi hit, only calcs one instance)

        atk_val = user.elem_atk
        def_val = target.elem_def
        boost_multiplier = self.boost_ratio[boosts]
        random_multipler = random_multipler
        if target.broken:
            weakness_multiplier = 2
        elif kind in target.active_weaknesses:
            weakness_multiplier = 1.3
        else:
            weakness_multiplier = 1
        if kind + '_boost' in user.buffs:
            elemental_multiplier = 1.3 
        else:
            elemental_multiplier = 1
        dmg = (atk_val - (def_val * self.defence_ratio / 2)) * (self.invocation_ratio / 100) * (boost_multiplier / 100) * weakness_multiplier * LEVEL_MULTIPLIER.GET(user.level) * elemental_multiplier * random_multiplier * 0.5
        dmg = round(dmg)
        return dmg
    
Tradewinds = Spell(defence_ratio = 0.769, invocation_ratio = 130, sp_cost = 7, boost_ratio = [100, 200, 300, 400], num_hits = [1,1,1,1], kinds = [('wind'), ('wind'), ('wind'), ('wind')])
