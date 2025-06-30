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