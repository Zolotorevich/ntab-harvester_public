"""Database connection"""
from typing import Any

import mysql.connector

DB_OPTIONS = {
  'host': 'localhost',
  'user': 'root',
  'password': '',
  'database': 'ntab'
}

def write(table: str, data: list[dict[str, Any]]) -> int:
    """Write data to database

    Args:
        table: table name postfix e.g. 'news' for 'harvester_news'
        data: dict with data {title, url, preview, date}

    Returns:
        Number of affected rows

    Raises:
        ConnectionError: for SQL errors
    """

    query = (f'INSERT INTO harvester_{table} (title, url, preview, date) '
             'VALUES (%(title)s, %(url)s, %(preview)s, %(date)s) '
             'ON DUPLICATE KEY UPDATE url=url')

    try:
        connection = mysql.connector.connect(**DB_OPTIONS)
        cursor = connection.cursor()
        cursor.executemany(query, data)
        affected_rows = cursor.rowcount
        connection.commit()
        cursor.close()
        connection.close()

    except mysql.connector.Error as error:
        raise ConnectionError(f'SQL Fail to insert {error}')

    finally:
        if connection.is_connected(): # type: ignore
            connection.close() # type: ignore

    return affected_rows