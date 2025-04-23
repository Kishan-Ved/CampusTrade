"""
Frontend application for the B+ Tree database.
"""

import os
import sys
import json

# Add the parent directory to the path so we can import the db_engine module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_engine import Database, BPlusTreeVisualizer

# Try to import Flask, but make it optional
try:
    from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_from_directory
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

# Global database instance
db = None

# Only create Flask app if Flask is available
if FLASK_AVAILABLE:
    app = Flask(__name__)
    app.secret_key = 'bplus_tree_secret_key'

@app.route('/')
def index():
    """Render the index page."""
    available_databases = Database.list_databases()
    return render_template('index.html',
                           tables=db.list_tables() if db else [],
                           available_databases=available_databases)

@app.route('/create_database', methods=['POST'])
def create_database():
    """Create a new database."""
    global db

    name = request.form.get('name')
    if not name:
        flash('Database name is required', 'error')
        return redirect(url_for('index'))

    db = Database(name)
    flash(f'Database {name} created successfully', 'success')
    return redirect(url_for('index'))

@app.route('/load_database', methods=['POST'])
def load_database():
    """Load an existing database."""
    global db

    name = request.form.get('name')
    if not name:
        flash('Database name is required', 'error')
        return redirect(url_for('index'))

    db = Database.load(name)
    if db is None:
        flash(f'Database {name} not found', 'error')
    else:
        flash(f'Database {name} loaded successfully', 'success')

    return redirect(url_for('index'))

@app.route('/save_database', methods=['POST'])
def save_database():
    """Save the current database."""
    if db is None:
        flash('No database is currently loaded', 'error')
        return redirect(url_for('index'))

    if db.save():
        flash(f'Database {db.name} saved successfully', 'success')
    else:
        flash(f'Failed to save database {db.name}', 'error')

    return redirect(url_for('index'))

@app.route('/create_table', methods=['POST'])
def create_table():
    """Create a new table."""
    if db is None:
        flash('No database is currently loaded', 'error')
        return redirect(url_for('index'))

    name = request.form.get('name')
    schema_json = request.form.get('schema')

    if not name or not schema_json:
        flash('Table name and schema are required', 'error')
        return redirect(url_for('index'))

    try:
        schema = json.loads(schema_json)
    except json.JSONDecodeError:
        flash('Invalid schema JSON', 'error')
        return redirect(url_for('index'))

    table = db.create_table(name, schema)
    if table is None:
        flash(f'Table {name} already exists', 'error')
    else:
        flash(f'Table {name} created successfully', 'success')

    return redirect(url_for('index'))

@app.route('/drop_table', methods=['POST'])
def drop_table():
    """Drop a table."""
    if db is None:
        flash('No database is currently loaded', 'error')
        return redirect(url_for('index'))

    name = request.form.get('name')
    if not name:
        flash('Table name is required', 'error')
        return redirect(url_for('index'))

    if db.drop_table(name):
        flash(f'Table {name} dropped successfully', 'success')
    else:
        flash(f'Table {name} not found', 'error')

    return redirect(url_for('index'))

@app.route('/table/<name>')
def view_table(name):
    """View a table."""
    if db is None:
        flash('No database is currently loaded', 'error')
        return redirect(url_for('index'))

    table = db.get_table(name)
    if table is None:
        flash(f'Table {name} not found', 'error')
        return redirect(url_for('index'))

    return render_template('table.html', table=table, rows=table.rows)

@app.route('/table/<name>/insert', methods=['POST'])
def insert_row(name):
    """Insert a row into a table."""
    if db is None:
        flash('No database is currently loaded', 'error')
        return redirect(url_for('index'))

    table = db.get_table(name)
    if table is None:
        flash(f'Table {name} not found', 'error')
        return redirect(url_for('index'))

    row_json = request.form.get('row')
    if not row_json:
        flash('Row data is required', 'error')
        return redirect(url_for('table', name=name))

    try:
        row = json.loads(row_json)
    except json.JSONDecodeError:
        flash('Invalid row JSON', 'error')
        return redirect(url_for('table', name=name))

    if table.insert(row):
        flash('Row inserted successfully', 'success')
    else:
        flash('Failed to insert row', 'error')

    return redirect(url_for('view_table', name=name))

