import sqlite3
import pandas as pd
import numpy as np
from lets_plot import *

LetsPlot.setup_html(isolated_frame=True)

sqlite_file = "lahmansbaseballdb.sqlite"

db = sqlite3.connect(sqlite_file)

table_data = pd.read_sql_query("SELECT * FROM sqlite_master WHERE type='table';", db)

# people.playerId-> collegePlaying.playerId -->collegePlaying.schooId-> "idbyuid"


q1_query = """
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
"""

q1_data = pd.read_sql_query(q1_query, db)

q2a_query = """
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
"""

q2a_data = pd.read_sql_query(q2a_query, db)


q2b_query = """
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
  batting.AB >= 10
ORDER BY
  "Batting Average" DESC,
  batting.playerID ASC
LIMIT
  5;
"""

q2b_data = pd.read_sql_query(q2b_query, db)

q2c_query = """
SELECT
  batting.playerID,
  (people.nameFirst || ' ' || people.nameLast) AS "Player Name",
  SUM(batting.AB) AS "Total At Bats",
  SUM(batting.H) AS "Total Hits",
  CAST(SUM(batting.H) AS FLOAT) / CAST(SUM(batting.AB) AS FLOAT) AS "Career Batting Average"
FROM
  batting
  INNER JOIN people ON batting.playerID = people.playerID
GROUP BY
  batting.playerID,
  people.nameFirst,
  people.nameLast
HAVING
  "Total At Bats" >= 100
ORDER BY
  "Career Batting Average" DESC,
  batting.playerID ASC
LIMIT
  5;
"""

q2c_data = pd.read_sql_query(q2c_query, db)

q3_query = """
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
  "lifetime_park_changes" >= 5
  AND "total_years_active" >= 10
ORDER BY
  "park_changes_100_year_average" DESC;
"""

q3_data = pd.read_sql_query(q3_query, db)

q3_plot = (
    ggplot(
        data=q3_data,
        mapping=aes(x="name", y="park_changes_100_year_average", fill="name"),
    )
    + geom_bar(stat="identity")
    + labs(
        title="Average Park Changes per 100 Years by Team",
        x="Team Name",
        y="Park Changes per 100 Years",
    )
)

s1_query = """
SELECT
  f.playerID,
  f.yearID,
  f.POS,
  f.G,
  s.salary
FROM
  fielding AS f
  INNER JOIN salaries AS s
ON
  s.yearID = f.yearID
  AND s.playerID = f.playerID
WHERE
  f.ID = (
    SELECT
      f2.ID
    FROM
      fielding AS f2
    WHERE
      f2.playerID = f.playerID
      AND f2.yearID = f.yearID
    ORDER BY
      f2.G DESC
    LIMIT
      1
  )
"""

s1_data = pd.read_sql_query(s1_query, db)
