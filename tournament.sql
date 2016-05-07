-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


create database tournament;

CREATE TABLE players(
	 id serial PRIMARY KEY,
	 name varchar(50));

CREATE TABLE matches(
	 id serial PRIMARY KEY,
	 winner integer REFERENCES players(id),
	 loser integer REFERENCES players(id));

CREATE VIEW Wins as select players.id,players.name,count(winner) as wins from players left join matches on players.id = winner group by players.id order by wins desc;   


CREATE VIEW Defeats as select players.id,count(loser) as Defeats from players left join matches on players.id = loser group by players.id order by defeats desc;

