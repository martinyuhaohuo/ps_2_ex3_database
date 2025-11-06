import sqlite3 as sql
import pandas as pd
from typing import Optional


def find_column_name(
    table_name: str,
    connection: sql.Connection,
    properties: Optional[list[str]] = ["name", "type"],
) -> pd.DataFrame | pd.Series:
    query = f"""
    PRAGMA table_info({table_name})
    """
    result = pd.read_sql(query, connection)[properties]
    return result


def col_all_table(connection: sql.Connection) -> None:
    # look at column names of all tables
    query = """
        SELECT name
        FROM sqlite_master
        WHERE type = "table"
    """
    table_names = pd.read_sql(query, connection)["name"]
    for table in table_names:
        print(
            f"{table}: "
            + ", ".join(find_column_name(table, connection)["name"].to_list())
            + "\n"
        )


def get_pts_team_year(connection: sql.Connection) -> pd.DataFrame:
    query = """
    SELECT a.year, a.team_id, b.abbreviation, avg(pts) AS avg_pts
    FROM (
        SELECT strftime("%Y", game_date_est) AS year,
            team_id_home AS team_id,
            pts_home AS pts
        FROM line_score
        UNION ALL
        SELECT strftime("%Y", game_date_est) AS year,
            team_id_away AS team_id,
            pts_away AS pts
        FROM line_score
        ) AS a
    LEFT JOIN (
        SELECT distinct id,
            abbreviation
            FROM team
    ) AS b ON a.team_id = b.id
    GROUP BY 1,2,3
    HAVING abbreviation IS NOT NULL
    ORDER BY 1 DESC,4 DESC
    """
    pts_team_year = pd.read_sql(query, connection)
    pts_team_year["year"] = pts_team_year["year"].astype(int)
    return pts_team_year


def get_team_attendance(connection: sql.Connection) -> pd.DataFrame:
    query = """
    SELECT b.abbreviation, avg(a.attendance) AS avg_atend
    FROM
    (SELECT game_id, attendance FROM game_info
        WHERE CAST(strftime("%Y", game_date) AS INTEGER) >= 2014
    ) AS a
    LEFT JOIN
    (SELECT distinct game_id, team_abbreviation_home AS abbreviation
        FROM game
    ) AS b
    ON a.game_id = b.game_id
    GROUP BY 1
    HAVING avg(a.attendance) IS NOT NULL
    ORDER BY 2 DESC
    """
    team_attendance = pd.read_sql(query, connection)
    return team_attendance
