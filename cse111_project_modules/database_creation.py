import database_connection as conn
usertable = '''
    CREATE TABLE IF NOT EXISTS user(
        u_username VARCHAR(255) NOT NULL,
        u_playerid VARCHAR(255) NOT NULL,
        u_wins VARCHAR(255) DEFAULT 0,
        u_losses VARCHAR(255) DEFAULT 0,
        u_games VARCHAR(255) DEFAULT 0,
        PRIMARY KEY (u_playerid, u_username)
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
        
        FOREIGN KEY (p_playerid) REFERENCES user(u_playerid) ON DELETE CASCADE
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
        t_turnnumber VARCHAR(255) NOT NULL,
        t_gameid VARCHAR(255) NOT NULL,
        
        PRIMARY KEY (t_teamid),
        FOREIGN KEY (t_playerid) REFERENCES user(u_playerid) ON DELETE CASCADE,
        FOREIGN KEY (t_turnnumber) REFERENCES turn(tn_turnnumber) ON DELETE CASCADE,
        FOREIGN KEY (t_gameid) REFERENCES game(g_gameid) ON DELETE CASCADE
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
        FOREIGN KEY (g_player1id) REFERENCES user(u_playerid) ON DELETE CASCADE,
        FOREIGN KEY (g_player2id) REFERENCES user(u_playerid) ON DELETE CASCADE
    )    
'''

dropgametable = '''
    DROP TABLE IF EXISTS game
'''

turntable = '''
    CREATE TABLE IF NOT EXISTS turn(
        tn_turnnumber VARCHAR(255) NOT NULL,
        tn_gameid VARCHAR(255) NOT NULL,
        tn_gold VARCHAR(255) DEFAULT 3,
        FOREIGN KEY (tn_gameid) REFERENCES game(g_gameid) ON DELETE CASCADE
    )
'''

dropturntable = '''
    DROP TABLE IF EXISTS turn
'''

shoptable = '''
    CREATE TABLE IF NOT EXISTS shop(
        s_shopid VARCHAR(255) NOT NULL,
        s_gameid VARCHAR(255) NOT NULL,
        s_turnid VARCHAR(255) NOT NULL,
        PRIMARY KEY (s_shopid),
        FOREIGN KEY (s_gameid) REFERENCES game(g_gameid) ON DELETE CASCADE,
        FOREIGN KEY (s_turnid) REFERENCES turn(tn_turnid) ON DELETE CASCADE
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
        ut_teamid VARCHAR(255),
        ut_gold VARCHAR(255) NOT NULL,
        ut_health VARCHAR(255) NOT NULL,
        ut_attack VARCHAR(255) NOT NULL,
        
        PRIMARY KEY (ut_unitid),
        FOREIGN KEY (ut_shopid) REFERENCES shop(s_shopid) ON DELETE CASCADE,
        FOREIGN KEY (ut_teamid) REFERENCES team(t_teamid) ON DELETE CASCADE
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
        m_effect INT NOT NULL,
        m_name VARCHAR(255) NOT NULL,
        m_attribute TEXT NOT NULL, 
        
        PRIMARY KEY (m_modifierid),
        FOREIGN KEY (m_unitid) REFERENCES unit(ut_unitid) ON DELETE CASCADE,
        FOREIGN KEY (m_shopid) REFERENCES shop(s_shopid) ON DELETE CASCADE
    )
'''
dropmodifiertable = '''
    DROP TABLE IF EXISTS modifier
'''

createtables = [usertable, passwordtable, teamtable, gametable, turntable, shoptable, unittable, modifiertable]
droptables = [dropmodifiertable, dropunittable, dropshoptable, dropturntable, dropgametable, dropteamtable, droppasswordtable, dropusertable]
    
def dropAllTables(connection):
    cursor = connection.cursor()
    for query in droptables:
        cursor.execute(query)

def createAllTables(connection):
    
    cursor = connection.cursor()
    
    for query in createtables:
        cursor.execute(query)

def databaseReset():
    connection = conn.databaseConnection()
    with connection:
        dropAllTables(connection)
        createAllTables(connection)
    conn.closeConnection(connection)
    
if __name__ == '__main__':
    databaseReset()