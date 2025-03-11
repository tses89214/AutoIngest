import mysql.connector
from collections import OrderedDict

class DatabaseConnector:
    def __init__(self, db_host, db_name, db_user, db_password):
        self.db_host = db_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.mydb = None
        self.cursor = None

    def connect(self):
        try:
            self.mydb = mysql.connector.connect(
                host=self.db_host,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name
            )
            self.cursor = self.mydb.cursor()
        except mysql.connector.Error as err:
            print(f"Database Connection Error: {err}")
            raise

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.mydb and self.mydb.is_connected():
            self.mydb.close()

    def get_table_names(self):
        """
        Extracts the table names from the database.

        Returns:
            list: A list of table names.
        """
        try:
            self.connect()
            # Get table names
            self.cursor.execute("SELECT DISTINCT `table` FROM expect_schema")
            table_names = [row[0] for row in self.cursor.fetchall()]
            return table_names
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return []
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []
        finally:
            self.close()

    def extract_schema(self, table_name):
        """
        Extracts the schema from the database for a given table, ordered by column_order.

        Args:
            table_name (str): The name of the table to extract the schema for.

        Returns:
            dict: A dictionary representing the schema, with column names as keys and data types as values, ordered by column_order.
        """
        try:
            self.connect()
            # Get column, data_type and column_order from expect_schema table
            self.cursor.execute(
                "SELECT `column`, `data_type`, `column_order` FROM expect_schema WHERE `table` = %s ORDER BY `column_order`",
                (table_name,),
            )
            # Create an ordered dictionary from the result
            ordered_schema = OrderedDict()
            for row in self.cursor.fetchall():
                ordered_schema[row[0]] = row[1]
            return ordered_schema
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
        finally:
            self.close()
