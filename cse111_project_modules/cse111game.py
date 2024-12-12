import database_creation as db_creation
import game_functions as game
import modifier_functions as modifier
import shop_functions as shop
import team_functions as team
import turn_functions as turn
import unit_functions as unit
import user_functions as user
from getpass import getpass
import os

def playerTurn(userID, shopID, teamID, gameID, opponent):
    os.system('clear')
    while True:
        print(f"Game vs {opponent}")
        turnNumber = int(turn.findLatestTurn(gameID)[0][0])
        print(f"Current Turn: {turnNumber}")
        print(f"\n=== Your Turn ===")
        print("1. View Shop")
        print("2. Buy Unit or Modifier")
        print("3. View Your Team")
        print("4. End Turn")
        gold = int(turn.getGold(gameID, turnNumber)[0][0])
        action = input("Choose an action (1-4): ")
        if action == "1":
            print("\nAvailable units in shop:")
            units = unit.findUnit(shopID, 10)  
            for u in units:
                print(f"Name: {u[1]}, Cost: {u[2]}, Health: {u[3]}, Attack: {u[4]}")
            
            print("\nAvailable modifiers in shop:")
            modifiers = modifier.findModifier(shopID)  
            for m in modifiers:
                print(f"Name: {m[1]}, Effect: {m[2]} on {m[3]} Cost: {m[4]}")  # Modifier name, effect value, and attribute
            print(f"You have {gold} gold.")
        elif action == "2":
            print("1. Buy a Unit")
            print("2. Buy a Modifier")
            buy_choice = input("Choose an option (1-2): ")

            if buy_choice == "1":
                unit_name = input("Enter the unit name you want to purchase: ")
                units = unit.findUnit(shopID, gold)
            
                unitID = None
                for u in units:
                    if u[1] == unit_name:  
                        unitID = u[0]  
                        break
                if unitID:
                    print(f"Purchasing {unit_name}...")
                    # Link the unitID to the player's teamID
                    unit.addUnitToTeam(teamID, unitID, gameID, userID, turnNumber)  
                    os.system('clear')
                    print(f"{unit_name} has been added to your team!")
                else:
                    os.system('clear')
                    print(f"Unit {unit_name} not found in the shop.")

            elif buy_choice == "2":
                modifier_name = input("Enter the modifier name you want to purchase: ")
                modifiers = modifier.findModifier(shopID)  
                modifier_to_buy = None
                for m in modifiers:
                    if m[1] == modifier_name: 
                        modifier_to_buy = m
                        break
                
                if modifier_to_buy:
                    print(f"Purchasing {modifier_name}...")
                    print("Select a unit to apply the modifier to:")
                    team_units = team.getTeam(teamID)  # Get all units in the player's team

                    unit_name_to_apply = input("Enter the unit name to apply the modifier to: ")
                    selected_unit = None
                    for u in team_units:
                        if u['name'] == unit_name_to_apply: 
                            selected_unit = u['id']
                            break
                    
                    if selected_unit:
                        print(f"Applying {modifier_name} to {unit_name_to_apply}...")
                        unitID = selected_unit 
                        modifier_effect = modifier_to_buy[2]  # Effect value
                        modifier_attribute = modifier_to_buy[3]  # Attribute affected (health, attack)
                        cost = modifier_to_buy[4]
                        
                        # Apply the modifier effect to the unit
                        modifier.applyModifier(unitID, modifier_effect, modifier_attribute, cost, gameID, userID, turnNumber)
                        os.system('clear')
                        print(f"{modifier_name} has been applied!")
                    else:
                        os.system('clear')
                        print(f"Unit {unit_name_to_apply} not found in your team.")
                else:
                    os.system('clear')
                    print(f"Modifier {modifier_name} not found in the shop.")

        elif action == "3":
            # Modify team
            os.system('clear')
            team_units = team.getTeam(teamID)  # Get the current team units
            print()

            # print("Options: ")
            # print("1. Sell a unit")
            # print("2. Rearrange units")

            # team_action = input("Choose an action (1-2): ")

            # if team_action == "1":
            #     unit_to_sell = input("Enter the unit name to sell: ")
            #     team.sellUnit(teamID, unit_to_sell)  # Implement selling logic
            #     print(f"Sold unit {unit_to_sell}")

            # elif team_action == "2":
            #     print("Rearranging units...")
            #     team.rearrangeUnits(teamID)  # Implement rearranging logic

        elif action == "4":
            unit.createBotTeam(gameID, turnNumber)  
            os.system('clear')
            print("Ending turn...")
            fightingTurn(userID, gameID, teamID, turnNumber)
            
            turnNumber += 1
            turn.incrementTurn(gameID, turnNumber)
            shop.genNewShops(gameID, turnNumber)
            shopID = shop.getTurnShop(userID, gameID, turnNumber)
            team.dupeTeams(gameID, turnNumber)
            teamID = team.getPlayerTeamID(userID, gameID, turnNumber)

        elif action == "5":
            break
        else:
            print("Invalid input. Please choose a valid option.")

def fightingTurn(userID, gameID, teamID, turnNumber):
    print("Currently fighting...")
    team.getTeam(teamID)
    team.getPlayerTeam(1, gameID, turnNumber)
    

if __name__ == "__main__":
    os.system('clear')
    print("Resetting database...\n\n")
    db_creation.databaseReset()
    user.createuser("Botguy", "1")
    running = True
    userid = 0
    loggedin = False
    playing = False
    while(running):
        selector = input("1: Create User\n2: Login User\n3: Exit\nSelect what option you want to do: ")
        if int(selector) == 1:
            print("Now Creating A User...")
            username = input("Enter Username: ")
            print("Enter a password")
            password = getpass()
            # userid = input("Enter A UserID: ")
            result = user.createuser(username, password)
            if result != -1:
                os.system('clear')
                print("Successfully created a user!")
            else:
                print("User already exists")
        if int(selector) == 2:
            print("Now Logging In A User!")
            username = input("Enter Username: ")
            print("Enter a password")
            password = str(getpass())
            result = user.login(username, password)
            if result != -1:
                os.system('clear')
                print("Sucessfully logged in user!")
                userid = result
                loggedin = True
                print("Welcome to the game!")
        while(loggedin):
            results = game.findUserGames(userid)
            if results != []:
                print("Here are all your active games:")
                for index, result in enumerate(results):
                    game_id = result[0]
                    opponent_name = result[1]
                    print(f"{index + 1}: Game {index + 1} - Playing against {opponent_name}")
                selector = input("Please input what you would like to do.\n1: Create A New game\n2: Resume a game\n3: Log out\nSelect what option you want to do: ")
            else: 
                print("You do not have any active games")
                selector = input("Please input what you would like to do.\n1: Create A New game\n3: Log out\nSelect what option you want to do: ")
            if int(selector) == 1:
                print("Creating a new game...")
                gameID, shopID, teamID = game.createGame(userid, 1)
            if int(selector) == 2:
                gameselector = input("Please enter the number of the game you want to choose:\n")
                gameselector = int(gameselector) - 1
                if 0 <= gameselector and gameselector < len(results):
                    gameid = results[gameselector][0]
                    print(f"Now playing vs {results[gameselector][1]}")
                    playing = True
                else:
                    print("Invalid game selection")
            if int(selector) == 3:
                print("Now logging out.")
                loggedin = False
            while(playing):
                playerTurn(userid, shopID, teamID, gameid, opponent_name)
                playing = False
        if int(selector) == 3:
            print("Thanks for playing!")
            running = False
    
    
    