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
            INSERT INTO turn(tn_turnnumber, tn_gameid, tn_userid)
            VALUES (?, ?, ?)
        '''
    cursor.execute(turnquery, (1, gameID, player1ID))
    cursor.execute(turnquery, (1, gameID, player2ID))
    teamID = str(uuid.uuid4())

    teamquery = '''
            INSERT INTO team(t_teamname, t_teamid, t_playerid, t_turnnumber, t_gameid)
            VALUES (?, ?, ?, ?, ?)
        '''
    cursor.execute(teamquery, ("New Team", teamID, player1ID, 1, gameID))
    teamID = str(uuid.uuid4())
    cursor.execute(teamquery, ("New Team", teamID, player2ID, 1, gameID))
    
    shopID = str(uuid.uuid4())

    shopquery = '''
        INSERT INTO shop(s_shopid, s_gameid, s_turnid)
        VALUES(?,?,?)
    '''

    cursor.execute(shopquery, (shopID, gameID, 1))
    
    unitquery = '''
        INSERT INTO unit(ut_name, ut_unitid, ut_shopid, ut_teamid,
                         ut_gold, ut_health, ut_attack)
        VALUES (?, ?, ?, NULL, ?, ?, ?)
    '''
    sample_units = [
        ("Warrior", "1", "100", "15"),
        ("Archer", "1", "80", "20"),
        ("Mage", "1", "70", "25"),
        ("Knight", "1", "120", "10"),
    ]
    for unit in sample_units:
        unitid = str(uuid.uuid4())
        unitName, gold, health, attack = unit
        cursor.execute(unitquery, (unitName, unitid, shopID, gold, health, attack))


    modifierquery = '''
        INSERT INTO modifier(m_modifierid, m_unitid, m_shopid, m_effect, m_name, m_attribute)
        VALUES (?, ?, ?, ?, ?, ?)
    '''

    sample_modifiers = [
    ("Health Boost I", 10, "HEALTH"),
    ("Attack Boost I", 10, "ATTACK"),
    ("Health Boost II", 20, "HEALTH"),
    ("Attack Boost II", 20, "ATTACK"),
]

    for modifier in sample_modifiers:
        modifierID = str(uuid.uuid4())
        modifierName, effect, attribute = modifier
        cursor.execute(modifierquery, (modifierID, unitid, shopID, effect, modifierName, attribute))

        
    connection.commit()
    
    conn.closeConnection(connection)
    return gameID, shopID, teamID

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

def findUserGamers(userid):
    connection = conn.databaseConnection()
    cursor = connection.cursor()
    findquery = '''
        SELECT g_gameid
        FROM game
        WHERE g_player1id = ?
        OR g_player2id = ?
    '''
    cursor.execute(findquery, (userid, userid))
    results = cursor.fetchall()
    return results


def getGameHistory(gameid):
    connection = conn.databaseConnection()
    cursor = connection.cursor()
    
    