import database_connection as conn
import uuid 

def createShop(gameID, turnID, userID):
    connection = conn.databaseConnection()
    cursor = connection.cursor()

    shopid = str(uuid.uuid4())

    shopquery = '''
        INSERT INTO shop(s_shopid, s_gameid, s_turnid, s_userid)
        VALUES(?,?,?,?)
    '''

    cursor.execute(shopquery, (shopid, gameID, turnID, userID))
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
        return cursor.fetchall()
    except Exception as e:
        print(f"Error deleting unit: {e}")
        connection.rollback()
    finally:
        conn.closeConnection(connection)
        
        
def genNewShops(gameID, turnNumber):
    connection = conn.databaseConnection()
    cursor = connection.cursor()
    query = '''
        SELECT g_player1id, g_player2id
        FROM game
        WHERE g_gameid = ?
    '''
    players = cursor.execute(query,(gameID,)).fetchall()[0]
    
    if not players:
        print("Failed to increment turn")
    
    shopquery = '''
        INSERT INTO shop(s_shopid, s_gameid, s_turnid, s_userid)
        VALUES(?,?,?,?)
    '''

    
    
    for player in players:
        shopid = str(uuid.uuid4())
        cursor.execute(shopquery, (shopid, gameID, turnNumber, player))
    
    connection.commit()
    conn.closeConnection(connection)