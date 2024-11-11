import database_connection as conn

def createTurn(turnNumber, gameID):
    connection = conn.databaseConnection()
    cursor = connection.cursor()

    turnquery = '''
            INSERT INTO game(tn_turnnumber, tn_gameid)
            VALUES (?, ?)
        '''
    cursor.execute(turnquery, (turnNumber, gameID))

    connection.commit()
    conn.closeConnection(connection)

def editTurn():
    ...

def deleteTeam():
    ...