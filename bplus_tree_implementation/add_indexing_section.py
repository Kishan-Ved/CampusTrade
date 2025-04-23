"""
Script to add the indexing performance section to the implementation report notebook.
"""

import json

def main():
    """Add the indexing performance section to the notebook."""
    # Path to the notebook in the main directory
    notebook_path = 'implementation_report.ipynb'
    
    # Path to the indexing performance section
    section_path = 'indexing_performance_section.md'
    
    # Read the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Read the indexing performance section
    with open(section_path, 'r', encoding='utf-8') as f:
        section_content = f.read()
    
    # Create a new markdown cell with the section content
    new_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": section_content
    }
    
    # Add the new cell to the notebook
    notebook['cells'].append(new_cell)
    
    # Save the updated notebook
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1)
    
    print(f"Added indexing performance section to {notebook_path}")

if __name__ == '__main__':
    main()
