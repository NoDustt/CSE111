import database_creation as db_creation
import game_functions as game
import modifier_functions as modifier
import shop_functions as shop
import team_functions as team
import turn_functions as turn
import unit_functions as unit
import user_functions as user


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
    
    print("Lets look at the persepctive of User 1 Versus User 2!")
    print("Printing the current game shop:")
    shopidG1 = shop.findShop(gameU1vsU2ID)[0]
    units = unit.findUnit(shopidG1)
    print(units)
    
    
    