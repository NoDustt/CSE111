import database_connection as conn

def createTurn(turnNumber, gameID):
    connection = conn.databaseConnection()
    cursor = connection.cursor()

    turnquery = '''
            INSERT INTO turn(tn_turnnumber, tn_gameid)
            VALUES (?, ?)
        '''
    cursor.execute(turnquery, (turnNumber, gameID))

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