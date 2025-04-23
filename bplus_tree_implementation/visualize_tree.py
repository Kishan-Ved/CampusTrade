"""
Script to visualize a sample B+ Tree.
"""

from db_engine import BPlusTree, BPlusTreeVisualizer

def main():
    """Create and visualize a sample B+ Tree."""
    # Create a B+ Tree
    tree = BPlusTree(order=5)
    
    # Insert some key-value pairs
    for i in range(10):
        tree.insert(i, f'value_{i}')
    
    # Visualize the tree
    visualizer = BPlusTreeVisualizer(tree, 'sample_tree')
    output_path = visualizer.visualize()
    
    print(f'Tree visualization saved to: {output_path}')

if __name__ == '__main__':
    main()
