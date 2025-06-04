import sqlite3
from pathlib import Path


class SQLiteDB:
    def __init__(self, db_path=None):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        """Establish a connection to the SQLite database."""

        if self.db_path is None:
            path = Path(__file__).parent.parent.joinpath("data.db")
        else:
            path = Path(__file__).parent.parent.joinpath(self.db_path)

        self.db_path = path.resolve()
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row  # Enable row access by column name

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query, params=None) -> list[dict]:
        """Execute a query and return the results."""
        if not self.connection:
            raise Exception("Database connection is not established.")

        cursor = self.connection.cursor()
        cursor.execute(query, params or [])
        result: list[sqlite3.Row] = cursor.fetchall()
        cursor.close()

        list_of_dicts = []

        for row in result:
            item = {}
            for key in row.keys():
                item[key] = row[key]
            list_of_dicts.append(item)
        return list_of_dicts
