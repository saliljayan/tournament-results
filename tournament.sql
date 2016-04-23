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
	 matches varchar(50),
	 winner integer,
	 loser integer);

CREATE TABLE standings(
	 id integer references players(id) on DELETE CASCADE,
	 played integer,
	 wins integer);