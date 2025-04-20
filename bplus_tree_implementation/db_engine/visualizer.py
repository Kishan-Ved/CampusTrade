"""
Visualizer for B+ Tree using Graphviz.
"""

import os

# Try to import graphviz, but make it optional
try:
    import graphviz
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False

class BPlusTreeVisualizer:
    """Visualizer for B+ Tree using Graphviz."""

    def __init__(self, tree, filename="bplus_tree", directory="visualizations"):
        """
        Initialize a B+ Tree visualizer.

        Args:
            tree (BPlusTree): The B+ Tree to visualize
            filename (str): The filename for the visualization
            directory (str): The directory to save the visualization to
        """
        self.tree = tree
        self.filename = filename
        self.directory = directory

        # Create the directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)

    def visualize(self):
        """
        Visualize the B+ Tree.

        Returns:
            str: The path to the visualization file, or None if graphviz is not available
        """
        if not GRAPHVIZ_AVAILABLE:
            print("Graphviz is not available. Visualization skipped.")
            return None

        # Create a new graph
        dot = graphviz.Digraph(comment="B+ Tree Visualization")

        # Add nodes and edges to the graph
        self._add_nodes_and_edges(dot, self.tree.root)

        # Add leaf node connections
        self._add_leaf_connections(dot)

        # Render the graph
        output_path = dot.render(filename=self.filename, directory=self.directory, format="png", cleanup=True)

        return output_path

    def _add_nodes_and_edges(self, dot, node, node_id=None):
        """
        Add nodes and edges to the graph recursively.

        Args:
            dot (graphviz.Digraph): The graph to add nodes and edges to
            node (Node): The current node
            node_id (str): The ID of the current node

        Returns:
            str: The ID of the current node
        """
        if node_id is None:
            node_id = str(id(node))

        # Add the node to the graph
        if node.is_leaf:
            # Leaf node
            label = "Leaf | " + " | ".join([str(key) for key in node.keys])
            dot.node(node_id, label, shape="record", style="filled", fillcolor="lightblue")
        else:
            # Internal node
            label = "Internal | " + " | ".join([str(key) for key in node.keys])
            dot.node(node_id, label, shape="record")

        # Add edges to children for internal nodes
        if not node.is_leaf:
            for i, child in enumerate(node.children):
                child_id = str(id(child))
                self._add_nodes_and_edges(dot, child, child_id)
                dot.edge(node_id, child_id)

        return node_id

    def _add_leaf_connections(self, dot):
        """
        Add connections between leaf nodes.

        Args:
            dot (graphviz.Digraph): The graph to add connections to
        """
        # Find the leftmost leaf node
        current = self.tree.root
        while not current.is_leaf:
            current = current.children[0]

        # Add connections between leaf nodes
        while current.next_leaf is not None:
            dot.edge(str(id(current)), str(id(current.next_leaf)), style="dashed", color="red")
            current = current.next_leaf
