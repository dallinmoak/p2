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
