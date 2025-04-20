"""
Benchmarking utilities for B+ Tree and BruteForceDB.
"""

import time
import random
import os
from .bplus_tree import BPlusTree
from .brute_force_db import BruteForceDB

# Try to import optional dependencies
try:
    import matplotlib.pyplot as plt
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

class Benchmarker:
    """Benchmarker for B+ Tree and BruteForceDB."""

    def __init__(self, output_directory="benchmarks"):
        """
        Initialize a benchmarker.

        Args:
            output_directory (str): The directory to save benchmark results to
        """
        self.output_directory = output_directory

        # Create the output directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)

    def generate_random_data(self, size, key_range=None):
        """
        Generate random data for benchmarking.

        Args:
            size (int): The number of key-value pairs to generate
            key_range (tuple): The range of keys to generate (min, max)

        Returns:
            list: A list of (key, value) pairs
        """
        if key_range is None:
            key_range = (0, size * 10)

        # Generate random keys
        keys = random.sample(range(key_range[0], key_range[1]), size)

        # Generate random values
        values = [f"value_{i}" for i in range(size)]

        return list(zip(keys, values))

    def benchmark_insert(self, data_sizes, num_runs=3):
        """
        Benchmark insert operations.

        Args:
            data_sizes (list): The sizes of data to benchmark
            num_runs (int): The number of runs for each data size

        Returns:
            dict: The benchmark results
        """
        results = {
            'bplus_tree': {
                'time': [],
                'memory': []
            },
            'brute_force': {
                'time': [],
                'memory': []
            }
        }

        for size in data_sizes:
            bplus_times = []
            bplus_memory = []
            brute_times = []
            brute_memory = []

            for _ in range(num_runs):
                # Generate random data
                data = self.generate_random_data(size)

                # Benchmark B+ Tree
                tree = BPlusTree()
                start_time = time.time()
                start_memory = self._get_memory_usage()

                for key, value in data:
                    tree.insert(key, value)

                end_time = time.time()
                end_memory = self._get_memory_usage()

                bplus_times.append(end_time - start_time)
                bplus_memory.append(end_memory - start_memory)

                # Benchmark BruteForceDB
                db = BruteForceDB()
                start_time = time.time()
                start_memory = self._get_memory_usage()

                for key, value in data:
                    db.insert(key, value)

                end_time = time.time()
                end_memory = self._get_memory_usage()

                brute_times.append(end_time - start_time)
                brute_memory.append(end_memory - start_memory)

            # Calculate average time and memory usage
            results['bplus_tree']['time'].append(sum(bplus_times) / num_runs)
            results['bplus_tree']['memory'].append(sum(bplus_memory) / num_runs)
            results['brute_force']['time'].append(sum(brute_times) / num_runs)
            results['brute_force']['memory'].append(sum(brute_memory) / num_runs)

        # Plot the results
        self._plot_results(data_sizes, results, 'insert')

        return results

    def benchmark_search(self, data_sizes, num_runs=3, num_searches=100):
        """
        Benchmark search operations.

        Args:
            data_sizes (list): The sizes of data to benchmark
            num_runs (int): The number of runs for each data size
            num_searches (int): The number of searches to perform

        Returns:
            dict: The benchmark results
        """
        results = {
            'bplus_tree': {
                'time': [],
                'memory': []
            },
            'brute_force': {
                'time': [],
                'memory': []
            }
        }

        for size in data_sizes:
            bplus_times = []
            bplus_memory = []
            brute_times = []
            brute_memory = []

            for _ in range(num_runs):
                # Generate random data
                data = self.generate_random_data(size)

                # Insert data into B+ Tree and BruteForceDB
                tree = BPlusTree()
                db = BruteForceDB()

                for key, value in data:
                    tree.insert(key, value)
                    db.insert(key, value)

                # Generate random keys for searching
                search_keys = random.sample([key for key, _ in data], min(num_searches, len(data)))

                # Benchmark B+ Tree
                start_time = time.time()
                start_memory = self._get_memory_usage()

                for key in search_keys:
                    tree.search(key)

                end_time = time.time()
                end_memory = self._get_memory_usage()

                bplus_times.append(end_time - start_time)
                bplus_memory.append(end_memory - start_memory)

                # Benchmark BruteForceDB
                start_time = time.time()
                start_memory = self._get_memory_usage()

                for key in search_keys:
                    db.search(key)

                end_time = time.time()
                end_memory = self._get_memory_usage()

                brute_times.append(end_time - start_time)
                brute_memory.append(end_memory - start_memory)

            # Calculate average time and memory usage
            results['bplus_tree']['time'].append(sum(bplus_times) / num_runs)
            results['bplus_tree']['memory'].append(sum(bplus_memory) / num_runs)
            results['brute_force']['time'].append(sum(brute_times) / num_runs)
            results['brute_force']['memory'].append(sum(brute_memory) / num_runs)

        # Plot the results
        self._plot_results(data_sizes, results, 'search')

        return results

    def benchmark_range_search(self, data_sizes, num_runs=3, num_searches=100, range_size=0.1):
        """
        Benchmark range search operations.

        Args:
            data_sizes (list): The sizes of data to benchmark
            num_runs (int): The number of runs for each data size
            num_searches (int): The number of searches to perform
            range_size (float): The size of the range as a fraction of the data size

        Returns:
            dict: The benchmark results
        """
        results = {
            'bplus_tree': {
                'time': [],
                'memory': []
            },
            'brute_force': {
                'time': [],
                'memory': []
            }
        }

        for size in data_sizes:
            bplus_times = []
            bplus_memory = []
            brute_times = []
            brute_memory = []

            for _ in range(num_runs):
                # Generate random data
                data = self.generate_random_data(size)

                # Insert data into B+ Tree and BruteForceDB
                tree = BPlusTree()
                db = BruteForceDB()

                for key, value in data:
                    tree.insert(key, value)
                    db.insert(key, value)

                # Generate random ranges for searching
                keys = sorted([key for key, _ in data])
                ranges = []

                for _ in range(min(num_searches, len(data))):
                    start_idx = random.randint(0, len(keys) - 2)
                    end_idx = min(start_idx + int(len(keys) * range_size), len(keys) - 1)
                    ranges.append((keys[start_idx], keys[end_idx]))

                # Benchmark B+ Tree
                start_time = time.time()
                start_memory = self._get_memory_usage()

                for start_key, end_key in ranges:
                    tree.range_search(start_key, end_key)

                end_time = time.time()
                end_memory = self._get_memory_usage()

                bplus_times.append(end_time - start_time)
                bplus_memory.append(end_memory - start_memory)

                # Benchmark BruteForceDB
                start_time = time.time()
                start_memory = self._get_memory_usage()

                for start_key, end_key in ranges:
                    db.range_search(start_key, end_key)

                end_time = time.time()
                end_memory = self._get_memory_usage()

                brute_times.append(end_time - start_time)
                brute_memory.append(end_memory - start_memory)

            # Calculate average time and memory usage
            results['bplus_tree']['time'].append(sum(bplus_times) / num_runs)
            results['bplus_tree']['memory'].append(sum(bplus_memory) / num_runs)
            results['brute_force']['time'].append(sum(brute_times) / num_runs)
            results['brute_force']['memory'].append(sum(brute_memory) / num_runs)

        # Plot the results
        self._plot_results(data_sizes, results, 'range_search')

        return results

    def benchmark_delete(self, data_sizes, num_runs=3, delete_fraction=0.5):
        """
        Benchmark delete operations.

        Args:
            data_sizes (list): The sizes of data to benchmark
            num_runs (int): The number of runs for each data size
            delete_fraction (float): The fraction of data to delete

        Returns:
            dict: The benchmark results
        """
        results = {
            'bplus_tree': {
                'time': [],
                'memory': []
            },
            'brute_force': {
                'time': [],
                'memory': []
            }
        }

        for size in data_sizes:
            bplus_times = []
            bplus_memory = []
            brute_times = []
            brute_memory = []

            for _ in range(num_runs):
                # Generate random data
                data = self.generate_random_data(size)

                # Insert data into B+ Tree and BruteForceDB
                tree = BPlusTree()
                db = BruteForceDB()

                for key, value in data:
                    tree.insert(key, value)
                    db.insert(key, value)

                # Generate random keys for deletion
                delete_keys = random.sample([key for key, _ in data], int(len(data) * delete_fraction))

                # Benchmark B+ Tree
                start_time = time.time()
                start_memory = self._get_memory_usage()

                for key in delete_keys:
                    tree.delete(key)

                end_time = time.time()
                end_memory = self._get_memory_usage()

                bplus_times.append(end_time - start_time)
                bplus_memory.append(end_memory - start_memory)

                # Benchmark BruteForceDB
                start_time = time.time()
                start_memory = self._get_memory_usage()

                for key in delete_keys:
                    db.delete(key)

                end_time = time.time()
                end_memory = self._get_memory_usage()

                brute_times.append(end_time - start_time)
                brute_memory.append(end_memory - start_memory)

            # Calculate average time and memory usage
            results['bplus_tree']['time'].append(sum(bplus_times) / num_runs)
            results['bplus_tree']['memory'].append(sum(bplus_memory) / num_runs)
            results['brute_force']['time'].append(sum(brute_times) / num_runs)
            results['brute_force']['memory'].append(sum(brute_memory) / num_runs)

        # Plot the results
        self._plot_results(data_sizes, results, 'delete')

        return results

    def _get_memory_usage(self):
        """
        Get the current memory usage.

        Returns:
            float: The current memory usage in MB, or 0 if psutil is not available
        """
        if not PSUTIL_AVAILABLE:
            return 0

        process = psutil.Process(os.getpid())
        return process.memory_info().rss / (1024 * 1024)  # Convert to MB

    def _plot_results(self, data_sizes, results, operation):
        """
        Plot benchmark results.

        Args:
            data_sizes (list): The sizes of data
            results (dict): The benchmark results
            operation (str): The operation being benchmarked
        """
        if not MATPLOTLIB_AVAILABLE:
            print(f"Matplotlib is not available. Plotting for {operation} skipped.")
            return

        # Create a figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Plot time results
        ax1.plot(data_sizes, results['bplus_tree']['time'], 'o-', label='B+ Tree')
        ax1.plot(data_sizes, results['brute_force']['time'], 's-', label='Brute Force')
        ax1.set_xlabel('Data Size')
        ax1.set_ylabel('Time (seconds)')
        ax1.set_title(f'{operation.capitalize()} Time')
        ax1.legend()
        ax1.grid(True)

        # Plot memory results
        ax2.plot(data_sizes, results['bplus_tree']['memory'], 'o-', label='B+ Tree')
        ax2.plot(data_sizes, results['brute_force']['memory'], 's-', label='Brute Force')
        ax2.set_xlabel('Data Size')
        ax2.set_ylabel('Memory (MB)')
        ax2.set_title(f'{operation.capitalize()} Memory Usage')
        ax2.legend()
        ax2.grid(True)

        # Adjust layout and save the figure
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_directory, f'{operation}_benchmark.png'))
        plt.close()
