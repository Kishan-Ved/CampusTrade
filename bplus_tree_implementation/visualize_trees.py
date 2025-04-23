"""
Script to visualize B+ Trees with different structures.
"""

import os
from db_engine import BPlusTree, BPlusTreeVisualizer

def visualize_small_tree():
    """Create and visualize a small B+ Tree."""
    # Create a B+ Tree with order 3 (minimum for B+ Tree)
    tree = BPlusTree(order=3)
    
    # Insert some key-value pairs
    keys = [5, 8, 1, 3, 9, 6]
    for key in keys:
        tree.insert(key, f'value_{key}')
    
    # Visualize the tree
    visualizer = BPlusTreeVisualizer(tree, 'small_tree')
    output_path = visualizer.visualize()
    
    print(f'Small tree visualization saved to: {output_path}')
    return output_path

def visualize_medium_tree():
    """Create and visualize a medium-sized B+ Tree."""
    # Create a B+ Tree with order 4
    tree = BPlusTree(order=4)
    
    # Insert some key-value pairs
    keys = [5, 8, 1, 3, 9, 6, 7, 2, 4, 10, 11, 12]
    for key in keys:
        tree.insert(key, f'value_{key}')
    
    # Visualize the tree
    visualizer = BPlusTreeVisualizer(tree, 'medium_tree')
    output_path = visualizer.visualize()
    
    print(f'Medium tree visualization saved to: {output_path}')
    return output_path

def visualize_large_tree():
    """Create and visualize a larger B+ Tree."""
    # Create a B+ Tree with order 5
    tree = BPlusTree(order=5)
    
    # Insert some key-value pairs
    keys = list(range(1, 31))  # 1 to 30
    for key in keys:
        tree.insert(key, f'value_{key}')
    
    # Visualize the tree
    visualizer = BPlusTreeVisualizer(tree, 'large_tree')
    output_path = visualizer.visualize()
    
    print(f'Large tree visualization saved to: {output_path}')
    return output_path

def visualize_after_operations():
    """Create a tree, perform operations, and visualize it."""
    # Create a B+ Tree with order 4
    tree = BPlusTree(order=4)
    
    # Insert some key-value pairs
    keys = [5, 8, 1, 3, 9, 6, 7, 2, 4]
    for key in keys:
        tree.insert(key, f'value_{key}')
    
    # Perform some operations
    tree.delete(3)  # Delete a key
    tree.delete(6)  # Delete another key
    tree.update(5, 'updated_value_5')  # Update a value
    tree.insert(10, 'value_10')  # Insert a new key
    
    # Visualize the tree
    visualizer = BPlusTreeVisualizer(tree, 'after_operations')
    output_path = visualizer.visualize()
    
    print(f'Tree after operations visualization saved to: {output_path}')
    return output_path

def main():
    """Generate all visualizations."""
    # Create visualizations directory if it doesn't exist
    os.makedirs('visualizations', exist_ok=True)
    
    # Generate visualizations
    small_tree_path = visualize_small_tree()
    medium_tree_path = visualize_medium_tree()
    large_tree_path = visualize_large_tree()
    after_operations_path = visualize_after_operations()
    
    print("\nAll visualizations completed!")
    print("You can find the visualizations in the 'visualizations' directory.")

if __name__ == '__main__':
    main()
