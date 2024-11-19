from unit_functions import createUnit
from team_functions import createTeam
from shop_functions import createShop
from modifier_functions import createModifier

sample_modifiers = [
    ("Mighty Boost", "Increases attack power by 10%"),
    ("Stone Skin", "Reduces incoming damage by 15%"),
    ("Swiftness", "Increases movement speed by 20%"),
    ("Regen", "Restores 5 health per turn"),
    ("Poison Touch", "Deals 5 poison damage per turn to enemies"),
]

def populateModifier():
    shopID = createShop()
    teamID = createTeam()
    unitID = createUnit()

    
    for modifier in sample_modifiers:
        modifierName, effect = modifier
        createModifier(unitID, shopID, effect, modifierName)



if __name__ == "__main__":
    populateModifier()

