import database_connection as conn
import uuid 
import random

def createGame(player1ID, player2ID):
    connection = conn.databaseConnection()
    cursor = connection.cursor()
    
    gameID = str(uuid.uuid4())

    gamequery = '''
            INSERT INTO game(g_gameID, g_player1id, g_player2id)
            VALUES (?, ?, ?)
        '''
    cursor.execute(gamequery, (gameID, player1ID, player2ID))
    turnquery = '''
            INSERT INTO turn(tn_turnnumber, tn_gameid, tn_userid)
            VALUES (?, ?, ?)
        '''
    cursor.execute(turnquery, (1, gameID, player2ID))
    cursor.execute(turnquery, (1, gameID, player1ID))
    teamID = str(uuid.uuid4())

    teamquery = '''
            INSERT INTO team(t_teamname, t_teamid, t_playerid, t_turnnumber, t_gameid)
            VALUES (?, ?, ?, ?, ?)
        '''
    cursor.execute(teamquery, ("New Team", teamID, player2ID, 1, gameID))
    teamID = str(uuid.uuid4())
    cursor.execute(teamquery, ("New Team", teamID, player1ID, 1, gameID))
    
    shopID = str(uuid.uuid4())

    shopquery = '''
        INSERT INTO shop(s_shopid, s_gameid, s_turnid, s_userid)
        VALUES(?,?,?,?)
    '''

    cursor.execute(shopquery, (shopID, gameID, 1, player1ID))
    
    
    unitquery = '''
        INSERT INTO unit(ut_name, ut_unitid, ut_shopid, ut_teamid,
                         ut_gold, ut_health, ut_attack)
        VALUES (?, ?, ?, NULL, ?, ?, ?)
    '''
    sample_units = [
    ("Warrior", "1", "100", "15"),
    ("Archer", "1", "80", "20"),
    ("Mage", "1", "70", "25"),
    ("Knight", "1", "120", "10"),
    ("Berserker", "1", "150", "30"),
    ("Rogue", "1", "90", "18"),
    ("Paladin", "1", "110", "12"),
    ("Wizard", "1", "60", "22"),
    ("Assassin", "1", "80", "25"),
    ("Priest", "1", "50", "10"),
    ("Gladiator", "1", "130", "20"),
    ("Shaman", "1", "75", "15"),
    ("Tank", "1", "160", "5"),
    ("Sniper", "1", "85", "30"),
    ("Sorcerer", "1", "95", "28"),
    ("Defender", "1", "120", "8"),
    ("Beastmaster", "1", "140", "22"),
    ("Druid", "1", "85", "18"),
    ("Hunter", "1", "100", "20"),
    ("Knight Captain", "1", "150", "25"),
    ("Witch", "1", "60", "15"),
    ("Barbarian", "1", "140", "35"),
    ("Templar", "1", "110", "16"),
    ("Vampire", "1", "90", "24"),
    ("Elementalist", "1", "80", "20"),
    ("Monk", "1", "110", "12"),
    ("Dragon Rider", "1", "180", "30"),
    ("Dark Knight", "1", "160", "15"),
    ("Centurion", "1", "130", "18"),
    ("Necromancer", "1", "70", "15"),
    ("Warlock", "1", "95", "25"),
    ("Guardian", "1", "100", "20"),
    ("Lightbringer", "1", "120", "10"),
    ("Giant", "1", "200", "40"),
    ("Gunslinger", "1", "90", "25"),
    ("Reaper", "1", "85", "28"),
    ("Samurai", "1", "120", "30"),
    ("Ranger", "1", "100", "22"),
    ("Ninja", "1", "80", "27"),
    ("Stormbringer", "1", "110", "18"),
    ("Dark Mage", "1", "70", "20"),
    ("Fighter", "1", "100", "15"),
    ("Sorceress", "1", "85", "18"),
    ("Cavalier", "1", "130", "22"),
    ("Bounty Hunter", "1", "95", "25"),
    ("Golem", "1", "150", "5"),
    ("Paladin Knight", "1", "140", "18"),
    ("Demon Hunter", "1", "120", "20"),
    ("Arbalist", "1", "90", "28")
    ]

    randomunits = random.sample(sample_units, 4)
    for unit in randomunits:
        unitid = str(uuid.uuid4())
        unitName, gold, health, attack = unit
        cursor.execute(unitquery, (unitName, unitid, shopID, gold, health, attack))


    modifierquery = '''
        INSERT INTO modifier(m_modifierid, m_unitid, m_shopid, m_effect, m_name, m_attribute, m_cost)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    '''

    sample_modifiers = [
    ("Health Boost I", 10, "HEALTH", 2),
    ("Attack Boost I", 10, "ATTACK", 2),
    ("Health Boost II", 20, "HEALTH", 3),
    ("Attack Boost II", 20, "ATTACK", 3),
    ("Health Boost III", 30, "HEALTH", 5),
    ("Attack Boost III", 30, "ATTACK", 5),
    ]

    randommodifiers = random.sample(sample_modifiers, 3)
    for modifier in randommodifiers:
        modifierID = str(uuid.uuid4())
        modifierName, effect, attribute, cost= modifier
        cursor.execute(modifierquery, (modifierID, unitid, shopID, effect, modifierName, attribute, cost))

    shopID = str(uuid.uuid4())
    cursor.execute(shopquery, (shopID, gameID, 1, player2ID))
    randomunits = random.sample(sample_units, 4)
    for unit in randomunits:
        unitid = str(uuid.uuid4())
        unitName, gold, health, attack = unit
        cursor.execute(unitquery, (unitName, unitid, shopID, gold, health, attack))
    randommodifiers = random.sample(sample_modifiers, 3)
    for modifier in randommodifiers:
        modifierID = str(uuid.uuid4())
        modifierName, effect, attribute, cost= modifier
        cursor.execute(modifierquery, (modifierID, unitid, shopID, effect, modifierName, attribute, cost))
    connection.commit()
    
    conn.closeConnection(connection)
    return gameID, shopID, teamID

def editGame(gameID, player1ID, player2ID):
    connection = conn.databaseConnection()
    try:
        cursor = connection.cursor()
        updatequery = '''
            UPDATE game
            SET g_player1id = ?, g_player2id = ?
            WHERE g_gameid = ?
        '''

        cursor.execute(updatequery, (player1ID, player2ID))
        connection.commit()

    except Exception as e:
        print(e)
        connection.rollback()

    finally:
        conn.closeConnection(connection)


def deleteGame(gameID):
    connection = conn.databaseConnection()
    try:
        cursor = connection.cursor()
        deletequery = '''
            DELETE FROM game
            WHERE g_gameid = ?
        '''
        cursor.execute(deletequery, (gameID,))

        connection.commit()
    except Exception as e:
        print(e)
        connection.rollback()
    finally:
        conn.closeConnection(connection)

def findUserGames(userid):
    connection = conn.databaseConnection()
    cursor = connection.cursor()
    findquery = '''
        SELECT g_gameid, u_username
        FROM game, user
        WHERE g_player1id = ?
        AND u_playerid != ?
        OR g_player2id = ?
    '''
    cursor.execute(findquery, (userid, userid, userid))
    results = cursor.fetchall()
    return results


def getGameHistory(gameid):
    connection = conn.databaseConnection()
    cursor = connection.cursor()
    
    