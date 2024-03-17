import math
import sys
import numpy as np
import pydantic

class Weapon:

    def __init__(self, phys_atk: int, elem_atk: int, kind: str) -> None:

        self.phys_atk = phys_atk 
        self.elem_atk = elem_atk 
        self.kind = kind
    
    def get_phys_atk(self) -> int:
        return self.phys_atk 

    def get_elem_atk(self) -> int:
        return self.elem_atk
    
    def get_kind(self) -> str:
        return self.kind
    
Spear: Weapon = Weapon(8, 0, "Polearm")

WolfsBow: Weapon = Weapon(42, 34, "Bow")