SELECT
  f.playerID,
  f.yearID,
  f.POS,
  f.G,
  s.salary
FROM
  fielding AS f
  INNER JOIN salaries AS s
WHERE
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