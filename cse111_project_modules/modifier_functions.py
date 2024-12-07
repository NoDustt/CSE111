import database_connection as conn
import uuid 

def createModifier(unitID, shopID, effect, modifierName, attribute):
    connection = conn.databaseConnection()

    cursor = connection.cursor()

    modifierID = str(uuid.uuid4())

    modifierquery = '''
        INSERT INTO modifier(m_modifierid, m_unitid, m_shopid, m_effect, m_name, m_attribute)
        VALUES (?, ?, ?, ?, ?, ?)
    '''

    cursor.execute(modifierquery, (modifierID, unitID, shopID, effect, modifierName, attribute))
    connection.commit()
    conn.closeConnection(connection)

def editModifier(modifierID, unitID, shopID, effect, modifierName):
    connection = conn.databaseConnection()

    try:
        cursor = connection.cursor()
        modifierquery = '''
            UPDATE modifier
            SET m_unitid = ?, m_shopid = ?, m_effect = ?, 
                m_name, m_attribute = ?
            WHERE m_modifierid = ?
        '''

        cursor.execute(modifierquery, (unitID, shopID, effect, modifierName))
        connection.commit()

    except Exception as e:
        print(e)
        connection.rollback()

    finally:
        conn.closeConnection(connection)

def deleteModifier(modifierID):
    connection = conn.databaseConnection()
    try:
        cursor = connection.cursor()
        deletequery = '''
            DELETE FROM modifier
            WHERE m_modifierid = ?
        '''
        cursor.execute(deletequery, (modifierID,))
        connection.commit()
    except Exception as e:
        print(e)
        connection.rollback()
    finally:
        conn.closeConnection(connection)

