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
    hostname: str = 'localhost'
    driver: str = None
    sqlconnection_string = ''
    sqlconnection: Connection = None
    drivers_list = [
        '{ODBC Driver 11 for SQL Server}',
        '{ODBC Driver 13 for SQL Server}',
        '{ODBC Driver 13.1 for SQL Server}',
        '{ODBC Driver 17 for SQL Server}',
        '{ODBC Driver 18 for SQL Server}',
        '{SQL Server Native Client 11.0}',
        '{SQL Server Native Client 10.0}',
        '{SQL Native Client}',
        '{SQL Server}'
    ]

@dataclass
class Databases(DBConfig):

    def connect(self) -> Connection:

        if self.driver is None:
            for driver in self.drivers_list:
                try:
                    # Attempt to connect using the driver
                    connection_string = (
                        f'DRIVER={driver};'
                        f'SERVER={self.hostname};'
                        f'DATABASE={self.database};'
                        f'UID={self.username};'
                        f'PWD={self.password};'
                    )
                    # If successful, return the connection string
                    self.sqlconnection = pyodbc.connect(connection_string)
                    return self.sqlconnection
                
                except pyodbc.Error as e:
                    # If the connection fails, log the error and continue to the next driver
                    msg = f"Failed to connect with {driver}: {e}"
                    print(msg)

                except Exception as e:
                    msg = f"Failed to connect with {driver}: {e}"
                    print(msg)
                    return msg
        else:
            # If a default driver is set, use it to connect
            connection_string = (
                f'DRIVER={self.driver};'
                f'SERVER={self.hostname}\\{self.instance};'
                f'DATABASE={self.database};'
                f'UID={self.username};'
                f'PWD={self.password};'
            )

            self.sqlconnection = pyodbc.connect(connection_string)
            return self.sqlconnection
            
        raise Exception("No valid SQL driver found.")

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
        if not hasattr(rows[0], 'cursor_description'):
            raise ValueError("Rows must be a list of pyodbc Row objects with cursor_description.")
        if not self.sqlconnection:
            raise Exception("Database connection is not established.")
        if not rows[0].cursor_description:
            raise ValueError("Rows must have cursor_description attribute.")
        
        columns = [col[0] for col in rows[0].cursor_description]
        if not columns:
            raise ValueError("Cursor description is empty, cannot convert rows to dicts.")
        

        rows_list = []

        for row in rows:
            row_obj = {}
            for idx, col in enumerate(row):
                row_obj[columns[idx]] = col
            rows_list.append(row_obj)
    
        return rows_list

    def query(self, sql: str) -> List[dict]:
        if not self.sqlconnection:
            raise Exception("Database connection is not established.")
        
        cursor = self.sqlconnection.cursor()
        cursor.execute(sql)
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

