"""
Script to check if the implementation report notebook contains the indexing performance section.
"""

import json

def main():
    """Check if the notebook contains the indexing performance section."""
    # Path to the notebook in the main directory
    notebook_path = 'implementation_report.ipynb'
    
    # Read the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Print the total number of cells
    print(f"Total cells in notebook: {len(notebook['cells'])}")
    
    # Check for the indexing performance section
    found = False
    for i, cell in enumerate(notebook['cells']):
        if cell['cell_type'] == 'markdown':
            source = cell.get('source', '')
            if isinstance(source, list):
                source = ''.join(source)
            if '# 5. Indexing Performance on Campus Trade Database' in source:
                print(f"Found indexing performance section at cell {i}")
                found = True
                break
    
    if not found:
        print("Indexing performance section not found in the notebook")

if __name__ == '__main__':
    main()
