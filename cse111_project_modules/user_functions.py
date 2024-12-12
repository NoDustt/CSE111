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
    
def getwinslosses(userID):
    connection = conn.databaseConnection()
    cursor = connection.cursor()
    
    query = '''
        SELECT u_wins, u_losses, u_games FROM user WHERE u_playerid = ?
    '''
    
    results = cursor.execute(query, (userID,)).fetchall()[0]
    print(f"Wins: {results[0]}\nLosses:{results[1]}\nGames Played: {results[2]}\n")
    conn.closeConnection(connection)
    
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
        