@app.route('/table/<name>/delete', methods=['POST'])
def delete_row(name):
    """Delete a row from a table."""
    if db is None:
        flash('No database is currently loaded', 'error')
        return redirect(url_for('index'))

    table = db.get_table(name)
    if table is None:
        flash(f'Table {name} not found', 'error')
        return redirect(url_for('index'))

    primary_key = request.form.get('primary_key')
    if not primary_key:
        flash('Primary key is required', 'error')
        return redirect(url_for('table', name=name))

    # Convert the primary key to the appropriate type
    try:
        primary_key = int(primary_key)
    except ValueError:
        pass  # Keep it as a string

    # Define a where function to match the primary key
    def where_func(row):
        return row.get(table.primary_key) == primary_key

    count = table.delete(where_func)
    if count > 0:
        flash(f'{count} row(s) deleted successfully', 'success')
    else:
        flash('No rows matched the criteria', 'error')

    return redirect(url_for('view_table', name=name))

@app.route('/table/<name>/update', methods=['POST'])
def update_row(name):
    """Update a row in a table."""
    if db is None:
        flash('No database is currently loaded', 'error')
        return redirect(url_for('index'))

    table = db.get_table(name)
    if table is None:
        flash(f'Table {name} not found', 'error')
        return redirect(url_for('index'))

    primary_key = request.form.get('primary_key')
    set_json = request.form.get('set')

    if not primary_key or not set_json:
        flash('Primary key and set values are required', 'error')
        return redirect(url_for('table', name=name))

    # Convert the primary key to the appropriate type
    try:
        primary_key = int(primary_key)
    except ValueError:
        pass  # Keep it as a string

    try:
        set_values = json.loads(set_json)
    except json.JSONDecodeError:
        flash('Invalid set JSON', 'error')
        return redirect(url_for('table', name=name))

    # Define a where function to match the primary key
    def where_func(row):
        return row.get(table.primary_key) == primary_key

    count = table.update(set_values, where_func)
    if count > 0:
        flash(f'{count} row(s) updated successfully', 'success')
    else:
        flash('No rows matched the criteria', 'error')

    return redirect(url_for('view_table', name=name))

@app.route('/table/<name>/search', methods=['POST'])
def search_table(name):
    """Search a table."""
    if db is None:
        flash('No database is currently loaded', 'error')
        return redirect(url_for('index'))

    table = db.get_table(name)
    if table is None:
        flash(f'Table {name} not found', 'error')
        return redirect(url_for('index'))

    column = request.form.get('column')
    value = request.form.get('value')

    if not column or not value:
        flash('Column and value are required', 'error')
        return redirect(url_for('table', name=name))

    # Convert the value to the appropriate type
    try:
        value = int(value)
    except ValueError:
        pass  # Keep it as a string

    # Check if the column has an index
    if column in table.indices:
        # Use the index for searching
        row = table.select_by_index(column, value)
        if row is not None:
            return render_template('table.html', table=table, rows=[row], search=True)
        else:
            flash('No rows matched the criteria', 'error')
    else:
        # Define a where function to match the column value
        def where_func(row):
            return row.get(column) == value

        rows = table.select(where=where_func)
        if rows:
            return render_template('table.html', table=table, rows=rows, search=True)
        else:
            flash('No rows matched the criteria', 'error')

    return redirect(url_for('view_table', name=name))

