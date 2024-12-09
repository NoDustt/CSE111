import database_connection as conn
import uuid 

def createShop(gameID, turnID):
    connection = conn.databaseConnection()
    cursor = connection.cursor()

    shopid = str(uuid.uuid4())

    shopquery = '''
        INSERT INTO shop(s_shopid, s_gameid, s_turnid)
        VALUES(?,?,?)
    '''

    cursor.execute(shopquery, (shopid, gameID, turnID))
    connection.commit()
    conn.closeConnection(connection)

def editShop(shopID, shop):
    ...

def deleteShop(shopID):
    connection = conn.databaseConnection()
    cursor = connection.cursor()
    try:
        cursor = connection.cursor()
        deletequery = '''
            DELETE FROM shop
            WHERE s_shopid = ?
        '''
        cursor.execute(deletequery, (shopID,))
        connection.commit()
    except Exception as e:
        print(f"Error deleting unit: {e}")
        connection.rollback()
    finally:
        conn.closeConnection(connection)

def findShop(gameID):
    connection = conn.databaseConnection()
    cursor = connection.cursor()
    try:
        cursor = connection.cursor()
        findshop = '''
            SELECT s_shopid FROM shop
            WHERE s_gameid = ?
        '''
        cursor.execute(findshop, (gameID,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error deleting unit: {e}")
        connection.rollback()
    finally:
        conn.closeConnection(connection)
            