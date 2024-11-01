import sqlite3
from sqlite3 import Error

usertable = '''
    CREATE TABLE IF NOT EXISTS user(
        u_username VARCHAR(255) NOT NULL,
        u_playerid VARCHAR(255) NOT NULL,
        PRIMARY KEY (u_playerid)
    )
'''

dropusertable = '''
    DROP TABLE IF EXISTS user
'''

passwordtable = '''
    CREATE TABLE IF NOT EXISTS password(
        p_username VARCHAR(255) NOT NULL,
        p_playerid VARCHAR(255) NOT NULL,
        p_hashedpassword VARCHAR(255) NOT NULL,
        p_salt VARCHAR(255) NOT NULL,
        
        FOREIGN KEY (p_playerid) REFERENCES user(u_playerid)
    )   
'''

droppasswordtable = '''
    DROP TABLE IF EXISTS password
'''

teamtable = '''
    CREATE TABLE IF NOT EXISTS team(
        t_teamname VARCHAR(255) NOT NULL,
        t_teamid VARCHAR(255) NOT NULL,
        t_playerid VARCHAR(255) NOT NULL,
        
        PRIMARY KEY (t_teamid),
        FOREIGN KEY (t_playerid) REFERENCES user(u_playerid)
    )
'''

dropteamtable = '''
    DROP TABLE IF EXISTS team
'''

gametable = '''
    CREATE TABLE IF NOT EXISTS game(
        g_gameid VARCHAR(255) NOT NULL,
        g_player1id VARCHAR(255) NOT NULL,
        g_player2id VARCHAR(255) NOT NULL,
        
        PRIMARY KEY (g_gameid),
        FOREIGN KEY (g_player1id) REFERENCES user(u_playerid),
        FOREIGN KEY (g_player2id) REFERENCES user(u_playerid)
    )    
'''

dropgametable = '''
    DROP TABLE IF EXISTS game
'''

turntable = '''
    CREATE TABLE IF NOT EXISTS turn(
        tn_turnnumber VARCHAR(255) NOT NULL,
        tn_gameid VARCHAR(255) NOT NULL,
        
        FOREIGN KEY (tn_gameid) REFERENCES game(g_gameid)
    )
'''

dropturntable = '''
    DROP TABLE IF EXISTS turn
'''

shoptable = '''
    CREATE TABLE IF NOT EXISTS shop(
        s_shopid VARCHAR(255) NOT NULL,
        s_gameid VARCHAR(255) NOT NULL,
        
        PRIMARY KEY (s_shopid),
        FOREIGN KEY (s_gameid) REFERENCES shop(s_gameid)
    )
'''

dropshoptable = '''
    DROP TABLE IF EXISTS shop
'''

unittable = '''
    CREATE TABLE IF NOT EXISTS unit(
        ut_name VARCHAR(255) NOT NULL, 
        ut_unitid VARCHAR(255) NOT NULL,
        ut_shopid VARCHAR(255) NOT NULL,
        ut_teamid VARCHAR(255) NOT NULL,
        ut_level VARCHAR(255) NOT NULL,
        
        PRIMARY KEY (ut_unitid),
        FOREIGN KEY (ut_shopid) REFERENCES shop(s_shopid),
        FOREIGN KEY (ut_teamid) REFERENCES team(t_teamid)
    )
'''

dropunittable = '''
    DROP TABLE IF EXISTS unit
'''

modifiertable = '''
    CREATE TABLE IF NOT EXISTS modifier(
        m_modifierid VARCHAR(255) NOT NULL,
        m_unitid VARCHAR(255) NOT NULL,
        m_shopid VARCHAR(255) NOT NULL,
        m_effect VARCHAR(255) NOT NULL,
        m_name VARCHAR(255) NOT NULL,
        
        PRIMARY KEY (m_modifierid),
        FOREIGN KEY (m_unitid) REFERENCES unit(ut_unitid),
        FOREIGN KEY (m_shopid) REFERENCES shop(s_shopid)
    )
'''
dropmodifiertable = '''
    DROP TABLE IF EXISTS modifier
'''

createtables = [usertable, passwordtable, teamtable, gametable, turntable, shoptable, unittable, modifiertable]
droptables = [dropmodifiertable, dropunittable, dropshoptable, dropturntable, dropgametable, dropteamtable, droppasswordtable, dropusertable]

def databaseConnection(database):
    connection = None
    try:
        connection = sqlite3.connect(database)
        return connection
    except Error as e:
        print(e)
    
    
def closeConnection(connection):
    try:
        connection.close()
    except Error as e:
        print(e)

def dropAllTables(connection):
    cursor = connection.cursor()
    for query in droptables:
        cursor.execute(query)

def createAllTables(connection):
    cursor = connection.cursor()
    
    for query in createtables:
        cursor.execute(query)

def databaseReset():
    database = r"cse111_project.sqlite"
    connection = databaseConnection(database)
    with connection:
        dropAllTables(connection)
        createAllTables(connection)
    closeConnection(connection)
    
if __name__ == '__main__':
    databaseReset()