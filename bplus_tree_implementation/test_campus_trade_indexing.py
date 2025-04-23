"""
Script to test indexing performance on the campus_trade database.
"""

import time
import random
import os
import matplotlib.pyplot as plt
from db_engine import Database

def measure_search_performance(table, column, values, num_searches=50):
    """Measure search performance with and without an index."""
    # Select random values to search for
    search_values = random.sample(values, min(num_searches, len(values)))
    
    # Measure non-indexed search time
    start_time = time.time()
    
    for value in search_values:
        # Define a where function to match the column value
        def where_func(row):
            return row.get(column) == value
        
        # Perform a non-indexed search
        table.select(where=where_func)
    
    non_indexed_time = time.time() - start_time
    
    # Create an index on the column if it doesn't exist and it's not the primary key
    if column not in table.indices and column != table.primary_key:
        print(f"  Creating index on {column}...")
        table.create_index(column)
    
    # Measure indexed search time
    start_time = time.time()
    
    for value in search_values:
        # Perform an indexed search
        table.select_by_index(column, value)
    
    indexed_time = time.time() - start_time
    
    # Drop the index if we created it
    if column != table.primary_key:
        table.drop_index(column)
    
    return non_indexed_time, indexed_time

def test_table_indexing(table, columns_to_test):
    """Test indexing performance on specific columns of a table."""
    results = {}
    
    print(f"Testing indexing performance on table: {table.name}")
    
    for column in columns_to_test:
        # Skip if column doesn't exist in the table
        if column not in table.schema:
            print(f"  Column {column} not found in table {table.name}")
            continue
        
        # Get unique values for the column
        values = set()
        for row in table.rows:
            if column in row:
                values.add(row[column])
        
        values = list(values)
        
        if not values:
            print(f"  No values found for column {column}")
            continue
        
        print(f"  Testing column: {column} (found {len(values)} unique values)")
        
        # Measure search performance
        non_indexed_time, indexed_time = measure_search_performance(table, column, values)
        
        # Calculate speedup
        speedup = non_indexed_time / indexed_time if indexed_time > 0 else float('inf')
        
        results[column] = {
            'non_indexed': non_indexed_time,
            'indexed': indexed_time,
            'speedup': speedup
        }
        
        print(f"    Non-indexed: {non_indexed_time:.6f}s, Indexed: {indexed_time:.6f}s")
        print(f"    Speedup: {speedup:.2f}x")
    
    return results

def plot_results(results, output_file):
    """Plot the indexing performance results."""
    # Prepare data for plotting
    columns = list(results.keys())
    non_indexed_times = [results[col]['non_indexed'] for col in columns]
    indexed_times = [results[col]['indexed'] for col in columns]
    speedups = [results[col]['speedup'] for col in columns]
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Plot search times
    x = range(len(columns))
    width = 0.35
    
    ax1.bar([i - width/2 for i in x], non_indexed_times, width, label='Non-indexed')
    ax1.bar([i + width/2 for i in x], indexed_times, width, label='Indexed')
    
    ax1.set_xlabel('Column')
    ax1.set_ylabel('Time (seconds)')
    ax1.set_title('Search Time Comparison')
    ax1.set_xticks(x)
    ax1.set_xticklabels(columns)
    ax1.legend()
    ax1.grid(True, axis='y')
    
    # Plot speedups
    ax2.bar(x, speedups, width=0.6)
    
    ax2.set_xlabel('Column')
    ax2.set_ylabel('Speedup (x times)')
    ax2.set_title('Indexing Speedup')
    ax2.set_xticks(x)
    ax2.set_xticklabels(columns)
    ax2.grid(True, axis='y')
    
    # Add speedup values on top of bars
    for i, v in enumerate(speedups):
        ax2.text(i, v + 0.5, f"{v:.2f}x", ha='center')
    
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
    
    return output_file

def main():
    """Test indexing performance on the campus_trade database."""
    print("Loading campus_trade database...")
    
    # Load the campus_trade database
    db = Database.load('campus_trade')
    
    if db is None:
        print("Failed to load campus_trade database. Make sure it exists.")
        return
    
    print(f"Database loaded. Tables: {db.list_tables()}")
    
    # Create output directory
    os.makedirs('campus_trade_indexing', exist_ok=True)
    
    # Test indexing on memberExt table
    if 'memberExt' in db.tables:
        member_table = db.tables['memberExt']
        member_results = test_table_indexing(member_table, ['Member_ID', 'Name', 'Email', 'Age'])
        
        if member_results:
            output_file = plot_results(member_results, 'campus_trade_indexing/memberExt_indexing.png')
            print(f"Results saved to: {output_file}")
    
    # Test indexing on product_listing table
    if 'product_listing' in db.tables:
        product_table = db.tables['product_listing']
        product_results = test_table_indexing(product_table, ['Product_ID', 'Seller_ID', 'Category_ID', 'Price'])
        
        if product_results:
            output_file = plot_results(product_results, 'campus_trade_indexing/product_listing_indexing.png')
            print(f"Results saved to: {output_file}")
    
    # Test indexing on category table
    if 'category' in db.tables:
        category_table = db.tables['category']
        category_results = test_table_indexing(category_table, ['Category_ID', 'Category_Name'])
        
        if category_results:
            output_file = plot_results(category_results, 'campus_trade_indexing/category_indexing.png')
            print(f"Results saved to: {output_file}")
    
    print("Indexing tests completed.")

if __name__ == '__main__':
    main()
