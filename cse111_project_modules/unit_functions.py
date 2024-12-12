import database_connection as conn
import uuid 

def createUnit(unitName, shopID, teamID, gold, health, attack):
    connection = conn.databaseConnection()

    cursor = connection.cursor()

    unitid = str(uuid.uuid4())

    unitquery = '''
            INSERT INTO unit(ut_name, ut_unitid, ut_shopid, ut_teamid,
            ut_gold, ut_health, ut_attack)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
    
    cursor.execute(unitquery, (unitName, unitid, shopID, teamID, gold, health, attack))


    connection.commit()
    conn.closeConnection(connection)
    return unitid

def updateUnit(unitID, unitName, shopID, teamID, gold, health, attack):
    connection = conn.databaseConnection()

    try:
        cursor = connection.cursor()
        updatequery = '''
            UPDATE unit
            SET ut_name = ?, ut_shopid = ?, ut_teamid = ?, 
                ut_gold = ?, ut_health = ?, ut_attack = ?
            WHERE ut_unitid = ?
        '''

        cursor.execute(updatequery, (unitName, shopID, teamID, gold, health, attack, unitID))
        connection.commit()

    except Exception as e:
        print(e)
        connection.rollback()

    finally:
        conn.closeConnection(connection)


def findUnit(shopID, gold):
    connection = conn.databaseConnection()
    cursor = connection.cursor()
    try:
        
        cursor = connection.cursor()
        
        findUnitQuery = '''
            SELECT ut_unitid, ut_name, ut_gold, ut_health, ut_attack FROM unit
            WHERE ut_shopid = ?
            AND ut_teamid IS NULL
            AND ut_gold <= ?
        '''
        cursor.execute(findUnitQuery, (shopID, gold))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error deleting unit: {e}")
        connection.rollback()
    finally:
        conn.closeConnection(connection)

def addUnitToTeam(teamID, unitID, gameID, userID, turnnumber):
    connection = conn.databaseConnection()
    cursor = connection.cursor()
    try:
        update_unit_query = '''
            UPDATE unit
            SET ut_teamid = ?
            WHERE ut_unitid = ?
        '''
        cursor.execute(update_unit_query, (teamID, unitID))
        connection.commit()
        
        cost_query = '''
            SELECT ut_gold FROM unit WHERE ut_unitid = ?
        '''
        cost = int(cursor.execute(cost_query, (unitID,)).fetchone()[0][0])
        
        update_team_query = '''
            UPDATE turn
            SET tn_gold = tn_gold - ?
            WHERE tn_gameid = ?
            AND tn_userid = ?
            AND tn_turnnumber = ?
        '''
        cursor.execute(update_team_query, (cost, gameID, userID, turnnumber))
        connection.commit()
        # print(f"Unit {unitID} successfully assigned to Team {teamID}.")
    except Exception as e:
        print(f"Error assigning unit to team: {e}")
        connection.rollback()
    finally:
        conn.closeConnection(connection)

def deleteUnit(unitID):
    connection = conn.databaseConnection()
    try:
        cursor = connection.cursor()
        deletequery = '''
            DELETE FROM unit
            WHERE ut_unitid = ?
        '''
        cursor.execute(deletequery, (unitID,))
        connection.commit()
    except Exception as e:
        print(e)
        connection.rollback()
    finally:
        conn.closeConnection(connection)


def createBotTeam(gameID, turnNumber):
    connection = conn.databaseConnection()
    cursor = connection.cursor()
    
