-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.




-- Name of the player will be registered here

create table players 
(	player_id serial primary key, 
	name text
);

-- All match and score related data will be registered here

create table scores
(	match serial,
	winner_id INT NOT NULL,
	loser_id INT NULL, 
	tournament int, 
	round int, 
	CONSTRAINT fk_sc_winner_id
		FOREIGN KEY (winner_id)
		REFERENCES players (player_id)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	CONSTRAINT fk_sc_loser_id
		FOREIGN KEY (loser_id)
		REFERENCES players (player_id)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	CHECK (winner_id != loser_id)
);

CREATE VIEW matches_won 
	AS SELECT 	player_id, players.name AS name,
				count(*) AS wins 
	FROM 		players, scores
	WHERE 		players.player_id = scores.winner_id 
	GROUP BY 	player_id;


CREATE VIEW standings
	AS SELECT 	players.player_id AS id, players.name, 
				count(matches_won.wins) AS win,
    			SUM(CASE WHEN scores.match != 0 THEN 1 ELSE 0 END) AS matches 
    FROM 		players
    LEFT JOIN 	scores
    ON 			(players.player_id = scores.winner_id OR players.player_id = scores.loser_id)
    LEFT JOIN 	matches_won 
    ON 			players.player_id = matches_won.player_id
    GROUP BY 	players.player_id
    ORDER BY 	win DESC;