@app.route('/table/<name>/range_search', methods=['POST'])
def range_search_table(name):
    """Perform a range search on a table."""
    if db is None:
        flash('No database is currently loaded', 'error')
        return redirect(url_for('index'))

    table = db.get_table(name)
    if table is None:
        flash(f'Table {name} not found', 'error')
        return redirect(url_for('index'))

    column = request.form.get('column')
    start_value = request.form.get('start_value')
    end_value = request.form.get('end_value')

    if not column or not start_value or not end_value:
        flash('Column, start value, and end value are required', 'error')
        return redirect(url_for('table', name=name))

    # Convert the values to the appropriate type
    try:
        start_value = int(start_value)
    except ValueError:
        pass  # Keep it as a string

    try:
        end_value = int(end_value)
    except ValueError:
        pass  # Keep it as a string

    # Check if the column has an index
    if column in table.indices:
        # Use the index for range searching
        rows = table.select_range_by_index(column, start_value, end_value)
        if rows:
            return render_template('table.html', table=table, rows=rows, search=True)
        else:
            flash('No rows matched the criteria', 'error')
    else:
        # Define a where function to match the range
        def where_func(row):
            value = row.get(column)
            return value is not None and start_value <= value <= end_value

        rows = table.select(where=where_func)
        if rows:
            return render_template('table.html', table=table, rows=rows, search=True)
        else:
            flash('No rows matched the criteria', 'error')

    return redirect(url_for('view_table', name=name))

@app.route('/table/<name>/create_index', methods=['POST'])
def create_index(name):
    """Create an index for a column."""
    if db is None:
        flash('No database is currently loaded', 'error')
        return redirect(url_for('index'))

    table = db.get_table(name)
    if table is None:
        flash(f'Table {name} not found', 'error')
        return redirect(url_for('index'))

    column = request.form.get('column')
    if not column:
        flash('Column name is required', 'error')
        return redirect(url_for('view_table', name=name))

    if table.create_index(column):
        flash(f'Index created for column {column}', 'success')
    else:
        flash(f'Failed to create index for column {column}', 'error')

    return redirect(url_for('view_table', name=name))

@app.route('/table/<name>/drop_index', methods=['POST'])
def drop_index(name):
    """Drop an index for a column."""
    if db is None:
        flash('No database is currently loaded', 'error')
        return redirect(url_for('index'))

    table = db.get_table(name)
    if table is None:
        flash(f'Table {name} not found', 'error')
        return redirect(url_for('index'))

    column = request.form.get('column')
    if not column:
        flash('Column name is required', 'error')
        return redirect(url_for('view_table', name=name))

    if table.drop_index(column):
        flash(f'Index dropped for column {column}', 'success')
    else:
        flash(f'Failed to drop index for column {column}', 'error')

    return redirect(url_for('view_table', name=name))

@app.route('/table/<name>/visualize_index', methods=['POST'])
def visualize_index(name):
    """Visualize an index for a column."""
    if db is None:
        flash('No database is currently loaded', 'error')
        return redirect(url_for('index'))

    table = db.get_table(name)
    if table is None:
        flash(f'Table {name} not found', 'error')
        return redirect(url_for('index'))

    column = request.form.get('column')
    if not column:
        flash('Column name is required', 'error')
        return redirect(url_for('view_table', name=name))

    if column not in table.indices:
        flash(f'No index found for column {column}', 'error')
        return redirect(url_for('view_table', name=name))

    # Visualize the B+ Tree
    visualizer = BPlusTreeVisualizer(table.indices[column], f"{name}_{column}_index")
    output_path = visualizer.visualize()

    # Extract the filename from the output path
    filename = os.path.basename(output_path)

    # Return the visualization
    return send_from_directory(os.path.dirname(output_path), filename)

@app.route('/visualizations/<path:filename>')
def visualizations(filename):
    """Serve visualization files."""
    return send_from_directory('visualizations', filename)

def run_app():
    """Run the Flask application if Flask is available."""
    if not FLASK_AVAILABLE:
        print("Flask is not available. Web UI cannot be started.")
        return False

    # Create a default database
    global db
    db = Database('campus_trade')

    # Run the app
    app.run(debug=True)
    return True

if __name__ == '__main__':
    run_app()
