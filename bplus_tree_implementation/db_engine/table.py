"""
Table implementation for the database.
"""

import json
import os
from .bplus_tree import BPlusTree

class Table:
    """Table class for the database."""
    
    def __init__(self, name, schema, order=5):
        """
        Initialize a table.
        
        Args:
            name (str): The name of the table
            schema (dict): The schema of the table (column name -> data type)
            order (int): The order of the B+ Tree for indexing
        """
        self.name = name
        self.schema = schema
        self.primary_key = None
        self.indices = {}  # column_name -> BPlusTree
        self.rows = []
        self.order = order
        
        # Find the primary key in the schema
        for column, properties in schema.items():
            if properties.get('primary_key', False):
                self.primary_key = column
                # Create an index for the primary key
                self.indices[column] = BPlusTree(order)
                break
        
        # If no primary key is specified, use the first column
        if self.primary_key is None and schema:
            self.primary_key = list(schema.keys())[0]
            self.indices[self.primary_key] = BPlusTree(order)
    
    def create_index(self, column):
        """
        Create an index for a column.
        
        Args:
            column (str): The column to create an index for
            
        Returns:
            bool: True if the index was created, False if it already exists or the column doesn't exist
        """
        if column not in self.schema:
            return False
        
        if column in self.indices:
            return False
        
        # Create a B+ Tree index for the column
        self.indices[column] = BPlusTree(self.order)
        
        # Populate the index with existing data
        for i, row in enumerate(self.rows):
            if column in row:
                self.indices[column].insert(row[column], i)
        
        return True
    
    def drop_index(self, column):
        """
        Drop an index for a column.
        
        Args:
            column (str): The column to drop the index for
            
        Returns:
            bool: True if the index was dropped, False if it doesn't exist or is the primary key
        """
        if column not in self.indices or column == self.primary_key:
            return False
        
        del self.indices[column]
        return True
    
    def insert(self, row):
        """
        Insert a row into the table.
        
        Args:
            row (dict): The row to insert (column name -> value)
            
        Returns:
            bool: True if the row was inserted, False if it violates constraints
        """
        # Check if the row has all required columns
        for column in self.schema:
            if column not in row and not self.schema[column].get('nullable', False):
                return False
        
        # Check if the primary key already exists
        if self.primary_key in row:
            pk_value = row[self.primary_key]
            if self.indices[self.primary_key].search(pk_value) is not None:
                return False
        
        # Add the row to the table
        row_index = len(self.rows)
        self.rows.append(row)
        
        # Update indices
        for column, index in self.indices.items():
            if column in row:
                index.insert(row[column], row_index)
        
        return True
    
    def select(self, columns=None, where=None):
        """
        Select rows from the table.
        
        Args:
            columns (list): The columns to select (None for all)
            where (function): A function that takes a row and returns True if it should be included
            
        Returns:
            list: A list of selected rows
        """
        result = []
        
        # If no columns are specified, select all columns
        if columns is None:
            columns = list(self.schema.keys())
        
        # If no where clause is specified, select all rows
        if where is None:
            for row in self.rows:
                result_row = {column: row.get(column) for column in columns if column in row}
                result.append(result_row)
        else:
            for row in self.rows:
                if where(row):
                    result_row = {column: row.get(column) for column in columns if column in row}
                    result.append(result_row)
        
        return result
    
    def select_by_index(self, column, value):
        """
        Select a row using an index.
        
        Args:
            column (str): The column to search on
            value: The value to search for
            
        Returns:
            dict: The row with the specified value, or None if not found
        """
        if column not in self.indices:
            return None
        
        row_index = self.indices[column].search(value)
        if row_index is None:
            return None
        
        return self.rows[row_index]
    
    def select_range_by_index(self, column, start_value, end_value):
        """
        Select rows in a range using an index.
        
        Args:
            column (str): The column to search on
            start_value: The lower bound of the range (inclusive)
            end_value: The upper bound of the range (inclusive)
            
        Returns:
            list: A list of rows in the specified range
        """
        if column not in self.indices:
            return []
        
        result = []
        range_results = self.indices[column].range_search(start_value, end_value)
        
        for _, row_index in range_results:
            result.append(self.rows[row_index])
        
        return result
    
    def update(self, set_values, where=None):
        """
        Update rows in the table.
        
        Args:
            set_values (dict): The values to set (column name -> value)
            where (function): A function that takes a row and returns True if it should be updated
            
        Returns:
            int: The number of rows updated
        """
        count = 0
        
        # If no where clause is specified, update all rows
        if where is None:
            for i, row in enumerate(self.rows):
                # Update indices for changed values
                for column, value in set_values.items():
                    if column in self.indices and column in row:
                        # Remove the old value from the index
                        self.indices[column].delete(row[column])
                        # Add the new value to the index
                        self.indices[column].insert(value, i)
                
                # Update the row
                row.update(set_values)
                count += 1
        else:
            for i, row in enumerate(self.rows):
                if where(row):
                    # Update indices for changed values
                    for column, value in set_values.items():
                        if column in self.indices and column in row:
                            # Remove the old value from the index
                            self.indices[column].delete(row[column])
                            # Add the new value to the index
                            self.indices[column].insert(value, i)
                    
                    # Update the row
                    row.update(set_values)
                    count += 1
        
        return count
    
    def delete(self, where=None):
        """
        Delete rows from the table.
        
        Args:
            where (function): A function that takes a row and returns True if it should be deleted
            
        Returns:
            int: The number of rows deleted
        """
        count = 0
        new_rows = []
        
        # If no where clause is specified, delete all rows
        if where is None:
            count = len(self.rows)
            # Clear all indices
            for index in self.indices.values():
                index.clear()
            self.rows = []
        else:
            # Keep track of rows to keep
            for i, row in enumerate(self.rows):
                if where(row):
                    # Remove the row from indices
                    for column, index in self.indices.items():
                        if column in row:
                            index.delete(row[column])
                    count += 1
                else:
                    new_rows.append(row)
            
            # Rebuild indices for the remaining rows
            if count > 0:
                self.rows = new_rows
                for column, index in self.indices.items():
                    index.clear()
                    for i, row in enumerate(self.rows):
                        if column in row:
                            index.insert(row[column], i)
        
        return count
    
    def count(self, where=None):
        """
        Count rows in the table.
        
        Args:
            where (function): A function that takes a row and returns True if it should be counted
            
        Returns:
            int: The number of rows that match the condition
        """
        if where is None:
            return len(self.rows)
        
        count = 0
        for row in self.rows:
            if where(row):
                count += 1
        
        return count
    
    def aggregate(self, column, function, where=None):
        """
        Perform an aggregation on a column.
        
        Args:
            column (str): The column to aggregate
            function (str): The aggregation function ('sum', 'avg', 'min', 'max', 'count')
            where (function): A function that takes a row and returns True if it should be included
            
        Returns:
            The result of the aggregation, or None if no rows match
        """
        values = []
        
        # Collect values that match the condition
        for row in self.rows:
            if column in row and (where is None or where(row)):
                values.append(row[column])
        
        # If no values match, return None
        if not values:
            return None
        
        # Perform the aggregation
        if function == 'sum':
            return sum(values)
        elif function == 'avg':
            return sum(values) / len(values)
        elif function == 'min':
            return min(values)
        elif function == 'max':
            return max(values)
        elif function == 'count':
            return len(values)
        else:
            return None
    
    def save_to_file(self, directory):
        """
        Save the table to a file.
        
        Args:
            directory (str): The directory to save the table to
            
        Returns:
            bool: True if the table was saved successfully, False otherwise
        """
        try:
            # Create the directory if it doesn't exist
            os.makedirs(directory, exist_ok=True)
            
            # Save the table metadata
            metadata = {
                'name': self.name,
                'schema': self.schema,
                'primary_key': self.primary_key,
                'order': self.order
            }
            
            with open(os.path.join(directory, f"{self.name}_metadata.json"), 'w') as f:
                json.dump(metadata, f, indent=2)
            
            # Save the table data
            with open(os.path.join(directory, f"{self.name}_data.json"), 'w') as f:
                json.dump(self.rows, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving table {self.name}: {e}")
            return False
    
    @classmethod
    def load_from_file(cls, directory, name):
        """
        Load a table from a file.
        
        Args:
            directory (str): The directory to load the table from
            name (str): The name of the table
            
        Returns:
            Table: The loaded table, or None if the table couldn't be loaded
        """
        try:
            # Load the table metadata
            with open(os.path.join(directory, f"{name}_metadata.json"), 'r') as f:
                metadata = json.load(f)
            
            # Create a new table
            table = cls(metadata['name'], metadata['schema'], metadata['order'])
            table.primary_key = metadata['primary_key']
            
            # Load the table data
            with open(os.path.join(directory, f"{name}_data.json"), 'r') as f:
                rows = json.load(f)
            
            # Insert the rows
            for row in rows:
                table.insert(row)
            
            return table
        except Exception as e:
            print(f"Error loading table {name}: {e}")
            return None
