#!/usr/bin/env python3

import os
from datetime import datetime
from datetime import timedelta
import numpy as np
import sys
# from latency_from_filename import print_latency_table
from latency_table import LatencyTable
from dir_utils import dir_file_paths


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


def get_bufr_ob_time(filepath):
    min_ob_time, max_ob_time = get_bufr_dates(filepath)
    return min_ob_time


def extract_bufr_instrument(filename):
    # Split the filename by '.'
    parts = filename.split('.')
    # Return the third element (index 2) which is the instrument
    return parts[2]


# def get_bufr_instrument_latency_tables(latency_table):


def compute_bufr_latency_table(path_list, logger=None):

    if logger is None:
        import logging
        logger = logging.getLogger(__name__)

    latency_table = {}

    for filepath in path_list:
        if not os.path.isfile(filepath):
            continue

        try:
            if os.path.getsize(filepath) == 0:
                # print(f"Skipping empty file: {filename}")
                continue  # Skip to the next file

            # Get observation time from the file
            filename = os.path.basename(filepath)
            # print(f'filepath = {filepath}')
            min_ob_time, max_ob_time = get_bufr_dates(filepath)
            ob_time = min_ob_time
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

