# import database_connection as conn
# import uuid 
# import bcrypt
# #file for all relelvant user function
# def createuser(username, password):
#     connection = conn.databaseConnection()
    
#     cursor = connection.cursor()
    
#     playerid = str(uuid.uuid4())
    
#     checkusername = '''
#         SELECT * FROM user
#         WHERE u_username = ?  
#     '''
#     cursor.execute(checkusername, (username,))
#     result = cursor.fetchall()
#     if result == []:
        
#         userquery = '''
#             INSERT INTO user(u_username, u_playerid)
#             VALUES (?, ?)
#         '''
        
#         values = (username, playerid)
#         cursor.execute(userquery, values)
#         connection.commit()
#         salt = bcrypt.gensalt()
#         hashedpassword = bcrypt.hashpw(password.encode("utf-8"), salt)
        
#         passwordquery = '''
#             INSERT INTO password(p_username, p_playerid, p_hashedpassword, p_salt)
#             VALUES (?, ?, ?, ?)
#         '''
        
#         cursor.execute(passwordquery, (username, playerid, hashedpassword, salt))
        
#         connection.commit()
#         conn.closeConnection(connection)
#         return playerid
#     return "user already exists"

# def login(username, password):
#     connection = conn.databaseConnection()
#     cursor = connection.cursor()
    
    
#     grabpassword = '''
#         SELECT p_hashedpassword FROM password
#         WHERE p_username = ?
#     '''
    
#     cursor.execute( )
    
# if __name__ == '__main__':
#     a = createuser("c", "password")
#     print(a)