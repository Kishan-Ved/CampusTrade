"""
Unit tests for the B+ Tree implementation.
"""

import os
import sys
import unittest

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_engine import BPlusTree

class TestBPlusTree(unittest.TestCase):
    """Test cases for the B+ Tree implementation."""
    
    def setUp(self):
        """Set up a B+ Tree for testing."""
        self.tree = BPlusTree(order=5)
    
    def test_insert_and_search(self):
        """Test inserting and searching for keys."""
        # Insert some key-value pairs
        self.tree.insert(10, "value_10")
        self.tree.insert(20, "value_20")
        self.tree.insert(5, "value_5")
        self.tree.insert(15, "value_15")
        
        # Search for keys
        self.assertEqual(self.tree.search(10), "value_10")
        self.assertEqual(self.tree.search(20), "value_20")
        self.assertEqual(self.tree.search(5), "value_5")
        self.assertEqual(self.tree.search(15), "value_15")
        
        # Search for a non-existent key
        self.assertIsNone(self.tree.search(30))
    
    def test_update(self):
        """Test updating values."""
        # Insert a key-value pair
        self.tree.insert(10, "value_10")
        
        # Update the value
        self.tree.update(10, "new_value_10")
        
        # Check the updated value
        self.assertEqual(self.tree.search(10), "new_value_10")
        
        # Update a non-existent key
        self.assertFalse(self.tree.update(30, "value_30"))
    
    def test_delete(self):
        """Test deleting keys."""
        # Insert some key-value pairs
        self.tree.insert(10, "value_10")
        self.tree.insert(20, "value_20")
        self.tree.insert(5, "value_5")
        
        # Delete a key
        self.assertTrue(self.tree.delete(10))
        
        # Check that the key is deleted
        self.assertIsNone(self.tree.search(10))
        
        # Delete a non-existent key
        self.assertFalse(self.tree.delete(30))
    
    def test_range_search(self):
        """Test range search."""
        # Insert some key-value pairs
        self.tree.insert(10, "value_10")
        self.tree.insert(20, "value_20")
        self.tree.insert(5, "value_5")
        self.tree.insert(15, "value_15")
        self.tree.insert(25, "value_25")
        
        # Perform a range search
        result = self.tree.range_search(10, 20)
        
        # Check the result
        self.assertEqual(len(result), 3)
        self.assertIn((10, "value_10"), result)
        self.assertIn((15, "value_15"), result)
        self.assertIn((20, "value_20"), result)
    
    def test_get_all_key_values(self):
        """Test getting all key-value pairs."""
        # Insert some key-value pairs
        self.tree.insert(10, "value_10")
        self.tree.insert(20, "value_20")
        self.tree.insert(5, "value_5")
        
        # Get all key-value pairs
        result = self.tree.get_all_key_values()
        
        # Check the result
        self.assertEqual(len(result), 3)
        self.assertIn((5, "value_5"), result)
        self.assertIn((10, "value_10"), result)
        self.assertIn((20, "value_20"), result)
    
    def test_size_and_is_empty(self):
        """Test size and is_empty methods."""
        # Check that the tree is empty
        self.assertTrue(self.tree.is_empty())
        self.assertEqual(self.tree.size(), 0)
        
        # Insert some key-value pairs
        self.tree.insert(10, "value_10")
        self.tree.insert(20, "value_20")
        
        # Check that the tree is not empty
        self.assertFalse(self.tree.is_empty())
        self.assertEqual(self.tree.size(), 2)
        
        # Delete a key
        self.tree.delete(10)
        
        # Check the size
        self.assertEqual(self.tree.size(), 1)
        
        # Clear the tree
        self.tree.clear()
        
        # Check that the tree is empty
        self.assertTrue(self.tree.is_empty())
        self.assertEqual(self.tree.size(), 0)
    
    def test_node_splitting(self):
        """Test node splitting when a node is full."""
        # Insert enough keys to cause node splitting
        keys = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        for key in keys:
            self.tree.insert(key, f"value_{key}")
        
        # Check that all keys can be found
        for key in keys:
            self.assertEqual(self.tree.search(key), f"value_{key}")

if __name__ == '__main__':
    unittest.main()
