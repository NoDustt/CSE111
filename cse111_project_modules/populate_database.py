import database_creation as db_creation
import game_functions as game
import modifier_functions as modifier
import shop_functions as shop
import team_functions as team
import turn_functions as turn
import unit_functions as unit
import user_functions as user

def playerTurn(userID, shopID, teamID):
    print(f"\n=== {userID}'s Turn ===")
    print("1. View Shop")
    print("2. Buy Unit")
    print("3. Modify Team")
    print("4. End Turn")

    while True:
        action = input("Choose an action (1-4): ")
        
        if action == "1":
            # View shop and available units
            print("Available units in shop:")
            units = unit.findUnit(shopID)  # Find units available in the shop
            for u in units:
                print(f"Name: {u['name']}, Level: {u['level']}, Health: {u['health']}, Attack: {u['attack']}")
        
        elif action == "2":
            # Buy a unit
            print("Enter the unit name you want to purchase: ")
            unit_name = input("Unit name: ")

            units = unit.findUnit(shopID)  # Find all units in the shop
            unit_to_buy = None
            for u in units:
                if u['name'] == unit_name:
                    unit_to_buy = u
                    break
            
            if unit_to_buy:
                print(f"Purchasing {unit_name}...")
                unit.addUnitToTeam(teamID, unit_to_buy)  # Add the unit to the player's team
                print(f"{unit_name} has been added to your team!")
            else:
                print(f"Unit {unit_name} not found in the shop.")
        
        elif action == "3":
            print("Your current team:")
            team_units = team.getTeamUnits(teamID)  # Get the current team units
            for u in team_units:
                unit_name, unit_level, unit_health, unit_attack = u
                print(f"Name: {unit_name}, Level: {unit_level}, Health: {unit_health}, Attack: {unit_attack}")

            print("Options: ")
            print("1. Sell a unit")

            team_action = input("Choose an action (1-3): ")

            if team_action == "1":
                unit_to_sell = input("Enter the unit name to sell: ")
                team.sellUnit(teamID, unit_to_sell)  # Implement selling logic
                print(f"Sold unit {unit_to_sell}")

            elif team_action == "2":
                print("Rearranging units...")
                team.rearrangeUnits(teamID)  # Implement rearranging logic
        
        elif action == "4":
            print("Ending turn...")
            break
        
        else:
            print("Invalid input. Please choose a valid option.")


if __name__ == "__main__":
    print("Resetting database...\n\n")
    db_creation.databaseReset()
    print("Creating users...")
    print("User 1: Mark\nPassword: Araza")
    user1ID = user.createuser("Mark", "Araza")
    print("Mark's ID: " + user1ID)
    print("User 2: An\nPassword: Nguyen")
    user2ID = user.createuser("An", "Nguyen")
    user3name = input("Create a new user...\nUsername: ")
    user3password = input("Password: ")
    user3ID = user.createuser(user3name, user3password)

    print("\n\nCreating games...")
    gameU1vsU2ID = game.createGame(user1ID, user2ID)
    gameU1vsU3ID = game.createGame(user1ID, user3ID)
    gameU2vsU3ID = game.createGame(user2ID, user3ID)
    
    print("Games created!")
    
    print("Let's look at the perspective of User 1 Versus User 2!")
    print("Printing the current game shop:")
    shopidG1 = shop.findShop(gameU1vsU2ID)[0]
    units = unit.findUnit(shopidG1)
    print(units)

    teamID = team.createTeam("Team 1", user1ID)  # Assume you create a team for User 1

    playerTurn(user1ID, shopidG1, teamID)
