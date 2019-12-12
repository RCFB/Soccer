-- Le DROP des tables est commenté car les tables ont ete crees, si on fait flask init-db sa va effacer les tables, on perds tout.
-- Il faut decommenter les DROPS si on veux creer  ou recreer les tables .
DROP VIEW IF EXISTS matches_with_team_names;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS users;

CREATE TABLE teams(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL
);

CREATE TABLE matches(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TIMESTAMP NOT NULL,
  team0 INTEGER NOT NULL,
  team1 INTEGER NOT NULL,
  score0 INTEGER NOT NULL,
  score1 INTEGER NOT NULL,
  FOREIGN KEY(team0) REFERENCES teams(id) ON DELETE CASCADE,
  FOREIGN KEY(team1) REFERENCES teams(id) ON DELETE CASCADE,
  UNIQUE(team0, team1)
);

CREATE TABLE users(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  admin INTEGER NOT NULL 
);

CREATE VIEW matches_with_team_names(id, date, score0, score1, team0, team1, team0_name, team1_name)
AS SELECT matches.id, date, score0, score1, team0, team1, teams0.name, teams1.name from matches
          INNER JOIN teams as teams0 ON teams0.id = team0
          INNER JOIN teams as teams1 ON teams1.id = team1;

