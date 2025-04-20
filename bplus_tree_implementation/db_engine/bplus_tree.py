"""
B+ Tree implementation for indexing in the database.
"""

from .node import InternalNode, LeafNode

class BPlusTree:
    """B+ Tree implementation for efficient indexing and range queries."""
    
    def __init__(self, order=5):
        """
        Initialize a B+ Tree.
        
        Args:
            order (int): The order of the B+ Tree (maximum number of children per node)
        """
        self.root = LeafNode(order)
        self.order = order
        self._size = 0
    
    def insert(self, key, value):
        """
        Insert a key-value pair into the B+ Tree.
        
        Args:
            key: The key to insert
            value: The value associated with the key
            
        Returns:
            bool: True if the key was inserted, False if it was updated
        """
        # Find the leaf node where the key should be inserted
        leaf_node = self._find_leaf(key)
        
        # Insert the key-value pair into the leaf node
        inserted = leaf_node.insert_key_value(key, value)
        
        # If the key was inserted (not updated), increment the size
        if inserted:
            self._size += 1
        
        # If the leaf node is full, split it
        if leaf_node.is_full():
            self._split_leaf(leaf_node)
        
        return inserted
    
    def _find_leaf(self, key):
        """
        Find the leaf node where a key should be located.
        
        Args:
            key: The key to search for
            
        Returns:
            LeafNode: The leaf node where the key should be located
        """
        current = self.root
        
        # Traverse the tree until we reach a leaf node
        while not current.is_leaf:
            current = current.find_child(key)
        
        return current
    
    def _split_leaf(self, leaf_node):
        """
        Split a leaf node and propagate changes up the tree.
        
        Args:
            leaf_node (LeafNode): The leaf node to split
        """
        # Split the leaf node
        median_key, left_node, right_node = leaf_node.split()
        
        # If the leaf node is the root, create a new root
        if leaf_node.is_root():
            new_root = InternalNode(self.order)
            new_root.keys = [median_key]
            new_root.children = [left_node, right_node]
            left_node.parent = new_root
            right_node.parent = new_root
            self.root = new_root
        else:
            # Insert the median key into the parent node
            parent = leaf_node.parent
            parent.insert_key(median_key, left_node, right_node)
            
            # If the parent node is full, split it
            if parent.is_full():
                self._split_internal(parent)
    
    def _split_internal(self, internal_node):
        """
        Split an internal node and propagate changes up the tree.
        
        Args:
            internal_node (InternalNode): The internal node to split
        """
        # Split the internal node
        median_key, left_node, right_node = internal_node.split()
        
        # If the internal node is the root, create a new root
        if internal_node.is_root():
            new_root = InternalNode(self.order)
            new_root.keys = [median_key]
            new_root.children = [left_node, right_node]
            left_node.parent = new_root
            right_node.parent = new_root
            self.root = new_root
        else:
            # Insert the median key into the parent node
            parent = internal_node.parent
            parent.insert_key(median_key, left_node, right_node)
            
            # If the parent node is full, split it
            if parent.is_full():
                self._split_internal(parent)
    
    def search(self, key):
        """
        Search for a key in the B+ Tree.
        
        Args:
            key: The key to search for
            
        Returns:
            The value associated with the key, or None if the key is not found
        """
        leaf_node = self._find_leaf(key)
        return leaf_node.get_value(key)
    
    def range_search(self, start_key, end_key):
        """
        Perform a range search in the B+ Tree.
        
        Args:
            start_key: The lower bound of the range (inclusive)
            end_key: The upper bound of the range (inclusive)
            
        Returns:
            list: A list of (key, value) pairs in the specified range
        """
        result = []
        
        # Find the leaf node where the start key should be located
        current = self._find_leaf(start_key)
        
        # Traverse the leaf nodes and collect keys and values in the range
        while current is not None:
            for i, key in enumerate(current.keys):
                if start_key <= key <= end_key:
                    result.append((key, current.values[i]))
            
            # If we've found keys greater than the end key, we're done
            if current.keys and current.keys[-1] > end_key:
                break
            
            # Move to the next leaf node
            current = current.next_leaf
        
        return result
    
    def delete(self, key):
        """
        Delete a key from the B+ Tree.
        
        Args:
            key: The key to delete
            
        Returns:
            bool: True if the key was deleted, False if it wasn't found
        """
        # Find the leaf node where the key should be located
        leaf_node = self._find_leaf(key)
        
        # Remove the key from the leaf node
        deleted = leaf_node.remove_key(key)
        
        # If the key was deleted, decrement the size
        if deleted:
            self._size -= 1
            
            # TODO: Handle underflow (merging nodes)
            # This is a simplified implementation that doesn't handle node merging
        
        return deleted
    
    def update(self, key, value):
        """
        Update the value associated with a key.
        
        Args:
            key: The key to update
            value: The new value
            
        Returns:
            bool: True if the key was updated, False if it wasn't found
        """
        # Find the leaf node where the key should be located
        leaf_node = self._find_leaf(key)
        
        # Check if the key exists
        for i, k in enumerate(leaf_node.keys):
            if k == key:
                leaf_node.values[i] = value
                return True
        
        return False
    
    def size(self):
        """
        Get the number of key-value pairs in the B+ Tree.
        
        Returns:
            int: The number of key-value pairs
        """
        return self._size
    
    def is_empty(self):
        """
        Check if the B+ Tree is empty.
        
        Returns:
            bool: True if the B+ Tree is empty, False otherwise
        """
        return self._size == 0
    
    def clear(self):
        """Clear the B+ Tree."""
        self.root = LeafNode(self.order)
        self._size = 0
    
    def get_all_key_values(self):
        """
        Get all key-value pairs in the B+ Tree.
        
        Returns:
            list: A list of (key, value) pairs
        """
        result = []
        
        # Start from the leftmost leaf node
        current = self.root
        while not current.is_leaf:
            current = current.children[0]
        
        # Traverse all leaf nodes
        while current is not None:
            for i, key in enumerate(current.keys):
                result.append((key, current.values[i]))
            current = current.next_leaf
        
        return result
