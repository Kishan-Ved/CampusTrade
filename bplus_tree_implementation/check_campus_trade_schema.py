"""
Script to check the schema of the campus_trade database.
"""

from db_engine import Database

def main():
    """Check the schema of the campus_trade database."""
    print("Loading campus_trade database...")
    
    # Load the campus_trade database
    db = Database.load('campus_trade')
    
    if db is None:
        print("Failed to load campus_trade database. Make sure it exists.")
        return
    
    print(f"Database loaded. Tables: {db.list_tables()}")
    
    # Print schema of each table
    for table_name in db.list_tables():
        table = db.tables[table_name]
        print(f"\nTable: {table_name}")
        print("Schema:")
        for column, properties in table.schema.items():
            print(f"  {column}: {properties}")
        
        print("Sample data:")
        if table.rows:
            sample_row = table.rows[0]
            for key, value in sample_row.items():
                print(f"  {key}: {value}")
        else:
            print("  No data")

if __name__ == '__main__':
    main()
