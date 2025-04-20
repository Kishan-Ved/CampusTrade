"""
Database implementation using B+ Tree for indexing.
"""

import os
import json
from .table import Table

class Database:
    """Database class for managing tables."""

    def __init__(self, name, data_directory="data"):
        """
        Initialize a database.

        Args:
            name (str): The name of the database
            data_directory (str): The directory to store the database files
        """
        self.name = name
        self.tables = {}
        self.data_directory = os.path.join(data_directory, name)

        # Create the data directory if it doesn't exist
        os.makedirs(self.data_directory, exist_ok=True)

    def create_table(self, name, schema, order=5):
        """
        Create a new table in the database.

        Args:
            name (str): The name of the table
            schema (dict): The schema of the table (column name -> data type)
            order (int): The order of the B+ Tree for indexing

        Returns:
            Table: The created table, or None if a table with the same name already exists
        """
        if name in self.tables:
            return None

        table = Table(name, schema, order)
        self.tables[name] = table
        return table

    def drop_table(self, name):
        """
        Drop a table from the database.

        Args:
            name (str): The name of the table

        Returns:
            bool: True if the table was dropped, False if it doesn't exist
        """
        if name not in self.tables:
            return False

        del self.tables[name]
        return True

    def get_table(self, name):
        """
        Get a table from the database.

        Args:
            name (str): The name of the table

        Returns:
            Table: The table, or None if it doesn't exist
        """
        return self.tables.get(name)

    def list_tables(self):
        """
        List all tables in the database.

        Returns:
            list: A list of table names
        """
        return list(self.tables.keys())

    def save(self):
        """
        Save the database to disk.

        Returns:
            bool: True if the database was saved successfully, False otherwise
        """
        try:
            # Create the data directory if it doesn't exist
            os.makedirs(self.data_directory, exist_ok=True)

            # Save the database metadata
            metadata = {
                'name': self.name,
                'tables': list(self.tables.keys())
            }

            with open(os.path.join(self.data_directory, "metadata.json"), 'w') as f:
                json.dump(metadata, f, indent=2)

            # Save each table
            for table in self.tables.values():
                table.save_to_file(self.data_directory)

            return True
        except Exception as e:
            print(f"Error saving database {self.name}: {e}")
            return False

    @classmethod
    def load(cls, name, data_directory="data"):
        """
        Load a database from disk.

        Args:
            name (str): The name of the database
            data_directory (str): The directory to load the database from

        Returns:
            Database: The loaded database, or None if the database couldn't be loaded
        """
        try:
            # Normalize the database name (convert to lowercase)
            name = name.lower()

            # Get the absolute path to the data directory
            abs_data_directory = os.path.abspath(data_directory)
            db_directory = os.path.join(abs_data_directory, name)

            print(f"Attempting to load database from: {db_directory}")

            # Check if the database directory exists
            if not os.path.exists(db_directory):
                print(f"Database directory not found: {db_directory}")

                # Check if there's a case-insensitive match
                if os.path.exists(abs_data_directory):
                    for dir_name in os.listdir(abs_data_directory):
                        if dir_name.lower() == name.lower():
                            db_directory = os.path.join(abs_data_directory, dir_name)
                            print(f"Found case-insensitive match: {db_directory}")
                            break

                if not os.path.exists(db_directory):
                    return None

            # Check if metadata.json exists
            metadata_path = os.path.join(db_directory, "metadata.json")
            if not os.path.exists(metadata_path):
                print(f"Metadata file not found: {metadata_path}")
                return None

            # Load the database metadata
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)

            # Create a new database
            db = cls(metadata['name'], data_directory)

            # Load each table
            for table_name in metadata['tables']:
                table = Table.load_from_file(db_directory, table_name)
                if table is not None:
                    db.tables[table_name] = table
                else:
                    print(f"Failed to load table: {table_name}")

            return db
        except Exception as e:
            print(f"Error loading database {name}: {e}")
            import traceback
            traceback.print_exc()
            return None

    @staticmethod
    def list_databases(data_directory="data"):
        """
        List all available databases.

        Args:
            data_directory (str): The directory to look for databases

        Returns:
            list: A list of database names
        """
        try:
            # Get the absolute path to the data directory
            abs_data_directory = os.path.abspath(data_directory)

            # Check if the data directory exists
            if not os.path.exists(abs_data_directory):
                return []

            # Get all subdirectories in the data directory
            databases = []
            for item in os.listdir(abs_data_directory):
                item_path = os.path.join(abs_data_directory, item)
                if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, "metadata.json")):
                    databases.append(item)

            return databases
        except Exception as e:
            print(f"Error listing databases: {e}")
            return []

    def execute_query(self, query):
        """
        Execute a query on the database.

        Args:
            query (dict): The query to execute

        Returns:
            The result of the query, or None if the query is invalid
        """
        # Check if the query is valid
        if not isinstance(query, dict) or 'type' not in query:
            return None

        # Execute the query based on its type
        if query['type'] == 'select':
            return self._execute_select(query)
        elif query['type'] == 'insert':
            return self._execute_insert(query)
        elif query['type'] == 'update':
            return self._execute_update(query)
        elif query['type'] == 'delete':
            return self._execute_delete(query)
        elif query['type'] == 'create_table':
            return self._execute_create_table(query)
        elif query['type'] == 'drop_table':
            return self._execute_drop_table(query)
        elif query['type'] == 'create_index':
            return self._execute_create_index(query)
        elif query['type'] == 'drop_index':
            return self._execute_drop_index(query)
        else:
            return None

    def _execute_select(self, query):
        """
        Execute a select query.

        Args:
            query (dict): The query to execute

        Returns:
            The result of the query, or None if the query is invalid
        """
        # Check if the query is valid
        if 'table' not in query or query['table'] not in self.tables:
            return None

        table = self.tables[query['table']]

        # Handle different types of select queries
        if 'key' in query and 'column' in query:
            # Select by index
            return table.select_by_index(query['column'], query['key'])
        elif 'start_key' in query and 'end_key' in query and 'column' in query:
            # Select range by index
            return table.select_range_by_index(query['column'], query['start_key'], query['end_key'])
        elif 'aggregate' in query and 'column' in query:
            # Aggregation
            return table.aggregate(query['column'], query['aggregate'], query.get('where'))
        else:
            # Regular select
            return table.select(query.get('columns'), query.get('where'))

    def _execute_insert(self, query):
        """
        Execute an insert query.

        Args:
            query (dict): The query to execute

        Returns:
            bool: True if the row was inserted, False otherwise
        """
        # Check if the query is valid
        if 'table' not in query or query['table'] not in self.tables or 'row' not in query:
            return False

        table = self.tables[query['table']]
        return table.insert(query['row'])

    def _execute_update(self, query):
        """
        Execute an update query.

        Args:
            query (dict): The query to execute

        Returns:
            int: The number of rows updated
        """
        # Check if the query is valid
        if 'table' not in query or query['table'] not in self.tables or 'set' not in query:
            return 0

        table = self.tables[query['table']]
        return table.update(query['set'], query.get('where'))

    def _execute_delete(self, query):
        """
        Execute a delete query.

        Args:
            query (dict): The query to execute

        Returns:
            int: The number of rows deleted
        """
        # Check if the query is valid
        if 'table' not in query or query['table'] not in self.tables:
            return 0

        table = self.tables[query['table']]
        return table.delete(query.get('where'))

    def _execute_create_table(self, query):
        """
        Execute a create table query.

        Args:
            query (dict): The query to execute

        Returns:
            Table: The created table, or None if the table couldn't be created
        """
        # Check if the query is valid
        if 'table' not in query or 'schema' not in query:
            return None

        return self.create_table(query['table'], query['schema'], query.get('order', 5))

    def _execute_drop_table(self, query):
        """
        Execute a drop table query.

        Args:
            query (dict): The query to execute

        Returns:
            bool: True if the table was dropped, False otherwise
        """
        # Check if the query is valid
        if 'table' not in query:
            return False

        return self.drop_table(query['table'])

    def _execute_create_index(self, query):
        """
        Execute a create index query.

        Args:
            query (dict): The query to execute

        Returns:
            bool: True if the index was created, False otherwise
        """
        # Check if the query is valid
        if 'table' not in query or query['table'] not in self.tables or 'column' not in query:
            return False

        table = self.tables[query['table']]
        return table.create_index(query['column'])

    def _execute_drop_index(self, query):
        """
        Execute a drop index query.

        Args:
            query (dict): The query to execute

        Returns:
            bool: True if the index was dropped, False otherwise
        """
        # Check if the query is valid
        if 'table' not in query or query['table'] not in self.tables or 'column' not in query:
            return False

        table = self.tables[query['table']]
        return table.drop_index(query['column'])
