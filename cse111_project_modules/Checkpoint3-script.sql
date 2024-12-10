DROP TABLE IF EXISTS modifier;
DROP TABLE IF EXISTS unit;
DROP TABLE IF EXISTS shop;
DROP TABLE IF EXISTS turn;
DROP TABLE IF EXISTS game;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS password;
DROP TABLE IF EXISTS user;

CREATE TABLE IF NOT EXISTS user(
        u_username VARCHAR(255) NOT NULL,
        u_playerid VARCHAR(255) NOT NULL,
        u_wins VARCHAR(255) DEFAULT 0,
        u_losses VARCHAR(255) DEFAULT 0,
        u_games VARCHAR(255) DEFAULT 0,
        PRIMARY KEY (u_playerid, u_username)
);

CREATE TABLE IF NOT EXISTS password (
    p_username VARCHAR(255) NOT NULL,
    p_playerid VARCHAR(255) NOT NULL,
    p_hashedpassword VARCHAR(255) NOT NULL,
    p_salt VARCHAR(255) NOT NULL,

    FOREIGN KEY (p_playerid) REFERENCES user(u_playerid) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS team(
        t_teamname VARCHAR(255) NOT NULL,
        t_teamid VARCHAR(255) NOT NULL,
        t_playerid VARCHAR(255) NOT NULL,
        t_turnnumber VARCHAR(255) NOT NULL,
        t_gameid VARCHAR(255) NOT NULL,
        
        PRIMARY KEY (t_teamid),
        FOREIGN KEY (t_playerid) REFERENCES user(u_playerid) ON DELETE CASCADE,
        FOREIGN KEY (t_turnnumber) REFERENCES turn(tn_turnnumber) ON DELETE CASCADE,
        FOREIGN KEY (t_gameid) REFERENCES game(g_gameid) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS game(
        g_gameid VARCHAR(255) NOT NULL,
        g_player1id VARCHAR(255) NOT NULL,
        g_player2id VARCHAR(255) NOT NULL,
        
        PRIMARY KEY (g_gameid),
        FOREIGN KEY (g_player1id) REFERENCES user(u_playerid) ON DELETE CASCADE,
        FOREIGN KEY (g_player2id) REFERENCES user(u_playerid) ON DELETE CASCADE
);    

CREATE TABLE IF NOT EXISTS turn(
        tn_turnnumber VARCHAR(255) NOT NULL,
        tn_gameid VARCHAR(255) NOT NULL,
        tn_gold VARCHAR(255) DEFAULT 3,
        tn_userid VARCHAR(255) NOT NULL,
        FOREIGN KEY (tn_gameid) REFERENCES game(g_gameid) ON DELETE CASCADE,
        FOREIGN KEY (tn_userid) REFERENCES user(u_userid) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS shop(
        s_shopid VARCHAR(255) NOT NULL,
        s_gameid VARCHAR(255) NOT NULL,
        s_turnid VARCHAR(255) NOT NULL,
        s_userid VARCHAR(255) NOT NULL,
        PRIMARY KEY (s_shopid),
        FOREIGN KEY (s_gameid) REFERENCES game(g_gameid) ON DELETE CASCADE,
        FOREIGN KEY (s_turnid) REFERENCES turn(tn_turnid) ON DELETE CASCADE,
        FOREIGN KEY (s_userid) REFERENCES user(u_userid) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS unit(
        ut_name VARCHAR(255) NOT NULL, 
        ut_unitid VARCHAR(255) NOT NULL,
        ut_shopid VARCHAR(255) NOT NULL,
        ut_teamid VARCHAR(255),
        ut_gold VARCHAR(255) NOT NULL,
        ut_health VARCHAR(255) NOT NULL,
        ut_attack VARCHAR(255) NOT NULL,
        
        PRIMARY KEY (ut_unitid),
        FOREIGN KEY (ut_shopid) REFERENCES shop(s_shopid) ON DELETE CASCADE,
        FOREIGN KEY (ut_teamid) REFERENCES team(t_teamid) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS modifier(
        m_modifierid VARCHAR(255) NOT NULL,
        m_unitid VARCHAR(255) NOT NULL,
        m_shopid VARCHAR(255) NOT NULL,
        m_effect INT NOT NULL,
        m_name VARCHAR(255) NOT NULL,
        m_attribute TEXT NOT NULL, 
        m_cost VARCHAR(255),
        
        PRIMARY KEY (m_modifierid),
        FOREIGN KEY (m_unitid) REFERENCES unit(ut_unitid) ON DELETE CASCADE,
        FOREIGN KEY (m_shopid) REFERENCES shop(s_shopid) ON DELETE CASCADE
);


-- Insert a new game
INSERT INTO game(g_gameID, g_player1id, g_player2id)
VALUES (?, ?, ?);

-- Insert a new turn for the game
INSERT INTO turn(tn_turnnumber, tn_gameid, tn_userid)
VALUES (?, ?, ?)

-- update turn whenever player ends turn
UPDATE turn
SET tn_gold = tn_gold - ?
WHERE tn_gameid = ?
AND tn_userid = ?
AND tn_turnnumber = ?


-- Insert a new team for player1
INSERT INTO team(t_teamname, t_teamid, t_playerid, t_turnnumber, t_gameid)
    VALUES (?, ?, ?, ?, ?)

-- Insert a new team for player2
INSERT INTO team(t_teamname, t_teamid, t_playerid)
VALUES (?, ?, ?);

-- Insert a new shop for the game
INSERT INTO shop(s_shopid, s_gameid, s_turnid, s_userid)
VALUES(?,?,?,?)

-- Insert units into the shop
INSERT INTO unit(ut_name, ut_unitid, ut_shopid, ut_teamid, ut_gold, ut_health, ut_attack)
VALUES (?, ?, ?, NULL, ?, ?, ?)

--Insert modifiers into the shop
INSERT INTO modifier(m_modifierid, m_unitid, m_shopid, m_effect, m_name, m_attribute, m_cost)
VALUES (?, ?, ?, ?, ?, ?, ?)

-- update modifiers
UPDATE modifier
SET m_unitid = ?, m_shopid = ?, m_effect = ?, 
m_name, m_attribute = ?
WHERE m_modifierid = ?

-- find modifier by shopID
SELECT m_modifierid, m_name, m_effect, m_attribute, m_cost
FROM modifier
WHERE m_shopid = ?

-- apply attack boosting modifier
UPDATE unit
SET ut_health = ut_health + ?
WHERE ut_unitid = ?

-- apply health boosting modifier
UPDATE unit
SET ut_attack = ut_attack + ?
WHERE ut_unitid = ?

-- delete modifier from modifierID
DELETE FROM modifier
WHERE m_modifierid = ?


-- Update an existing game with new player IDs
UPDATE game
SET g_player1id = ?, g_player2id = ?
WHERE g_gameid = ?;

-- Delete a game by gameID
DELETE FROM game
WHERE g_gameid = ?;

-- Find gameID from playerID
SELECT g_gameid
FROM game
WHERE g_player1id = ?
OR g_player2id = ?

-- Insert a new shop for the game
INSERT INTO shop(s_shopid, s_gameid)
VALUES (?, ?);

-- Delete a shop by shopID
DELETE FROM shop
WHERE s_shopid = ?;

-- Find a shop by gameID
SELECT s_shopid 
FROM shop
WHERE s_gameid = ?;


-- Insert a new team for a player
INSERT INTO team(t_teamname, t_teamid, t_playerid)
VALUES (?, ?, ?);

-- Update a team's name and playerID
UPDATE team
SET t_teamname = ?, t_playerid = ?
WHERE t_teamid = ?;

-- Delete a team by teamID
DELETE FROM team
WHERE t_teamid = ?;

-- create turn
INSERT INTO turn(tn_turnnumber, tn_gameid)
VALUES (?, ?);

-- Insert a new unit into the unit table
INSERT INTO unit(ut_name, ut_unitid, ut_shopid, ut_teamid, ut_level, ut_health, ut_attack)
VALUES (?, ?, ?, ?, ?, ?, ?);

-- Update an existing unit in the unit table
UPDATE unit
SET ut_name = ?, ut_shopid = ?, ut_teamid = ?, 
    ut_gold = ?, ut_health = ?, ut_attack = ?
WHERE ut_unitid = ?

-- Find units in shop by shopID and where cost is <= user input
SELECT ut_unitid, ut_name, ut_gold, ut_health, ut_attack FROM unit
WHERE ut_shopid = ?
AND ut_teamid IS NULL
AND ut_gold <= ?

-- add unit to Team by assigning unit a teamID
UPDATE unit
SET ut_teamid = ?
WHERE ut_unitid = ?

-- set cost unit
SELECT ut_gold FROM unit WHERE ut_unitid = ?

-- lower gold after purchasing unit from shop
UPDATE turn
SET tn_gold = tn_gold - ?
WHERE tn_gameid = ?
AND tn_userid = ?
AND tn_turnnumber = ?

-- Delete a unit by unit ID
DELETE FROM unit
WHERE ut_unitid = ?;

-- Find units by teamID
SELECT ut_name, ut_health, ut_attack, ut_unitid
FROM unit
WHERE ut_teamid = ?

--get opponents team by playerID and gameID
SELECT ut_name, ut_health, ut_attack, ut_unitid
FROM unit
INNER JOIN team
ON ut_teamid = t_teamid
WHERE t_playerid = ?
AND t_gameid = ?

-- find current turn number by gameID
SELECT MAX(tn_turnnumber) FROM turn
WHERE tn_gameid = ?

-- get current gold from gameID and turn number
SELECT tn_gold FROM turn
WHERE tn_gameID = ?
AND tn_turnnumber = ?
    