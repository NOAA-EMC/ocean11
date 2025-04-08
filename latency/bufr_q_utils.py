#!/usr/bin/env python3

import os
from datetime import datetime
from datetime import timedelta
import numpy as np
import sys
from dir_utils import dir_file_paths
# from latency_table import LatencyTable


# gdas_pyiodaconv = "/work/noaa/da/edwardg/03182025/global-workflow/sorc/gdas.cd/build/lib/python3.7"


# obsforge_pyiodaconv = '/work/noaa/da/edwardg/03182025/obsForge/build/lib/python3.7'
# sys.path.append(obsforge_pyiodaconv)

# gdas_pyiodaconv = "/u/edward.givelberg/ns/Mworkflow/global-workflow/sorc/gdas.cd/build/lib/python3.10"
# sys.path.append(gdas_pyiodaconv)
# from pyiodaconv import bufr


import bufr



def is_bufr_file(filepath):
    """Check if a file is a BUFR file by looking for 'BUFR' magic bytes."""
    try:
        with open(filepath, 'rb') as f:
            magic = f.read(4)
            return magic == b'BUFR'
    except Exception:
        return False


def select_bufr_files(filepaths):
    files = []
    for file in filepaths:
        if is_bufr_file(file):
            files.append(file)
    # print(f'selected {len(files)}')
    return files


def get_bufr_dates(file_path, yaml_path):
    container = bufr.Parser(file_path, yaml_path).parse()
    dateTime = container.get("variables/dateTime")

    print(f'dateTime = {dateTime}')

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


def get_bufr_ob_time(filepath):
    print("get_bufr_ob_time")
    min_ob_time, max_ob_time = get_bufr_dates(filepath)
    return min_ob_time


def extract_bufr_instrument(filename):
    # Split the filename by '.'
    parts = filename.split('.')
    # Return the third element (index 2) which is the instrument
    return parts[2]


if __name__ == '__main__':

    # data_dir = '/work/noaa/da/marineda/gfs-marine/data/obs/gfs.20230425'
    filepath = '/work/noaa/da/marineda/gfs-marine/data/obs/gfs.20230425/00/atmos/gfs.t00z.bathy.tm00.bufr_d'
    yamlpath = '/work/noaa/da/edwardg/ocean11/latency/read_bufr_date.yaml'
    get_bufr_dates(filepath, yamlpath)


'''
if __name__ == '__main__':
    # Check command-line argument
    if len(sys.argv) != 2:
        print("Usage: python bufr_latency.py <directory>")
        sys.exit(1)

    bufr_dir = sys.argv[1]

    # latency_table = compute_bufr_latency_table(bufr_dir, get_min_max_obs_time)
    # print_bufr_latency_table(latency_table)

    latency_table = LatencyTable()


    try:
        file_paths = dir_file_paths(bufr_dir)
        # print(f'{len(file_paths)} files')
        latency_table.compute(file_paths, get_bufr_ob_time)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

    print(f"Latency Table for {bufr_dir}:")
    # print_latency_table(latency_table)
    latency_table.print()
    print("-----------------------------------")
    # latency_stats(latency_table)
    # print("-----------------------------------")
'''
