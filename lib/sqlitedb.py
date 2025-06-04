import sqlite3
from pathlib import Path
from typing import Dict, List, Union, Optional


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

    def _format_response(
        self,
        error: bool = False,
        message: str = "",
        data: Optional[Union[List[Dict], Dict]] = None,
        record_id: Optional[int] = None,
        sqlerror: Optional[str] = None,
    ) -> Dict:
        """Helper method to format consistent response"""
        return {
            "error": error,
            "message": message,
            "data": data if data is not None else [],
            "recordId": record_id,
            "sqlerror": str(sqlerror) if sqlerror else None,
        }

    def execute_query(self, query: str, params=None) -> list[dict]:
        """Execute a query and return the results."""
        if not self.connection:
            raise Exception("Database connection is not established.")

        cursor = self.connection.cursor()
        cursor.execute(query, params or [])
        result: list[sqlite3.Row] = cursor.fetchall()
        cursor.close()

        return [dict(row) for row in result]

    def save(self, table: str, data: Dict) -> Dict:
        """
        Insert a new record into the specified table.

        Args:
            table: Name of the table
            data: Dictionary with column names as keys and values to insert

        Returns:
            Dictionary with operation results
        """
        try:
            if not self.connection:
                self.connect()

            columns = ", ".join(data.keys())
            placeholders = ", ".join(["?"] * len(data))
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

            cursor = self.connection.cursor()
            cursor.execute(query, tuple(data.values()))
            self.connection.commit()
            record_id = cursor.lastrowid
            cursor.close()

            return self._format_response(
                error=False, message="Record saved successfully", record_id=record_id
            )

        except sqlite3.Error as e:
            return self._format_response(
                error=True, message="Failed to save record", sqlerror=e
            )

        except Exception as e:
            return self._format_response(error=True, message=str(e), sqlerror=None)

    def delete(self, table: str, id: int) -> Dict:
        try:
            if not self.connection:
                self.connect()

            query = f"DELETE FROM {table} WHERE id={id}"

            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            record_id = cursor.lastrowid
            cursor.close()

            return self._format_response(
                error=False, message="Record deleted successfully", record_id=record_id
            )

        except sqlite3.Error as e:
            return self._format_response(
                error=True, message="Failed to save record", sqlerror=e
            )

        except Exception as e:
            return self._format_response(error=True, message=str(e), sqlerror=None)

    def update(self, table: str, record_id: int, data: Dict) -> Dict:
        """
        Update an existing record in the specified table.

        Args:
            table: Name of the table
            record_id: ID of the record to update
            data: Dictionary with column names as keys and new values

        Returns:
            Dictionary with operation results
        """
        try:
            if not self.connection:
                self.connect()

            set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
            query = f"UPDATE {table} SET {set_clause} WHERE id = ?"

            cursor = self.connection.cursor()
            cursor.execute(query, tuple(data.values()) + (record_id,))
            self.connection.commit()
            affected_rows = cursor.rowcount
            cursor.close()

            if affected_rows == 0:
                return self._format_response(
                    error=True,
                    message="No record found with the specified ID",
                    record_id=record_id,
                )

            return self._format_response(
                error=False, message="Record updated successfully", record_id=record_id
            )

        except sqlite3.Error as e:
            return self._format_response(
                error=True,
                message="Failed to update record",
                record_id=record_id,
                sqlerror=e,
            )

        except Exception as e:
            return self._format_response(
                error=True, message=str(e), record_id=record_id, sqlerror=None
            )

    def fetchall(
        self, table: str, conditions: Dict = None, limit: int = 50, order_by: str = None
    ) -> Dict:
        """
        Retrieve all records from the specified table, optionally filtered.

        Args:
            table: Name of the table
            conditions: Optional dictionary of filter conditions
            order_by: Optional ORDER BY clause

        Returns:
            Dictionary with operation results including data
        """
        try:
            if not self.connection:
                self.connect()

            query = f"SELECT * FROM {table}"
            params = []

            if conditions:
                where_clause = " AND ".join([f"{key} = ?" for key in conditions.keys()])
                query += f" WHERE {where_clause}"
                params.extend(conditions.values())

            if order_by:
                query += f" ORDER BY {order_by}"
            
            if limit:
                query += f" LIMIT {limit}"

            cursor = self.connection.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()
            cursor.close()

            data = [dict(row) for row in result]

            return self._format_response(
                error=False, message="Records retrieved successfully", data=data
            )

        except sqlite3.Error as e:
            return self._format_response(
                error=True, message="Failed to retrieve records", sqlerror=e
            )

        except Exception as e:
            return self._format_response(error=True, message=str(e), sqlerror=None)

    def fetchone(
        self, table: str, record_id: int = None, conditions: Dict = None
    ) -> Dict:
        """
        Retrieve a single record from the specified table.

        Args:
            table: Name of the table
            record_id: Optional ID of the record to fetch
            conditions: Optional dictionary of filter conditions

        Returns:
            Dictionary with operation results including single data record
        """
        try:
            if not self.connection:
                self.connect()

            query = f"SELECT * FROM {table}"
            params = []

            if record_id is not None:
                query += " WHERE id = ?"
                params.append(record_id)
            elif conditions:
                where_clause = " AND ".join([f"{key} = ?" for key in conditions.keys()])
                query += f" WHERE {where_clause}"
                params.extend(conditions.values())
            else:
                return self._format_response(
                    error=True,
                    message="Either record_id or conditions must be provided",
                )

            query += " LIMIT 1"

            cursor = self.connection.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()
            cursor.close()

            if not result:
                return self._format_response(
                    error=True, message="No record found", record_id=record_id
                )

            return self._format_response(
                error=False,
                message="Record retrieved successfully",
                data=dict(result),
                record_id=record_id if record_id else result.get("id"),
            )

        except sqlite3.Error as e:
            return self._format_response(
                error=True,
                message="Failed to retrieve record",
                record_id=record_id,
                sqlerror=e,
            )

        except Exception as e:
            return self._format_response(
                error=True, message=str(e), record_id=record_id, sqlerror=None
            )
