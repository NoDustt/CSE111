import database_connection as conn
import uuid 
import random

def createTeam(teamName, playerID, teamID, turnnumber, gameID):
    connection = conn.databaseConnection()
    cursor = connection.cursor()

    teamID = str(uuid.uuid4())

    teamquery = '''
            INSERT INTO team(t_teamname, t_teamid, t_playerid, t_turnnumber, t_gameid)
            VALUES (?, ?, ?, ?, ?)
        '''
    cursor.execute(teamquery, (teamName, teamID, playerID, turnnumber, gameID))

    connection.commit()
    conn.closeConnection(connection)
    return teamID

def getPlayerTeamID(playerID, gameID, turnNumber):
    connection = conn.databaseConnection()
    cursor = connection.cursor()
    
    query = '''
        SELECT t_teamid FROM team
        WHERE t_playerid = ?
        AND t_gameid = ?
        AND t_turnNumber = ?
    '''
    teamid = cursor.execute(query, (playerID, gameID, turnNumber)).fetchall()[0][0]
    return teamid

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

def getPlayerTeam(userID, gameID, turnNumber):
    
    connection = conn.databaseConnection()
    cursor = connection.cursor()
    
    query = '''
        SELECT ut_name, ut_health, ut_attack, ut_unitid
        FROM unit
        INNER JOIN team
        ON ut_teamid = t_teamid
        WHERE t_playerid = ?
        AND t_gameid = ?
        AND t_turnnumber = ?
    '''
    
    cursor.execute(query, (userID, gameID, turnNumber))
    
    result = cursor.fetchall()
    print("Your opponents team:")
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
    
def dupeTeams(gameID, turnNumber):
    connection = conn.databaseConnection()
    cursor = connection.cursor()

    query = '''
        SELECT g_player1id, g_player2id
        FROM game
        WHERE g_gameid = ?
    '''
    players = cursor.execute(query,(gameID,)).fetchall()[0]
    newteams = []
    for player in players:
        newteams += [createTeam("New Team", player, 1, turnNumber, gameID)]

    query = '''
        INSERT INTO unit (ut_name, ut_shopid, ut_gold, ut_health, ut_attack, ut_unitid, ut_teamid)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    '''
    unitquery = '''
        SELECT 
        u.ut_name, 
        u.ut_shopid, 
        u.ut_gold, 
        u.ut_health, 
        u.ut_attack
        FROM unit u
        INNER JOIN team t
        ON 
            u.ut_teamid = t.t_teamid
        WHERE 
            t.t_turnnumber = ?
            AND t.t_playerid = ?
            AND t.t_gameid = ?
    '''
    a = 0
    for team in newteams:
        
        units = cursor.execute(unitquery, (turnNumber-1, players[a], gameID)).fetchall()
        for unit in units:
            unitid = str(uuid.uuid4())
            name, shop, cost, health, attack = unit
            cursor.execute(query, (name, shop, cost, health, attack, unitid, team))
            
        a = a+1
    
    connection.commit()
    
    
def printTurnTeams(gameID, userID):
    connection = conn.databaseConnection()
    cursor = connection.cursor()
    print("Printing teams at each turn")
    query = '''
        SELECT  t_turnnumber, ut_name, ut_health, ut_attack FROM team, unit
        WHERE t_gameid = ?
        AND t_playerid = ?
        AND ut_teamid = t_teamid
        ORDER BY t_turnnumber ASC
    '''
    
    userTeams = cursor.execute(query, (gameID, userID)).fetchall()
    print(userTeams)
    
    print("Printing shops at each turn")
    query = '''
        SELECT s_turnnumber, ut_name, ut_health, ut_attack FROM shop, unit
        WHERE s_gameid = ?
        AND s_userid = ?
        AND ut_shopid = s_shopid
        ORDER BY s_turnid ASC
    '''
    
    userTeams = cursor.execute(query, (gameID, userID)).fetchall()
    print(userTeams)