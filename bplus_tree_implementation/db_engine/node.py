"""
Node classes for B+ Tree implementation.
"""

class Node:
    """Base Node class for B+ Tree."""
    
    def __init__(self, order):
        """
        Initialize a node in B+ Tree.
        
        Args:
            order (int): The order of the B+ Tree (maximum number of children)
        """
        self.order = order
        self.keys = []
        self.parent = None
        self.is_leaf = False
    
    def is_root(self):
        """Check if the node is a root node."""
        return self.parent is None
    
    def is_full(self):
        """Check if the node is full (has maximum number of keys)."""
        return len(self.keys) >= self.order - 1


class InternalNode(Node):
    """Internal node class for B+ Tree."""
    
    def __init__(self, order):
        """
        Initialize an internal node.
        
        Args:
            order (int): The order of the B+ Tree
        """
        super().__init__(order)
        self.children = []
    
    def insert_key(self, key, left_child, right_child):
        """
        Insert a key and its children into the internal node.
        
        Args:
            key: The key to insert
            left_child: The left child node
            right_child: The right child node
        """
        # Find the position to insert the key
        i = 0
        while i < len(self.keys) and key > self.keys[i]:
            i += 1
        
        # Insert the key and update children
        self.keys.insert(i, key)
        
        # If this is a new split, we need to replace the old child with left_child
        # and insert right_child
        if right_child not in self.children:
            if left_child in self.children:
                idx = self.children.index(left_child)
                self.children[idx] = left_child
                self.children.insert(idx + 1, right_child)
            else:
                # This case should not happen in normal operation
                self.children.insert(i, left_child)
                self.children.insert(i + 1, right_child)
        
        # Update parent references
        left_child.parent = self
        right_child.parent = self
    
    def split(self):
        """
        Split the internal node when it's full.
        
        Returns:
            tuple: (median_key, left_node, right_node)
        """
        mid = len(self.keys) // 2
        
        # Create a new internal node for the right half
        right_node = InternalNode(self.order)
        right_node.keys = self.keys[mid+1:]
        right_node.children = self.children[mid+1:]
        
        # Update parent references for children of the right node
        for child in right_node.children:
            child.parent = right_node
        
        # Get the median key that will be pushed up
        median_key = self.keys[mid]
        
        # Update the current node to be the left node
        self.keys = self.keys[:mid]
        self.children = self.children[:mid+1]
        
        return median_key, self, right_node
    
    def find_child(self, key):
        """
        Find the appropriate child node for a given key.
        
        Args:
            key: The key to search for
            
        Returns:
            Node: The child node where the key should be located
        """
        i = 0
        while i < len(self.keys) and key >= self.keys[i]:
            i += 1
        return self.children[i]


class LeafNode(Node):
    """Leaf node class for B+ Tree."""
    
    def __init__(self, order):
        """
        Initialize a leaf node.
        
        Args:
            order (int): The order of the B+ Tree
        """
        super().__init__(order)
        self.values = []
        self.next_leaf = None
        self.is_leaf = True
    
    def insert_key_value(self, key, value):
        """
        Insert a key-value pair into the leaf node.
        
        Args:
            key: The key to insert
            value: The value associated with the key
            
        Returns:
            bool: True if the key was inserted, False if it already exists
        """
        # Find the position to insert the key
        i = 0
        while i < len(self.keys) and key > self.keys[i]:
            i += 1
        
        # Check if the key already exists
        if i < len(self.keys) and key == self.keys[i]:
            # Update the value if the key already exists
            self.values[i] = value
            return False
        
        # Insert the key and value
        self.keys.insert(i, key)
        self.values.insert(i, value)
        return True
    
    def split(self):
        """
        Split the leaf node when it's full.
        
        Returns:
            tuple: (median_key, left_node, right_node)
        """
        mid = len(self.keys) // 2
        
        # Create a new leaf node for the right half
        right_node = LeafNode(self.order)
        right_node.keys = self.keys[mid:]
        right_node.values = self.values[mid:]
        
        # Update the current node to be the left node
        self.keys = self.keys[:mid]
        self.values = self.values[:mid]
        
        # Link the leaves
        right_node.next_leaf = self.next_leaf
        self.next_leaf = right_node
        
        # The median key is the first key in the right node (for leaf nodes)
        median_key = right_node.keys[0]
        
        return median_key, self, right_node
    
    def get_value(self, key):
        """
        Get the value associated with a key.
        
        Args:
            key: The key to search for
            
        Returns:
            The value associated with the key, or None if the key is not found
        """
        for i, k in enumerate(self.keys):
            if k == key:
                return self.values[i]
        return None
    
    def remove_key(self, key):
        """
        Remove a key and its associated value from the leaf node.
        
        Args:
            key: The key to remove
            
        Returns:
            bool: True if the key was removed, False if it wasn't found
        """
        for i, k in enumerate(self.keys):
            if k == key:
                self.keys.pop(i)
                self.values.pop(i)
                return True
        return False
