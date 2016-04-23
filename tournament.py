#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#


import psycopg2



def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def initiateStandings():
    """Initiate the standings table"""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("select id from players")
    results = cursor.fetchall()
    cursor.execute("delete from standings")
    for index in range(len(results)):
        cursor.execute(
            "insert into standings (id, played, wins) values (%s , 0, 0)" , (results[index],))
    conn.commit()
    conn.close()

def updateStandings(winner , loser):
    """ Update the standings table on every match completion"""
    

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("select played, wins from standings where id = %s" , (winner,))
    results = cursor.fetchone()
    played = results[0] + 1
    wins = results [1] + 1
    cursor.execute("update standings set  played = %s,  wins = %s where standings.id = %s" , (played, wins, winner))    
    conn.commit()
    cursor.execute("select played, wins from standings where id = %s" , (loser,))
    results = cursor.fetchone()
    played = results[0] + 1
    wins = results [1]
    cursor.execute("update standings set  played = %s,  wins = %s where standings.id = %s" , (played, wins, loser))    
    conn.commit()
    conn.close()





def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("delete from matches")
    initiateStandings()
    conn.commit()
    conn.close() 
      

def deletePlayers():
    """Remove all the player records from the database."""

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("delete from players")
    cursor.execute("delete from standings")
    conn.commit()
    conn.close() 
    

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("select count(name) from players")
    results = cursor.fetchone()
    conn.close()
    return(results[0])


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("insert into players (name) values (%s)" , (name,))
    conn.commit()
    cursor.execute("select id from players order by id DESC")
    results = cursor.fetchone()
    cursor.execute(
            "insert into standings (id, played, wins) values (%s , 0, 0)" , (results[0],))
    conn.commit()
    conn.close()
    


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
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("select players.id as id, name, wins, played from players join standings on players.id = standings.id order by wins")
    standings = cursor.fetchall()
    conn.close() 
    return standings



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    

    text1 = str(winner) + " VS " + str(loser)
    
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("insert into matches values (%s, %s, %s)" , (text1, winner, loser))
    conn.commit()
    conn.close()
    updateStandings(winner,loser) 
    


 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("select standings.id, name from standings join players on players.id = standings.id order by wins desc;")
    pairings = []
    for row in cursor:
        
        pairings.append(row[0])
        pairings.append(row[1])
        
    conn.close()
    result = []
    temptuple = []
    i = (len(pairings))
    for row in range(i):
      temptuple.append(pairings[row])
      if ((row % 4) == 3):
           result.append(temptuple)
           temptuple =[]
    return result






