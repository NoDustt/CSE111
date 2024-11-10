import database_connection as conn
import uuid 

def createShop(gameID):
    connection = conn.databaseConnection()
    cursor = connection.cursor()

    shopid = str(uuid.uuid4())

    shopquery = '''
        INSERT INTO shop(s_shopid, s_gameid)
        VALUES(shopid,?)
    '''

    cursor.execute(shopquery, (shopid, gameID))
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

def findShop(shopID):
    ...