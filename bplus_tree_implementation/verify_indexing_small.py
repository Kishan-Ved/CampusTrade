"""
Script to verify that indexing operations are faster than normal search operations.
Uses smaller dataset sizes for quicker execution.
"""

import time
import random
import matplotlib.pyplot as plt
from db_engine import Database, Table

def create_test_table(size):
    """Create a test table with random data."""
    # Define schema
    schema = {
        'id': {'type': 'int', 'primary_key': True},
        'name': {'type': 'string', 'nullable': False},
        'age': {'type': 'int', 'nullable': False},
        'score': {'type': 'float', 'nullable': False}
    }
    
    # Create table
    table = Table('test_table', schema)
    
    # Generate random data
    for i in range(size):
        row = {
            'id': i,
            'name': f'Person_{i}',
            'age': random.randint(18, 80),
            'score': random.uniform(0, 100)
        }
        table.insert(row)
    
    return table

def measure_search_performance(table, column, num_searches=50):
    """Measure search performance with and without an index."""
    # Get random values to search for
    if column == 'id':
        search_values = random.sample(range(len(table.rows)), min(num_searches, len(table.rows)))
    elif column == 'age':
        search_values = [random.randint(18, 80) for _ in range(num_searches)]
    elif column == 'score':
        search_values = [random.uniform(0, 100) for _ in range(num_searches)]
    
    # Measure non-indexed search time
    start_time = time.time()
    
    for value in search_values:
        # Define a where function to match the column value
        def where_func(row):
            return row.get(column) == value
        
        # Perform a non-indexed search
        table.select(where=where_func)
    
    non_indexed_time = time.time() - start_time
    
    # Create an index on the column if it doesn't exist
    if column not in table.indices and column != 'id':  # id already has an index
        table.create_index(column)
    
    # Measure indexed search time
    start_time = time.time()
    
    for value in search_values:
        # Perform an indexed search
        table.select_by_index(column, value)
    
    indexed_time = time.time() - start_time
    
    return non_indexed_time, indexed_time

def run_performance_test(sizes):
    """Run performance tests for different table sizes."""
    results = {
        'sizes': sizes,
        'id': {'non_indexed': [], 'indexed': []},
        'age': {'non_indexed': [], 'indexed': []},
        'score': {'non_indexed': [], 'indexed': []}
    }
    
    for size in sizes:
        print(f"Testing with table size: {size}")
        table = create_test_table(size)
        
        # Test search by ID
        non_indexed_time, indexed_time = measure_search_performance(table, 'id')
        results['id']['non_indexed'].append(non_indexed_time)
        results['id']['indexed'].append(indexed_time)
        print(f"  ID search - Non-indexed: {non_indexed_time:.6f}s, Indexed: {indexed_time:.6f}s")
        
        # Test search by age
        non_indexed_time, indexed_time = measure_search_performance(table, 'age')
        results['age']['non_indexed'].append(non_indexed_time)
        results['age']['indexed'].append(indexed_time)
        print(f"  Age search - Non-indexed: {non_indexed_time:.6f}s, Indexed: {indexed_time:.6f}s")
        
        # Test search by score
        non_indexed_time, indexed_time = measure_search_performance(table, 'score')
        results['score']['non_indexed'].append(non_indexed_time)
        results['score']['indexed'].append(indexed_time)
        print(f"  Score search - Non-indexed: {non_indexed_time:.6f}s, Indexed: {indexed_time:.6f}s")
    
    return results

def plot_results(results):
    """Plot the performance results."""
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))
    
    # Plot ID search results
    axs[0].plot(results['sizes'], results['id']['non_indexed'], 'o-', label='Non-indexed')
    axs[0].plot(results['sizes'], results['id']['indexed'], 's-', label='Indexed')
    axs[0].set_xlabel('Table Size')
    axs[0].set_ylabel('Time (seconds)')
    axs[0].set_title('ID Search Performance')
    axs[0].legend()
    axs[0].grid(True)
    
    # Plot age search results
    axs[1].plot(results['sizes'], results['age']['non_indexed'], 'o-', label='Non-indexed')
    axs[1].plot(results['sizes'], results['age']['indexed'], 's-', label='Indexed')
    axs[1].set_xlabel('Table Size')
    axs[1].set_ylabel('Time (seconds)')
    axs[1].set_title('Age Search Performance')
    axs[1].legend()
    axs[1].grid(True)
    
    # Plot score search results
    axs[2].plot(results['sizes'], results['score']['non_indexed'], 'o-', label='Non-indexed')
    axs[2].plot(results['sizes'], results['score']['indexed'], 's-', label='Indexed')
    axs[2].set_xlabel('Table Size')
    axs[2].set_ylabel('Time (seconds)')
    axs[2].set_title('Score Search Performance')
    axs[2].legend()
    axs[2].grid(True)
    
    plt.tight_layout()
    plt.savefig('indexing_performance_small.png')
    plt.close()
    
    return 'indexing_performance_small.png'

def main():
    """Run the indexing performance verification."""
    print("Verifying indexing performance...")
    
    # Define table sizes to test (smaller sizes for quicker execution)
    sizes = [100, 200, 500, 1000]
    
    # Run performance tests
    results = run_performance_test(sizes)
    
    # Plot results
    output_path = plot_results(results)
    
    print(f"\nResults plotted to: {output_path}")
    print("\nConclusion:")
    
    # Calculate average speedup
    id_speedup = sum([n/i if i > 0 else 0 for n, i in zip(results['id']['non_indexed'], results['id']['indexed'])]) / len(sizes)
    age_speedup = sum([n/i if i > 0 else 0 for n, i in zip(results['age']['non_indexed'], results['age']['indexed'])]) / len(sizes)
    score_speedup = sum([n/i if i > 0 else 0 for n, i in zip(results['score']['non_indexed'], results['score']['indexed'])]) / len(sizes)
    
    print(f"  ID search: Indexed search is approximately {id_speedup:.2f}x faster than non-indexed search")
    print(f"  Age search: Indexed search is approximately {age_speedup:.2f}x faster than non-indexed search")
    print(f"  Score search: Indexed search is approximately {score_speedup:.2f}x faster than non-indexed search")

if __name__ == '__main__':
    main()
