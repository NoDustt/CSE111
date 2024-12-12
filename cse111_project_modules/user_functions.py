import database_connection as conn
import uuid 
import bcrypt
#file for all relelvant user function
def createuser(username, password):
    connection = conn.databaseConnection()
    
    cursor = connection.cursor()
    
    playerid = str(uuid.uuid4())
    
    checkusername = '''
        SELECT * FROM user
        WHERE u_username = ?  
    '''
    cursor.execute(checkusername, (username,))
    result = cursor.fetchall()
    if result == []:
        userquery = '''
            INSERT INTO user(u_username, u_playerid)
            VALUES (?, ?)
        '''
        
        values = (username, playerid)
        cursor.execute(userquery, values)
        connection.commit()
        salt = bcrypt.gensalt()
        hashedpassword = bcrypt.hashpw(password.encode("utf-8"), salt)
        
        passwordquery = '''
            INSERT INTO password(p_username, p_playerid, p_hashedpassword, p_salt)
            VALUES (?, ?, ?, ?)
        '''
        
        cursor.execute(passwordquery, (username, playerid, hashedpassword, salt))
        
        connection.commit()
        conn.closeConnection(connection)
        return playerid
    return "user already exists"

def create_user_with_id(username, password, playerid):
    connection = conn.databaseConnection()
    
    cursor = connection.cursor()
    
    
    checkusername = '''
        SELECT * FROM user
        WHERE u_username = ?  
    '''
    cursor.execute(checkusername, (username,))
    result = cursor.fetchall()
    if result == []:
        userquery = '''
            INSERT INTO user(u_username, u_playerid)
            VALUES (?, ?)
        '''
        
        values = (username, playerid)
        cursor.execute(userquery, values)
        connection.commit()
        salt = bcrypt.gensalt()
        hashedpassword = bcrypt.hashpw(password.encode("utf-8"), salt)
        
        passwordquery = '''
            INSERT INTO password(p_username, p_playerid, p_hashedpassword, p_salt)
            VALUES (?, ?, ?, ?)
        '''
        
        cursor.execute(passwordquery, (username, playerid, hashedpassword, salt))
        
        connection.commit()
        conn.closeConnection(connection)
        return playerid
    return -1

def login(username, password):
    connection = conn.databaseConnection()
    cursor = connection.cursor()
    
    grabpassword = '''
        SELECT p_playerid, p_hashedpassword FROM password
        WHERE p_username = ?
    '''
    
    cursor.execute(grabpassword, (username, ))
    userid, hashedpassword = cursor.fetchone()
    
    if bcrypt.checkpw(password.encode("utf-8"), hashedpassword):
        print("user has successfully logged in")
        return userid
    else: return -1

def updateUserStats(userID, win_or_loss):
    connection = conn.databaseConnection()
    cursor = connection.cursor()

    # Fetch current win/loss count from the database
    cursor.execute("SELECT u_wins, u_losses, u_games FROM user WHERE u_playerid = ?", (userID,))
    user_data = cursor.fetchone()
    
    if user_data:
        # Unpack data
        current_wins, current_losses, current_games = user_data
        
        # Update win or loss count based on the result of the fight
        if win_or_loss == "win":
            new_wins = current_wins + 1
            new_losses = current_losses
        elif win_or_loss == "loss":
            new_wins = current_wins
            new_losses = current_losses + 1
        else:
            # Invalid win/loss result
            return
        
        # Increment the games played count
        new_games = current_games + 1
        
        # Update the database with new values
        cursor.execute("""
            UPDATE user 
            SET u_wins = ?, u_losses = ?, u_games = ? 
            WHERE u_playerid = ?
        """, (new_wins, new_losses, new_games, userID))
        
        # Commit changes
        connection.commit()
        print("User stats updated successfully.")
    else:
        print("User not found in the database.")
    
if __name__ == '__main__':
    selector = input("Select 1 for creating a user, 2 to login as a user:")
    if selector == "1":
        print("currently signing up a user...")
        username = input("please input a username:")
        password = input("please enter a password:")
        print(username, password)
        result = createuser(username, password)
        print(result)
        
    if selector == "2":
        print("currently signing in")
        username = input("please input a username:")
        password = input("please enter a password:")
        result = login(username, password)
        print (result)
        

