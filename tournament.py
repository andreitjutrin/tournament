#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect(query):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()
    c.execute(query)
    db.commit()
    db.close

def deleteMatches():
    """Remove all the match records from the database."""

    query = "DELETE FROM scores;"
    connect(query)

def deletePlayers():
    """Remove all the player records from the database."""
 
    query = "DELETE FROM players"
    connect(query)

def countPlayers():
    """Returns the number of players currently registered."""

    query = "SELECT count(*) FROM players;"
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()
    c.execute(query)
    result = c.fetchall()
    db.commit()
    db.close
    return result[0][0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    clean_name = bleach.clean(name)
    query = "INSERT INTO players(name) values(%s);"
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()
    c.execute(query, (clean_name,))
    db.commit()
    db.close

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    query = "SELECT players.player_id AS id, players.name, count(matches_won.wins) AS win, \
            SUM(CASE WHEN scores.match != 0 THEN 1 ELSE 0 END) AS matches \
            FROM players \
            LEFT JOIN scores \
            ON (players.player_id = scores.winner_id OR players.player_id = scores.loser_id) \
            LEFT JOIN matches_won ON players.player_id = matches_won.player_id \
            GROUP BY players.player_id \
            ORDER BY win DESC;"
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()
    c.execute(query)
    result = c.fetchall()
    db.commit()
    db.close
    return result

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    query = "INSERT INTO scores(winner_id, loser_id) VALUES(%s, %s);"
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()
    c.execute(query, (winner, loser))
    db.commit()
    db.close

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  9*/634
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    query = "SELECT id, name FROM standings;"
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()
    c.execute(query)
    results = c.fetchall()
    db.close
    
    pairs = []
    pair = []
    for result in results:
        pair.extend(result)
        if len(pair) == 4:
            pairs.append(pair)
            pair = []
    return pairs

