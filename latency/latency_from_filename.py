#!/usr/bin/env python3

import os
import sys
from datetime import datetime, timedelta
from date_utils import extract_first_date, format_timedelta
from dir_utils import dir_file_paths, list_files_recursive_relative_path


def compute_latency_table(path_list, logger=None):
    """
    Returns a dictionary with filepaths as keys and latency (timedelta) as values.
    """

    if logger is None:
        import logging
        logger = logging.getLogger(__name__)

    latency_table = {}

    for filepath in path_list:
        if not os.path.isfile(filepath):
            continue

        # print(filepath)

        try:
            # Get observation time from the file
            filename = os.path.basename(filepath)
            ob_time = extract_first_date(filename)
            # print(f'ob_time = {ob_time}')
            if ob_time is None:
                continue  # Skip if no valid date extracted
                
            # Get file creation time
            creation_time = datetime.fromtimestamp(os.path.getctime(filepath))
            
            # Calculate latency (creation_time - ob_time)
            latency = creation_time - ob_time
            # print(f'latency = {latency}')
            latency_table[filepath] = latency
            
        except Exception as e:
            # Log the error but continue with other files
            print(f"Error processing {filename}: {str(e)}", file=sys.stderr)
            continue

    return latency_table


def print_latency_table(latency_table):
    if not latency_table:
        print("No latency data available")
        return
        
    print("Filename".ljust(40), "Latency")
    print("-" * 60)
    # latencies = []
    for filepath, latency in latency_table.items():
        filename = os.path.basename(filepath)  # Extract the filename from the path
        print(f"{filename.ljust(40)} {str(latency)}")
        # latencies.append(latency)


def latency_stats(latency_table):
    latencies = []
    for filepath, latency in latency_table.items():
        latencies.append(latency)

    if latencies:
        min_latency = min(latencies, key=lambda td: td.total_seconds())
        max_latency = max(latencies, key=lambda td: td.total_seconds())
        avg_latency = sum(latencies, timedelta()) / len(latencies)

        # print("\nLatency Statistics:")
        print(f'Number of files: {len(latencies)}')
        print(f"Minimum Latency: {format_timedelta(min_latency)}")
        print(f"Maximum Latency: {format_timedelta(max_latency)}")
        print(f"Average Latency: {format_timedelta(avg_latency)}")
    # else:
        # print("No latencies available to calculate statistics.")



if __name__ == '__main__':
    # Check command-line argument
    if len(sys.argv) != 2:
        print("Usage: python latency_from_filename.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]

    # files = list_files_recursive_relative_path(directory)
    # print(files)
    # sys.exit(1)
    
    try:
        file_paths = dir_file_paths(directory)
        # print(f'{len(file_paths)} files')
        latency_table = compute_latency_table(file_paths)
        # latency_table = compute_latency_table(directory)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

    print(f"Latency Table for {directory}:")
    print_latency_table(latency_table)
    print("-----------------------------------")
    latency_stats(latency_table)
    print("-----------------------------------")

