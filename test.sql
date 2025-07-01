SELECT
  (people.nameFirst || ' ' || people.nameLast) AS "Player Name",
  schools.name_full AS School,
  salaries.yearID as Year,
  salaries.salary as Salary,
  teams.name AS Team
FROM
  people
  JOIN collegePlaying ON people.playerID = collegePlaying.playerID
  JOIN schools ON collegePlaying.schoolID = schools.schoolID
  JOIN salaries ON people.playerID = salaries.playerID
  JOIN teams ON salaries.teamID = teams.teamID
WHERE
  schools.schoolID = "idbyuid"
GROUP BY
  people.playerID,
  salaries.salary,
  salaries.yearID,
  salaries.teamID;

SELECT
  batting.playerID,
  (people.nameFirst || ' ' || people.nameLast) AS "Player Name",
  teams.name,
  batting.yearID,
  batting.AB AS "At Bats",
  batting.H AS "Hits",
  CAST(batting.H AS FLOAT) / CAST(batting.AB AS FLOAT) AS "Batting Average"
FROM
  batting
  INNER JOIN people ON batting.playerID = people.playerID
  INNER JOIN teams ON batting.team_ID = teams.ID
WHERE
  batting.AB >= 1
ORDER BY
  "Batting Average" DESC,
  batting.playerID ASC
LIMIT
  5;

SELECT
  batting.playerID,
  (people.nameFirst || ' ' || people.nameLast) AS "Player Name",
  teams.name,
  SUM(batting.AB) AS "Total At Bats",
  SUM(batting.H) AS "Total Hits",
  CAST(SUM(batting.H) AS FLOAT) / CAST(SUM(batting.AB) AS FLOAT) AS "Career Batting Average"
FROM
  batting
  INNER JOIN people ON batting.playerID = people.playerID
  INNER JOIN teams ON batting.team_ID = teams.ID
GROUP BY
  batting.playerID,
  people.nameFirst,
  people.nameLast,
  teams.name
HAVING
  "Total At Bats" >= 100
ORDER BY
  "Career Batting Average" DESC,
  batting.playerID ASC
LIMIT
  5;

SELECT
  teams.teamID,
  teams.name,
  COUNT(DISTINCT teams.park) - 1 AS "lifetime_park_changes",
  COUNT(*) AS "total_years_active",
  CAST(COUNT(DISTINCT teams.park) AS FLOAT) / COUNT(*) * 100 AS "park_changes_100_year_average"
FROM
  teams
WHERE
  teams.park IS NOT NULL
GROUP BY
  teams.teamID
HAVING
  "lifetime_park_changes" >= 1
ORDER BY
  "park_changes_100_year_average" ASC;