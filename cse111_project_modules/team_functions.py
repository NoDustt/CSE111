import database_connection as conn
import uuid 

def createTeam(teamName, playerID):
    connection = conn.databaseConnection()
    cursor = connection.cursor()

    teamID = str(uuid.uuid4())

    teamquery = '''
            INSERT INTO team(t_teamname, t_teamid, t_playerid)
            VALUES (?, ?, ?)
        '''
    cursor.execute(teamquery, (teamName, teamID, playerID))

    connection.commit()
    conn.closeConnection(connection)

def editTeam(teamID, teamName, playerID):
    connection = conn.databaseConnection()
    try:
        cursor = connection.cursor()
        updatequery = '''
            UPDATE team
            SET t_teamname = ?, t_teamid = ?
            WHERE t_teamid = ?
        '''

        cursor.execute(updatequery, (teamName, playerID))
        connection.commit()

    except Exception as e:
        print(e)
        connection.rollback()

    finally:
        conn.closeConnection(connection)

def deleteTeam(teamID):
    connection = conn.databaseConnection()
    try:
        cursor = connection.cursor()
        deletequery = '''
            DELETE FROM team
            WHERE t_teamid = ?
        '''
        cursor.execute(deletequery, (teamID,))
        connection.commit()
    except Exception as e:
        print(e)
        connection.rollback()
    finally:
        conn.closeConnection(connection)

