"""
Script to run custom benchmarks comparing B+ Tree and BruteForceDB.
"""

import time
import random
import os
import matplotlib.pyplot as plt
from db_engine import BPlusTree, BruteForceDB

def benchmark_insert(data_sizes, num_runs=3):
    """Benchmark insert operations."""
    results = {
        'bplus_tree': {
            'time': []
        },
        'brute_force': {
            'time': []
        }
    }
    
    for size in data_sizes:
        bplus_times = []
        brute_times = []
        
        for _ in range(num_runs):
            # Generate random data
            keys = random.sample(range(size * 10), size)
            values = [f"value_{i}" for i in range(size)]
            data = list(zip(keys, values))
            
            # Benchmark B+ Tree
            tree = BPlusTree()
            start_time = time.time()
            
            for key, value in data:
                tree.insert(key, value)
            
            end_time = time.time()
            bplus_times.append(end_time - start_time)
            
            # Benchmark BruteForceDB
            db = BruteForceDB()
            start_time = time.time()
            
            for key, value in data:
                db.insert(key, value)
            
            end_time = time.time()
            brute_times.append(end_time - start_time)
        
        # Calculate average time
        results['bplus_tree']['time'].append(sum(bplus_times) / num_runs)
        results['brute_force']['time'].append(sum(brute_times) / num_runs)
    
    return results

def benchmark_search(data_sizes, num_runs=3, num_searches=100):
    """Benchmark search operations."""
    results = {
        'bplus_tree': {
            'time': []
        },
        'brute_force': {
            'time': []
        }
    }
    
    for size in data_sizes:
        bplus_times = []
        brute_times = []
        
        for _ in range(num_runs):
            # Generate random data
            keys = random.sample(range(size * 10), size)
            values = [f"value_{i}" for i in range(size)]
            data = list(zip(keys, values))
            
            # Insert data into B+ Tree and BruteForceDB
            tree = BPlusTree()
            db = BruteForceDB()
            
            for key, value in data:
                tree.insert(key, value)
                db.insert(key, value)
            
            # Generate random keys for searching
            search_keys = random.sample(keys, min(num_searches, len(keys)))
            
            # Benchmark B+ Tree
            start_time = time.time()
            
            for key in search_keys:
                tree.search(key)
            
            end_time = time.time()
            bplus_times.append(end_time - start_time)
            
            # Benchmark BruteForceDB
            start_time = time.time()
            
            for key in search_keys:
                db.search(key)
            
            end_time = time.time()
            brute_times.append(end_time - start_time)
        
        # Calculate average time
        results['bplus_tree']['time'].append(sum(bplus_times) / num_runs)
        results['brute_force']['time'].append(sum(brute_times) / num_runs)
    
    return results

def benchmark_range_search(data_sizes, num_runs=3, num_searches=50, range_size=0.1):
    """Benchmark range search operations."""
    results = {
        'bplus_tree': {
            'time': []
        },
        'brute_force': {
            'time': []
        }
    }
    
    for size in data_sizes:
        bplus_times = []
        brute_times = []
        
        for _ in range(num_runs):
            # Generate random data
            keys = random.sample(range(size * 10), size)
            values = [f"value_{i}" for i in range(size)]
            data = list(zip(keys, values))
            
            # Insert data into B+ Tree and BruteForceDB
            tree = BPlusTree()
            db = BruteForceDB()
            
            for key, value in data:
                tree.insert(key, value)
                db.insert(key, value)
            
            # Generate random ranges for searching
            sorted_keys = sorted(keys)
            ranges = []
            
            for _ in range(min(num_searches, len(keys))):
                start_idx = random.randint(0, len(sorted_keys) - 2)
                end_idx = min(start_idx + int(len(sorted_keys) * range_size), len(sorted_keys) - 1)
                ranges.append((sorted_keys[start_idx], sorted_keys[end_idx]))
            
            # Benchmark B+ Tree
            start_time = time.time()
            
            for start_key, end_key in ranges:
                tree.range_search(start_key, end_key)
            
            end_time = time.time()
            bplus_times.append(end_time - start_time)
            
            # Benchmark BruteForceDB
            start_time = time.time()
            
            for start_key, end_key in ranges:
                db.range_search(start_key, end_key)
            
            end_time = time.time()
            brute_times.append(end_time - start_time)
        
        # Calculate average time
        results['bplus_tree']['time'].append(sum(bplus_times) / num_runs)
        results['brute_force']['time'].append(sum(brute_times) / num_runs)
    
    return results

def plot_results(data_sizes, results, operation, output_dir="custom_benchmarks"):
    """Plot benchmark results."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create a figure
    plt.figure(figsize=(10, 6))
    
    # Plot time results
    plt.plot(data_sizes, results['bplus_tree']['time'], 'o-', label='B+ Tree')
    plt.plot(data_sizes, results['brute_force']['time'], 's-', label='Brute Force')
    plt.xlabel('Data Size')
    plt.ylabel('Time (seconds)')
    plt.title(f'{operation.capitalize()} Time')
    plt.legend()
    plt.grid(True)
    
    # Save the figure
    plt.savefig(os.path.join(output_dir, f'{operation}_benchmark.png'))
    plt.close()
    
    return os.path.join(output_dir, f'{operation}_benchmark.png')

def main():
    """Run custom benchmarks."""
    # Create output directory
    output_dir = "custom_benchmarks"
    os.makedirs(output_dir, exist_ok=True)
    
    # Define data sizes
    data_sizes = [100, 500, 1000, 5000, 10000]
    
    print("Running insert benchmarks...")
    insert_results = benchmark_insert(data_sizes)
    insert_path = plot_results(data_sizes, insert_results, 'insert', output_dir)
    print(f"Insert benchmark results saved to: {insert_path}")
    
    print("Running search benchmarks...")
    search_results = benchmark_search(data_sizes)
    search_path = plot_results(data_sizes, search_results, 'search', output_dir)
    print(f"Search benchmark results saved to: {search_path}")
    
    print("Running range search benchmarks...")
    range_search_results = benchmark_range_search(data_sizes)
    range_search_path = plot_results(data_sizes, range_search_results, 'range_search', output_dir)
    print(f"Range search benchmark results saved to: {range_search_path}")
    
    print("\nAll custom benchmarks completed!")
    print(f"You can find the benchmark results in the '{output_dir}' directory.")

if __name__ == '__main__':
    main()
