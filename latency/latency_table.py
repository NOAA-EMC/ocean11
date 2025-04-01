#!/usr/bin/env python3

import os
import sys
import statistics
from datetime import datetime, timedelta
from date_utils import get_first_time_from_filename, format_timedelta
from dir_utils import dir_file_paths, list_files_recursive_relative_path


class LatencyTable:
    def __init__(self, logger=None):
        if logger is None:
            import logging
            logger = logging.getLogger(__name__)
        self.latency_table = {}


    def add(self, another_table):
        self.latency_table.update(another_table.latency_table)


# a dictionary with filepaths as keys and latency (timedelta) as values.
# get_ob_time is a method to get observation time from the file or filename
    def compute(self, path_list, get_ob_time):
        for filepath in path_list:
            if not os.path.isfile(filepath):
                continue
            if os.path.getsize(filepath) == 0:
                # print(f"Skipping empty file: {filename}")
                continue  # Skip to the next file

            # print(filepath)

            try:
                # Get observation time from the file
                ob_time = get_ob_time(filepath)
                # print(f'ob_time = {ob_time}')
                if ob_time is None:
                    continue  # Skip if no valid date extracted
                
                # Get file creation time
                creation_time = datetime.fromtimestamp(os.path.getctime(filepath))

                # Calculate latency (creation_time - ob_time)
                latency = creation_time - ob_time
                # print(f'latency = {latency}')
                self.latency_table[filepath] = latency
            
            except Exception as e:
                # Log the error but continue with other files
                print(f"Error processing {filename}: {str(e)}", file=sys.stderr)
                continue



    def print(self):
        if not self.latency_table:
            print("No latency data available")
            return
        
        print("Filename".ljust(40), "Latency")
        print("-" * 60)
        # latencies = []
        for filepath, latency in self.latency_table.items():
            filename = os.path.basename(filepath)  # Extract the filename from the path
            print(f"{filename.ljust(40)} {str(latency)}")
            # latencies.append(latency)


    def get_all_latencies(self):
        latencies = []
        for filepath, latency in self.latency_table.items():
            latencies.append(latency)
        return latencies

    def stats(self):
        latencies = get_all_latencies()
        if latencies:
            min_latency = min(latencies, key=lambda td: td.total_seconds())
            max_latency = max(latencies, key=lambda td: td.total_seconds())
            avg_latency = sum(latencies, timedelta()) / len(latencies)
            median_latency = statistics.median(latencies)

            # print("\nLatency Statistics:")
            print(f'Number of files: {len(latencies)}')
            print(f"Minimum Latency: {format_timedelta(min_latency)}")
            print(f"Maximum Latency: {format_timedelta(max_latency)}")
            print(f"Average Latency: {format_timedelta(avg_latency)}")
            print(f"Median Latency: {format_timedelta(median_latency)}")
        # else:
            # print("No latencies available to calculate statistics.")

    def min_latency(self):
        latencies = self.get_all_latencies()
        return min(latencies, key=lambda td: td.total_seconds())

    def max_latency(self):
        latencies = self.get_all_latencies()
        return max(latencies, key=lambda td: td.total_seconds())

    def median_latency(self):
        latencies = self.get_all_latencies()
        return statistics.median(latencies)

    def avg_latency(self):
        latencies = self.get_all_latencies()
        return sum(latencies, timedelta()) / len(latencies)

    def number_of_items(self):
        latencies = self.get_all_latencies()
        return len(latencies)


if __name__ == '__main__':
    # Check command-line argument
    if len(sys.argv) != 2:
        print("Usage: python latency_from_filename.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]

    # files = list_files_recursive_relative_path(directory)
    # print(files)
    # sys.exit(1)
    
    latency_table = LatencyTable()

    try:
        file_paths = dir_file_paths(directory)
        print(f'Calculating latency for {len(file_paths)} files')
        latency_table.compute(file_paths, get_first_time_from_filename)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

    print(f"Latency Table for {directory}:")
    print("-----------------------------------")
    latency_table.print()
    print("-----------------------------------")
    latency_table.stats()
    print("-----------------------------------")
