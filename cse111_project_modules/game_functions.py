import database_connection as conn
import uuid 

def createGame(player1ID, player2ID):
    connection = conn.databaseConnection()
    cursor = connection.cursor()
    
    gameID = str(uuid.uuid4())

    gamequery = '''
            INSERT INTO game(g_gameID, g_player1id, g_player2id)
            VALUES (?, ?, ?)
        '''
    cursor.execute(gamequery, (gameID, player1ID, player2ID))
    turnquery = '''
            INSERT INTO turn(tn_turnnumber, tn_gameid)
            VALUES (?, ?)
        '''
    cursor.execute(turnquery, (1, gameID))
    
    teamID = str(uuid.uuid4())

    teamquery = '''
            INSERT INTO team(t_teamname, t_teamid, t_playerid)
            VALUES (?, ?, ?)
        '''
    cursor.execute(teamquery, ("New Team", teamID, player1ID))
    teamID = str(uuid.uuid4())
    cursor.execute(teamquery, ("New Team", teamID, player2ID))
    
    shopID = str(uuid.uuid4())

    shopquery = '''
        INSERT INTO shop(s_shopid, s_gameid)
        VALUES(?,?)
    '''

    cursor.execute(shopquery, (shopID, gameID))
    
    unitquery = '''
            INSERT INTO unit(ut_name, ut_unitid, ut_shopid, ut_teamid,
            ut_level, ut_health, ut_attack)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        
    sample_units = [
        ("Warrior", "1", "100", "15"),
        ("Archer", "1", "80", "20"),
        ("Mage", "1", "70", "25"),
        ("Knight", "1", "120", "10"),
        ("Healer", "1", "90", "5"),
    ]
    for unit in sample_units:
        unitid = str(uuid.uuid4())
        unitName, level, health, attack = unit
        cursor.execute(unitquery, (unitName, unitid, shopID, teamID, level, health, attack))
        
    connection.commit()
    
    conn.closeConnection(connection)
    return gameID

def editGame(gameID, player1ID, player2ID):
    connection = conn.databaseConnection()
    try:
        cursor = connection.cursor()
        updatequery = '''
            UPDATE game
            SET g_player1id = ?, g_player2id = ?
            WHERE g_gameid = ?
        '''

        cursor.execute(updatequery, (player1ID, player2ID))
        connection.commit()

    except Exception as e:
        print(e)
        connection.rollback()

    finally:
        conn.closeConnection(connection)


def deleteGame(gameID):
    connection = conn.databaseConnection()
    try:
        cursor = connection.cursor()
        deletequery = '''
            DELETE FROM game
            WHERE g_gameid = ?
        '''
        cursor.execute(deletequery, (gameID,))

        connection.commit()
    except Exception as e:
        print(e)
        connection.rollback()
    finally:
        conn.closeConnection(connection)
