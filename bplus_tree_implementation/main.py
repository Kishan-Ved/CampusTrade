"""
Main script to run the B+ Tree database application.
"""

import os
import sys
import argparse

def main():
    """Main function to run the application."""
    parser = argparse.ArgumentParser(description='B+ Tree Database Application')
    parser.add_argument('--init', action='store_true', help='Initialize the database')
    parser.add_argument('--run', action='store_true', help='Run the web application')
    parser.add_argument('--benchmark', action='store_true', help='Run benchmarks')
    args = parser.parse_args()

    if args.init:
        print("Initializing the database...")
        from init_database import init_database
        init_database()

    if args.benchmark:
        print("Running benchmarks...")
        from db_engine import Benchmarker
        benchmarker = Benchmarker()
        data_sizes = [100, 1000, 10000]
        benchmarker.benchmark_insert(data_sizes)
        benchmarker.benchmark_search(data_sizes)
        benchmarker.benchmark_range_search(data_sizes)
        benchmarker.benchmark_delete(data_sizes)
        print("Benchmarks completed. Results saved to the 'benchmarks' directory.")

    if args.run:
        print("Running the web application...")
        sys.path.append(os.path.join(os.path.dirname(__file__), 'frontend'))
        try:
            from frontend.app import run_app
            success = run_app()
            if not success:
                print("Failed to run the web application. Make sure Flask is installed.")
                print("You can install it with: pip install flask")
        except ImportError as e:
            print(f"Error importing frontend app: {e}")
            print("Make sure Flask is installed. You can install it with: pip install flask")

    if not (args.init or args.run or args.benchmark):
        parser.print_help()

if __name__ == '__main__':
    main()
