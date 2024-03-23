import math
import sys
import numpy as np
import pydantic
import characters 

class Grape:

    def __init__(self, restore_amount: int) -> None:

        self.restore_amount = restore_amount 

    def use(self, user: characters.Player) -> None: #can rework later if overheal is relevant
        user.hp = min(user.hp_max, user.hp + self.restore_amount)


HealingGrape = Grape(restore_amount=500)