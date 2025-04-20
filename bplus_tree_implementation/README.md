# B+ Tree Database Implementation

This project implements a lightweight database management system (DBMS) in Python that uses a B+ Tree for indexing and supports core database operations like insert, update, delete, select, aggregation, and range queries.

## Features

- B+ Tree implementation with automatic node splitting, merging, exact search, and range queries
- Database class for managing tables and operations
- Table class for handling table operations with B+ Tree indexing
- BruteForceDB implementation for performance comparison
- Benchmarking utilities for measuring time and memory usage
- Visualization of B+ Tree structure using Graphviz
- Web-based UI for interacting with the database

## Directory Structure

```
bplus_tree_implementation/
├── db_engine/                  # Core database engine implementation
│   ├── __init__.py             # Package initialization
│   ├── bplus_tree.py           # B+ Tree implementation
│   ├── brute_force_db.py       # BruteForceDB implementation
│   ├── database.py             # Database class
│   ├── node.py                 # Node classes for B+ Tree
│   ├── table.py                # Table class
│   ├── visualizer.py           # B+ Tree visualization
│   └── benchmarking.py         # Benchmarking utilities
├── frontend/                   # Web-based UI
│   ├── app.py                  # Flask application
│   ├── static/                 # Static files (CSS, JS)
│   └── templates/              # HTML templates
├── docs/                       # Documentation
│   └── implementation_report.ipynb  # Jupyter notebook report
├── tests/                      # Tests
├── data/                       # Database files
├── visualizations/             # B+ Tree visualizations
├── benchmarks/                 # Benchmark results
├── init_database.py            # Database initialization script
├── main.py                     # Main script to run the application
└── README.md                   # Project documentation
```

## Requirements

- Python 3.6+
- Flask
- Graphviz
- Matplotlib
- NumPy
- Jupyter Notebook (for the report)

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd bplus_tree_implementation
   ```

2. Install the required packages:
   ```
   pip install flask graphviz matplotlib numpy jupyter
   ```

3. Install Graphviz (for visualization):
   - On Windows: Download and install from https://graphviz.org/download/
   - On macOS: `brew install graphviz`
   - On Ubuntu/Debian: `sudo apt-get install graphviz`

## Usage

### Initialize the Database

```
python main.py --init
```

This will create a new database with sample tables and data based on the CampusTrade schema.

### Run the Web Application

```
python main.py --run
```

This will start the Flask web application. Open a web browser and navigate to http://localhost:5000 to access the UI.

### Run Benchmarks

```
python main.py --benchmark
```

This will run benchmarks for insert, search, range search, and delete operations on both B+ Tree and BruteForceDB implementations. The results will be saved to the `benchmarks` directory.

## Implementation Details

### B+ Tree

The B+ Tree implementation consists of the following components:

- `Node` class: Base class for nodes in the B+ Tree
- `InternalNode` class: Class for internal nodes in the B+ Tree
- `LeafNode` class: Class for leaf nodes in the B+ Tree
- `BPlusTree` class: Main class that implements the B+ Tree data structure

### Database

The database implementation consists of the following components:

- `Table` class: Manages table operations and uses B+ Tree for indexing
- `Database` class: Manages tables and provides a query interface

### Web UI

The web UI provides a user-friendly interface for interacting with the database. It supports the following operations:

- Create and load databases
- Create and drop tables
- Insert, update, and delete rows
- Search and range search
- Create and drop indices
- Visualize B+ Tree indices

## Report

The implementation report is available as a Jupyter notebook in the `docs` directory. It covers the following topics:

- B+ Tree implementation
- Database implementation
- Performance benchmarking
- CampusTrade database implementation

To view the report, run:

```
jupyter notebook docs/implementation_report.ipynb
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
