#!/usr/bin/env python3

import os
import sys
from datetime import datetime
# Assuming extract_first_date is in a file named date_utils.py
from date_utils import extract_first_date

def compute_latency_table(directory, logger=None):
    """
    Compute latency table for all files in the given directory.
    Returns a dictionary with filenames as keys and latency (timedelta) as values.
    """

    if logger is None:
        import logging
        logger = logging.getLogger(__name__)

    latency_table = {}
    
    # Check if directory exists
    if not os.path.isdir(directory):
        raise ValueError(f"{directory} is not a valid directory")
    
    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        
        # Skip if it's not a file
        if not os.path.isfile(filepath):
            continue
            
        try:
            # Get observation time from the file
            ob_time = extract_first_date(filepath)
            # print(f'ob_time = {ob_time}')
            if ob_time is None:
                continue  # Skip if no valid date extracted
                
            # Get file creation time
            creation_time = datetime.fromtimestamp(os.path.getctime(filepath))
            
            # Calculate latency (creation_time - ob_time)
            latency = creation_time - ob_time
            # print(f'latency = {latency}')
            latency_table[filename] = latency
            
        except Exception as e:
            # Log the error but continue with other files
            print(f"Error processing {filename}: {str(e)}", file=sys.stderr)
            continue
            
    return latency_table


def print_latency_table(latency_table):
    if not latency_table:
        print("No latency data available")
        return
        
    print("Latency Table:")
    print("Filename".ljust(40), "Latency")
    print("-" * 60)
    for filename, latency in latency_table.items():
        print(f"{filename.ljust(40)} {str(latency)}")


if __name__ == '__main__':
    # Check command-line argument
    if len(sys.argv) != 2:
        print("Usage: python latency_checker.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    try:
        latency_table = compute_latency_table(directory)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

    print_latency_table(latency_table)
