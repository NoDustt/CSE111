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
    
    shopid = str(uuid.uuid4())

    shopquery = '''
        INSERT INTO shop(s_shopid, s_gameid)
        VALUES(?,?)
    '''

    cursor.execute(shopquery, (shopid, gameID))
    
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
