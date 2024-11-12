from unit_functions import createUnit
from team_functions import createTeam
from shop_functions import createShop


sample_units = [
    ("Warrior", "1", "100", "15"),
    ("Archer", "1", "80", "20"),
    ("Mage", "1", "70", "25"),
    ("Knight", "1", "120", "10"),
    ("Healer", "1", "90", "5"),
]

def populateUnit():
    shopID = createShop()
    teamID = createTeam()

    
    for unit in sample_units:
        unitName, level, health, attack = unit
        createUnit(unitName, shopID, teamID, level, health, attack)


if __name__ == "__main__":
    populateUnit()




