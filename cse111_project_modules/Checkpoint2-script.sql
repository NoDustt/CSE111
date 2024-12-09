DROP TABLE IF EXISTS modifier;
DROP TABLE IF EXISTS unit;
DROP TABLE IF EXISTS shop;
DROP TABLE IF EXISTS turn;
DROP TABLE IF EXISTS game;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS password;
DROP TABLE IF EXISTS user;

CREATE TABLE IF NOT EXISTS user (
    u_username VARCHAR(255) NOT NULL,
    u_playerid VARCHAR(255) NOT NULL,
    PRIMARY KEY (u_playerid, u_username)
);

CREATE TABLE IF NOT EXISTS password (
    p_username VARCHAR(255) NOT NULL,
    p_playerid VARCHAR(255) NOT NULL,
    p_hashedpassword VARCHAR(255) NOT NULL,
    p_salt VARCHAR(255) NOT NULL,
    FOREIGN KEY (p_playerid) REFERENCES user(u_playerid) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS team (
    t_teamname VARCHAR(255) NOT NULL,
    t_teamid VARCHAR(255) NOT NULL,
    t_playerid VARCHAR(255) NOT NULL,
    PRIMARY KEY (t_teamid),
    FOREIGN KEY (t_playerid) REFERENCES user(u_playerid) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS game (
    g_gameid VARCHAR(255) NOT NULL,
    g_player1id VARCHAR(255) NOT NULL,
    g_player2id VARCHAR(255) NOT NULL,
    PRIMARY KEY (g_gameid),
    FOREIGN KEY (g_player1id) REFERENCES user(u_playerid) ON DELETE CASCADE,
    FOREIGN KEY (g_player2id) REFERENCES user(u_playerid) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS turn (
    tn_turnnumber VARCHAR(255) NOT NULL,
    tn_gameid VARCHAR(255) NOT NULL,
    FOREIGN KEY (tn_gameid) REFERENCES game(g_gameid) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS shop (
    s_shopid VARCHAR(255) NOT NULL,
    s_gameid VARCHAR(255) NOT NULL,
    PRIMARY KEY (s_shopid),
    FOREIGN KEY (s_gameid) REFERENCES game(g_gameid) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS unit (
    ut_name VARCHAR(255) NOT NULL,
    ut_unitid VARCHAR(255) NOT NULL,
    ut_shopid VARCHAR(255) NOT NULL,
    ut_teamid VARCHAR(255) NOT NULL,
    ut_level VARCHAR(255) NOT NULL,
    ut_health VARCHAR(255) NOT NULL,
    ut_attack VARCHAR(255) NOT NULL,
    PRIMARY KEY (ut_unitid),
    FOREIGN KEY (ut_shopid) REFERENCES shop(s_shopid) ON DELETE CASCADE,
    FOREIGN KEY (ut_teamid) REFERENCES team(t_teamid) ON DELETE CASCADE
);


-- Insert a new game
INSERT INTO game(g_gameID, g_player1id, g_player2id)
VALUES (?, ?, ?);

-- Insert a new turn for the game
INSERT INTO turn(tn_turnnumber, tn_gameid)
VALUES (?, ?);

-- Insert a new team for player1
INSERT INTO team(t_teamname, t_teamid, t_playerid)
VALUES (?, ?, ?);

-- Insert a new team for player2
INSERT INTO team(t_teamname, t_teamid, t_playerid)
VALUES (?, ?, ?);

-- Insert a new shop for the game
INSERT INTO shop(s_shopid, s_gameid)
VALUES(?, ?);

-- Insert units into the shop and assign them to the team
INSERT INTO unit(ut_name, ut_unitid, ut_shopid, ut_teamid, ut_level, ut_health, ut_attack)
VALUES (?, ?, ?, ?, ?, ?, ?);

-- Update an existing game with new player IDs
UPDATE game
SET g_player1id = ?, g_player2id = ?
WHERE g_gameid = ?;

-- Delete a game by gameID
DELETE FROM game
WHERE g_gameid = ?;

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


INSERT INTO turn(tn_turnnumber, tn_gameid)
VALUES (?, ?);


-- Insert a new unit into the unit table
INSERT INTO unit(ut_name, ut_unitid, ut_shopid, ut_teamid, ut_level, ut_health, ut_attack)
VALUES (?, ?, ?, ?, ?, ?, ?);

-- Update an existing unit in the unit table
UPDATE unit
SET ut_name = ?, ut_shopid = ?, ut_teamid = ?, 
    ut_level = ?, ut_health = ?, ut_attack = ?
WHERE ut_unitid = ?;

-- Find units by shop ID
SELECT ut_name, ut_level, ut_health, ut_attack 
FROM unit
WHERE ut_shopid = ?;

-- Delete a unit by unit ID
DELETE FROM unit
WHERE ut_unitid = ?;

    