import weapons
import actions
import characters
import items

tressa_lvl_one = characters.Player(
    level = 1,
    hp_max = 275,
    sp_max = 50,
    speed = 72,
    phys_def = 94,
    elem_def = 83,
    phys_atk = 88,
    elem_atk = 88,
    weapons = [weapons.Spear, weapons.WolfsBow],
    spells = [actions.Tradewinds],
    items = {items.HealingGrape: 3},
    traits = None #idk why i added this and I forgor
)