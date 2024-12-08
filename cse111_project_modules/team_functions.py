import database_connection as conn
import uuid 

def createTeam(teamName, playerID, teamID):
    connection = conn.databaseConnection()
    cursor = connection.cursor()

    teamID = str(uuid.uuid4())

    teamquery = '''
            INSERT INTO team(t_teamname, t_teamid, t_playerid)
            VALUES (?, ?, ?)
        '''
    cursor.execute(teamquery, (teamName, teamID, playerID, teamID))

    connection.commit()
    conn.closeConnection(connection)
    return teamID

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


def getTeam(teamID):
    connection = conn.databaseConnection()  
    try:
        cursor = connection.cursor()  
        getTeamquery = '''
            SELECT ut_name, ut_level, ut_health, ut_attack, ut_unitid
            FROM unit
            WHERE ut_teamid = ?
        '''  
        cursor.execute(getTeamquery, (teamID,))  
        result = cursor.fetchall()  

        print("Your current team:")  
        team_units = []  

        for u in result:  
            unit = {  
                'name': u[0],   # First column is unit name
                'level': u[1],  # Second column is unit level
                'health': u[2], # Third column is unit health
                'attack': u[3],  # Fourth column is unit attack
                'id': u[4] # Firth column is unit id
            }
            team_units.append(unit)  

        for u in team_units:
            print(f"Name: {u['name']}, Level: {u['level']}, Health: {u['health']}, Attack: {u['attack']}")


        return team_units  
    except Exception as e: 
        print(f"Error fetching units for team {teamID}: {e}")  
        connection.rollback()  
        return []  
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

