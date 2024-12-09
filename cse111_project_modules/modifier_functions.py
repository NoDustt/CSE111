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
    cursor = connection.cursor()

    try:
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

def findModifier(shopID):
    connection = conn.databaseConnection()
    cursor = connection.cursor()

    try:
        findModifierQuery = '''
            SELECT m_modifierid, m_name, m_effect, m_attribute
            FROM modifier
            WHERE m_shopid = ?
        '''
        cursor.execute(findModifierQuery, (shopID,))
        return cursor.fetchall()
    except Exception as e:
        print(e)
        connection.rollback()
    finally:
        conn.closeConnection(connection)

def applyModifier(unitID, effect, attribute):
    connection = conn.databaseConnection()
    cursor = connection.cursor()

    try:
        cursor = connection.cursor()
        if attribute == "HEALTH":
            applyquery = '''
                UPDATE unit
                SET ut_health = ut_health + ?
                WHERE ut_unitid = ?
        '''
        elif attribute == "ATTACK":
            applyquery = '''
                UPDATE unit
                SET ut_attack = ut_attack + ?
                WHERE ut_unitid = ?
        '''
        else:
                print(f"Invalid attribute: {attribute}")
                return

        cursor.execute(applyquery, (effect, unitID))
        connection.commit()
        print(f"Applied {effect} to {attribute} for unit {unitID}.")

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


