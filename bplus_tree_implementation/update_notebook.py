"""
Script to update the implementation report notebook with the indexing performance section.
"""

import json
import os

def main():
    """Update the implementation report notebook."""
    # Path to the notebook
    notebook_path = 'docs/implementation_report.ipynb'
    
    # Path to the indexing performance section
    section_path = 'docs/indexing_performance_section.md'
    
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
        "source": [section_content]
    }
    
    # Find the position to insert the new cell
    # We'll insert it after the "Range Search Performance" section
    insert_position = None
    for i, cell in enumerate(notebook['cells']):
        if cell['cell_type'] == 'markdown' and '### 4.3 Range Search Performance' in ''.join(cell['source']):
            # Insert after this cell and the next code cell
            insert_position = i + 2
            break
    
    if insert_position is None:
        # If we couldn't find the right position, append to the end
        notebook['cells'].append(new_cell)
    else:
        # Insert at the found position
        notebook['cells'].insert(insert_position, new_cell)
    
    # Save the updated notebook
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1)
    
    print(f"Updated {notebook_path} with the indexing performance section")

if __name__ == '__main__':
    main()
