import database_connection as conn
import uuid 
import random

def createTeam(teamName, playerID, teamID, turnnumber):
    connection = conn.databaseConnection()
    cursor = connection.cursor()

    teamID = str(uuid.uuid4())

    teamquery = '''
            INSERT INTO team(t_teamname, t_teamid, t_playerid, t_turnnumber)
            VALUES (?, ?, ?, ?)
        '''
    cursor.execute(teamquery, (teamName, teamID, playerID, teamID, turnnumber))

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
            SELECT ut_name, ut_health, ut_attack, ut_unitid
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
                'health': u[1], # Third column is unit health
                'attack': u[2],  # Fourth column is unit attack
                'id': u[3] # Firth column is unit id
            }
            team_units.append(unit)  

        for u in team_units:
            print(f"Name: {u['name']}, Health: {u['health']}, Attack: {u['attack']}")


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

def getPlayerTeam(userID, gameID):
    
    connection = conn.databaseConnection()
    cursor = connection.cursor()
    
    query = '''
        SELECT ut_name, ut_health, ut_attack, ut_unitid
        FROM unit
        INNER JOIN team
        ON ut_teamid = t_teamid
        WHERE t_playerid = ?
        AND t_gameid = ?
    '''
    
    cursor.execute(query, (userID, gameID))
    
    result = cursor.fetchall()
    print("Your opponents team")
    team_units = []  

    for u in result:  
        unit = {  
            'name': u[0],   # First column is unit name
            'health': u[1], # Third column is unit health
            'attack': u[2],  # Fourth column is unit attack
            'id': u[3] # Firth column is unit id
        }
        team_units.append(unit)  

    for u in team_units:
        print(f"Name: {u['name']}, Health: {u['health']}, Attack: {u['attack']}")


    return team_units  

def populateTeamWithRandom(userID, gameID, shopID, turnNumber):
    connection = conn.databaseConnection()
    cursor = connection.cursor()
    randint = random.randint(1,4)
    
    query = '''
        SELECT u_unitid
        FROM unit
        WHERE ut_shopid = ?
    '''
    
    cursor.execute(query, (shopID,))
    
    result = cursor.fetchall()
    print(result)
    
# def dupeTeams(gameID, turnNumber):
#     connection = conn.databaseConnection()
#     cursor = connection.cursor()
    
#     query = '''
#         SELECT t_teamid FROM team
#         WHERE t_gameid = ?
#     '''
    
#     teams = cursor.execute(query, (gameID,)).fetchall()[0]
    
#     query = '''
#         SELECT ut_unitid
#         FROM unit
#         WHERE ut_teamid = ?
#     '''
#     for team in teams:
#         units = cursor.execute(query, (team,)).fetchall()[0]
        