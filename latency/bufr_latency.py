#!/usr/bin/env python3

import os
from datetime import datetime
from datetime import timedelta
import numpy as np
import sys


gdas_pyiodaconv = "/work/noaa/da/edwardg/03182025/global-workflow/sorc/gdas.cd/build/lib/python3.7"
obsforge_pyiodaconv = '/work/noaa/da/edwardg/03182025/obsForge/build/lib/python3.7'
sys.path.append(obsforge_pyiodaconv)
sys.path.append(gdas_pyiodaconv)
from pyiodaconv import bufr


# orion
bufr_dir = "/work/noaa/da/marineda/gfs-marine/data/obs/ci/bufr/"
# bufrfile_path = "/work/noaa/da/marineda/gfs-marine/data/obs/ci/bufr/2019010700-gdas.t00z.cstgd.tm00.bufr_d"

# bufr_dir = '/home/Guillaume.Vernieres/scratch1/runs/realtimeobs/lfs/h1/ops/prod/dcom'
# ioda_dir = '/scratch1/NCEPDEV/stmp2/Guillaume.Vernieres/runs/realtimeobs/lfs/h1/ops/prod/dcom'
# ioda_dir = '/scratch1/NCEPDEV/stmp2/Guillaume.Vernieres/runs/realtimeobs/lfs/h1/ops/prod/dcom/20250316/seaice/pda'

# hera
bufr_dir = '/scratch1/NCEPDEV/da/common/ci/bufr'




def get_bufr_dates(file_path):
    q = bufr.QuerySet()
    q.add('year', '*/YEAR')
    q.add('month', '*/MNTH')
    q.add('day', '*/DAYS')
    q.add('hour', '*/HOUR')
    q.add('minute', '*/MINU')

    with bufr.File(file_path) as f:
        r = f.execute(q)

    dateTime = r.get_datetime('year', 'month', 'day', 'hour', 'minute')

    # print(f'dateTime = {dateTime}')


    # Convert numpy.datetime64 to datetime objects
    dateTime = [dt.astype('datetime64[ms]').astype(datetime) for dt in dateTime]


    # 1. Compute average datetime
    timestamps = [dt.timestamp() for dt in dateTime]  # Convert to timestamps
    avg_timestamp = np.mean(timestamps)  # Average timestamp
    avg_datetime = datetime.fromtimestamp(avg_timestamp)  # Back to datetime

    # 2. Compute half length of the date interval
    min_datetime = min(dateTime)
    max_datetime = max(dateTime)
    total_interval = max_datetime - min_datetime  # Timedelta object
    half_interval = total_interval / 2

    # Output results
    # print(f"Average Datetime: {avg_datetime}")
    # print(f"Min Datetime: {min_datetime}")
    # print(f"Max Datetime: {max_datetime}")
    # print(f"Total Interval: {total_interval}")
    # print(f"Half Length of Interval: {half_interval}")

    return min_datetime, max_datetime


def get_min_max_obs_time(file_path):
    return get_bufr_dates(file_path)



def compute_bufr_latency_table(directory, get_min_max_obs_time):
    """
    Calculate latency data for files in a directory, skipping empty files.
    
    Parameters:
    - directory (str): Path to the directory containing files.
    - get_min_max_obs_time (callable): Function that takes a file path and returns (min_obs_time, max_obs_time).
    
    
    Returns:
    - dict: Dictionary with file names as keys and (min_latency, max_latency) in hours as values.
    """
    latency_table = {}
    
    # Process each file in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):  # Ensure it's a file, not a directory
            # Check if the file is empty
            if os.path.getsize(file_path) == 0:
                # print(f"Skipping empty file: {filename}")
                continue  # Skip to the next file
            
            # Get file creation time
            creation_time_ts = os.path.getctime(file_path)
            creation_time = datetime.fromtimestamp(creation_time_ts)
            
            
            # Get min and max observation times
            min_obs_time, max_obs_time = get_min_max_obs_time(file_path)
            
            # Compute latencies (in hours)
            min_latency = (creation_time - min_obs_time).total_seconds() / 3600
            max_latency = (creation_time - max_obs_time).total_seconds() / 3600
            
            # Store in table
            latency_table[filename] = (min_latency, max_latency)
    
    return latency_table


