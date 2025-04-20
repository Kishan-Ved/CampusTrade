"""
Brute Force Database implementation for comparison with B+ Tree.
"""

class BruteForceDB:
    """
    A simple brute force database implementation for comparison with B+ Tree.
    Uses a dictionary to store key-value pairs and performs linear search for range queries.
    """
    
    def __init__(self):
        """Initialize a brute force database."""
        self.data = {}
    
    def insert(self, key, value):
        """
        Insert a key-value pair into the database.
        
        Args:
            key: The key to insert
            value: The value associated with the key
            
        Returns:
            bool: True if the key was inserted, False if it was updated
        """
        is_new = key not in self.data
        self.data[key] = value
        return is_new
    
    def search(self, key):
        """
        Search for a key in the database.
        
        Args:
            key: The key to search for
            
        Returns:
            The value associated with the key, or None if the key is not found
        """
        return self.data.get(key)
    
    def range_search(self, start_key, end_key):
        """
        Perform a range search in the database.
        
        Args:
            start_key: The lower bound of the range (inclusive)
            end_key: The upper bound of the range (inclusive)
            
        Returns:
            list: A list of (key, value) pairs in the specified range
        """
        result = []
        for key, value in self.data.items():
            if start_key <= key <= end_key:
                result.append((key, value))
        return sorted(result)  # Sort by key for consistent results
    
    def delete(self, key):
        """
        Delete a key from the database.
        
        Args:
            key: The key to delete
            
        Returns:
            bool: True if the key was deleted, False if it wasn't found
        """
        if key in self.data:
            del self.data[key]
            return True
        return False
    
    def update(self, key, value):
        """
        Update the value associated with a key.
        
        Args:
            key: The key to update
            value: The new value
            
        Returns:
            bool: True if the key was updated, False if it wasn't found
        """
        if key in self.data:
            self.data[key] = value
            return True
        return False
    
    def size(self):
        """
        Get the number of key-value pairs in the database.
        
        Returns:
            int: The number of key-value pairs
        """
        return len(self.data)
    
    def is_empty(self):
        """
        Check if the database is empty.
        
        Returns:
            bool: True if the database is empty, False otherwise
        """
        return len(self.data) == 0
    
    def clear(self):
        """Clear the database."""
        self.data.clear()
    
    def get_all_key_values(self):
        """
        Get all key-value pairs in the database.
        
        Returns:
            list: A list of (key, value) pairs
        """
        return sorted(self.data.items())  # Sort by key for consistent results
