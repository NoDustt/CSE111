import database_creation as db_creation
import game_functions as game
import modifier_functions as modifier
import shop_functions as shop
import team_functions as team
import turn_functions as turn
import unit_functions as unit
import user_functions as user
from getpass import getpass


if __name__ == "__main__":
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
                print("Sucessfully logged in user!")
                userid = result
                loggedin = True
                print("Welcome to the game!")
        while(loggedin):
            results = game.findUserGamers(userid)
            if results != []:
                print("Here are all your active games:")
                for result in results:
                    print(result[0])
                selector = input("Please input what you would like to do.\n1: Create A New game\n2: Resume a game\n3: Log out\nSelect what option you want to do: ")
            else: 
                print("You do not have any active games")
                selector = input("Please input what you would like to do.\n1: Create A New game\n3: Log out\nSelect what option you want to do: ")
            if int(selector) == 1:
                print("Creating a new game...")
                game.createGame(userid, 1)
            if int(selector) == 2:
                gameid = input("Please copy paste or enter the game you want to choose:\n")
                gamesearch = (gameid,)
                if gamesearch in results:
                    print("Now playing a game!")
                    playing = True
            if int(selector) == 3:
                print("Now logging out.")
                loggedin = False
            while(playing):
                print("Playing game!")
                playing = False
        if int(selector) == 3:
            print("Thanks for playing!")
            running = False
    
    
    