import pyodbc
from pyodbc import Connection, Row
from dataclasses import dataclass
from typing import List


@dataclass
class DBConfig:
    username: str
    password: str
    database: str
    instance: str
    hostname: str = "localhost"
    driver: str = None
    sqlconnection_string = ""
    sqlconnection: Connection = None


@dataclass
class Databases(DBConfig):

    def connect(self) -> Connection:
            # If a default driver is set, use it to connect
        connection_string = (
            f"DRIVER={self.driver};"
            f"SERVER={self.hostname}\\{self.instance};"
            f"DATABASE={self.database};"
            f"UID={self.username};"
            f"PWD={self.password};"
        )

        self.sqlconnection = pyodbc.connect(connection_string)
        return self.sqlconnection

    def close(self):
        if self.sqlconnection:
            self.sqlconnection.close()
            self.sqlconnection = None
        else:
            print("No active connection to close.")

    def rows_to_dict(self, rows: List[Row]) -> List[dict]:
        """Convert a list of pyodbc Row objects to a list of dictionaries."""
        if not rows:
            return []
        if not hasattr(rows[0], "cursor_description"):
            raise ValueError(
                "Rows must be a list of pyodbc Row objects with cursor_description."
            )
        if not self.sqlconnection:
            raise Exception("Database connection is not established.")
        if not rows[0].cursor_description:
            raise ValueError("Rows must have cursor_description attribute.")

        columns = [col[0] for col in rows[0].cursor_description]
        if not columns:
            raise ValueError(
                "Cursor description is empty, cannot convert rows to dicts."
            )

        rows_list = []

        for row in rows:
            row_obj = {}
            for idx, col in enumerate(row):
                row_obj[columns[idx]] = col
            rows_list.append(row_obj)

        return rows_list

    def query(self, sql: str = "", params=()) -> List[dict]:
        if not self.sqlconnection:
            raise Exception("Database connection is not established.")

        cursor = self.sqlconnection.cursor()
        cursor.execute(sql, params)
        results = cursor.fetchall()
        cursor.close()
        return self.rows_to_dict(results)

    @staticmethod
    def fetchall(dbconfig: dict, query: str, *args: tuple) -> List[dict]:
        if isinstance(dbconfig, DBConfig):
            dbconfig = dbconfig.__dict__
        db = Databases(**dbconfig)
        db.connect()

        if not db.sqlconnection:
            raise Exception("Database connection is not established.")

        cursor = db.sqlconnection.cursor()
        cursor.execute(query, args)
        result = cursor.fetchall()
        cursor.close()
        db.sqlconnection.close()
        return db.rows_to_dict(result)
