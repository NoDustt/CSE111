import database_connection as conn
def createTurn(turnNumber, gameID, tn_gold, tn_userid):
    connection = conn.databaseConnection()
    cursor = connection.cursor()

    turnquery = '''
            INSERT INTO turn(tn_turnnumber, tn_gameid, tn_gold, tn_userid)
            VALUES (?, ?, ?, ?)
        '''
    cursor.execute(turnquery, (turnNumber, gameID, tn_gold, tn_userid))

    connection.commit()
    conn.closeConnection(connection)

def editTurn():
    ...

def deleteTurn():
    ...
    
def findLatestTurn(gameID):
    connection = conn.databaseConnection()
    cursor = connection.cursor()
    
    query = '''
        SELECT MAX(tn_turnnumber) FROM turn
        WHERE tn_gameid = ?
    '''
    
    cursor.execute(query, (gameID,))
    
    results = cursor.fetchall()
    
    return results

def getGold(gameID, turnNumber):
    connection = conn.databaseConnection()
    cursor = connection.cursor()
    
    query = '''
        SELECT tn_gold FROM turn
        WHERE tn_gameID = ?
        AND tn_turnnumber = ?
    '''
    
    cursor.execute(query, (gameID, turnNumber))
    
    results = cursor.fetchall()
    
    return results

def incrementTurn(gameID, turnNumber):
    gold = max(3, turnNumber)
    connection = conn.databaseConnection()
    cursor = connection.cursor()
    query = '''
        SELECT g_player1id, g_player2id
        FROM game
        WHERE g_gameid = ?
    '''
    players = cursor.execute(query,(gameID,)).fetchall()[0]
    
    if not players:
        print("Failed to increment turn")
        
    query = '''
        INSERT INTO turn(tn_turnnumber, tn_gameid, tn_gold, tn_userid)
        VALUES (?, ?, ?, ?)
    '''
    
    for player in players:
        cursor.execute(query, (turnNumber, gameID, gold, player))
    
    connection.commit()
    conn.closeConnection(connection)