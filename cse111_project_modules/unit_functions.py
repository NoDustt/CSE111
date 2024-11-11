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

def updateUnit(unitID, unitName, shopID, teamID, level, health, attack):
    connection = conn.databaseConnection()

    try:
        cursor = connection.cursor()
        updatequery = '''
            UPDATE unit
            SET ut_name = ?, ut_shopid = ?, ut_teamid = ?, 
                ut_level = ?, ut_health = ?, ut_attack = ?
            WHERE ut_unitid = ?
        '''

        cursor.execute(updatequery, (unitName, shopID, teamID, level, health, attack, unitID))
        connection.commit()

    except Exception as e:
        print(e)
        connection.rollback()

    finally:
        conn.closeConnection(connection)


def findUnit():
    ...

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



    