def print_bufr_latency_table0(latency_table):
    """
    Print the latency table with file names and overall average latency window.
    
    Parameters:
    - latency_table (dict): Dictionary with file names and (min_latency, max_latency) pairs.
    """
    print("Latency Table:")
    print(f"{'File Name':<30} {'Min Latency (hours)':<20} {'Max Latency (hours)':<20}")
    print("-" * 70)
    
    # Extract latencies for averaging
    min_latencies = [lat[0] for lat in latency_table.values()]
    max_latencies = [lat[1] for lat in latency_table.values()]
    
    for filename, (min_lat, max_lat) in latency_table.items():
        print(f"{filename:<30} {min_lat:<20.2f} {max_lat:<20.2f}")
    
    # Calculate and print overall average latency window
    avg_min_latency = np.mean(min_latencies)
    avg_max_latency = np.mean(max_latencies)
    avg_latency_window = avg_max_latency - avg_min_latency

    print("\nSummary:")
    print(f"Overall Average Latency Window: {avg_latency_window:.2f} hours")
    print(f"  - Average Min Latency: {avg_min_latency:.2f} hours")
    print(f"  - Average Max Latency: {avg_max_latency:.2f} hours")


def print_bufr_latency_table(latency_table):
    """
    Print the latency table with file names and latencies in days, hours, minutes, seconds.
    
    Parameters:
    - latency_table (dict): Dictionary with file names and (min_latency, max_latency) pairs in hours.
    """
    print("Latency Table:")
    print(f"{'File Name':<30} {'Min Latency':<30} {'Max Latency':<30}")
    print("-" * 90)
    
    
    # Extract latencies for averaging
    min_latencies = [lat[0] for lat in latency_table.values()]
    max_latencies = [lat[1] for lat in latency_table.values()]
    
    for filename, (min_lat, max_lat) in latency_table.items():
        # Convert hours back to seconds, then to timedelta
        min_lat_seconds = min_lat * 3600
        max_lat_seconds = max_lat * 3600
        min_lat_td = timedelta(seconds=min_lat_seconds)
        max_lat_td = timedelta(seconds=max_lat_seconds)
        
        # Format timedelta into days, hours, minutes, seconds
        min_lat_str = str(min_lat_td)
        max_lat_str = str(max_lat_td)
        
        print(f"{filename:<30} {min_lat_str:<30} {max_lat_str:<30}")
    
    
    # Calculate and print overall average latency window
    avg_min_latency = np.mean(min_latencies)  # In hours
    avg_max_latency = np.mean(max_latencies)  # In hours
    avg_latency_window = avg_max_latency - avg_min_latency
    
    # Convert averages to timedelta for display
    avg_min_lat_td = timedelta(seconds=avg_min_latency * 3600)
    avg_max_lat_td = timedelta(seconds=avg_max_latency * 3600)
    avg_window_td = timedelta(seconds=avg_latency_window * 3600)
    
    print("\nSummary:")
    print(f"Overall Average Latency Window: {avg_window_td}")
    print(f"  - Average Min Latency: {avg_min_lat_td}")
    print(f"  - Average Max Latency: {avg_max_lat_td}")



if __name__ == '__main__':
    # Check command-line argument
    if len(sys.argv) != 2:
        print("Usage: python bufr_latency.py <directory>")
        sys.exit(1)

    bufr_dir = sys.argv[1]

    latency_table = compute_bufr_latency_table(bufr_dir, get_min_max_obs_time)
    print_bufr_latency_table(latency_table)
