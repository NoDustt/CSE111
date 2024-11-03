import database_connection as conn
import uuid 

def createUnit(modifierName, modifierID, unitID):
    connection = conn.databaseConnection()

    cursor = connection.cursor()

    unitid = str(uuid.uuid4())

    unitquery = '''
            INSERT INTO unit(ut_name, ut_unitid, ut_shopid, ut_teamid,
            ut_level, ut_health,ut_attack)
            VALUES (?, ?, ?, ?)
        '''
    
    cursor.execute(unitquery, ())

    connection.commit()
    conn.closeConnection(connection)
