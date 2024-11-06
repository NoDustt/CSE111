import database_connection as conn
import uuid 

def createUnit(unitName, shopID, teamID, level, health, attack):
    connection = conn.databaseConnection()

    cursor = connection.cursor()

    unitid = str(uuid.uuid4())

    unitquery = '''
            INSERT INTO unit(ut_name, ut_unitid, ut_shopid, ut_teamid,
            ut_level, ut_health, ut_attack)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
    
    cursor.execute(unitquery, (unitName, unitid, shopID, teamID, level, health, attack))


    connection.commit()
    conn.closeConnection(connection)

def updateUnit(unitID):
    connection = conn.databaseConnection()
    cursor = connection.cursor()

    updatequery = '''
            UPDATE unit(ut_name, ut_shopid, ut_teamid,
            ut_level, ut_health, ut_attack)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''

    cursor.execute(updatequery, (unitName, shopID, teamID, level, health, attack))

    conn.commit()



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
        print(f"Error deleting unit: {e}")
        connection.rollback()
    finally:
        conn.closeConnection(connection)

    