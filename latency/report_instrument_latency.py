#!/usr/bin/env python3

import os
import sys
# import re
import argparse
# import glob
from fnmatch import filter

from dir_utils import dir_file_paths
from date_utils import get_first_time_from_filename
from latency_table import LatencyTable


# Mindo's data on hercules:
# data_dir = '/work/noaa/da/marineda/gfs-marine/data/obs/gfs.20230425'
# wcoss:
# not data_root = '/lfs/h1/ops/prod/com/obsproc/v1.2'



data_dir="lfs/h1/ops/prod/dcom/20250328/sst"
data_dir="lfs/h1/ops/prod/dcom/20250328/wgrdbul/adt"


def select_by_instrument(file_list, instrument_name):
    """
    Filters the files whose names contain the instrument_name (case-insensitive).
    """
    instrument_name_lower = instrument_name.lower()  # Convert to lower case for case-insensitive comparison
    return [file for file in file_list if instrument_name_lower in file.lower()]



def ParseArgs():
    parser = argparse.ArgumentParser(description="Generate full file paths from a directory and filenames.")

    # Required argument for directory
    parser.add_argument("directory", help="Directory path")

    parser.add_argument("-I", "--instrument", help="Filter filenames case-sensitively")
    parser.add_argument("-f", "--filter", help="Filter filenames case-sensitively")

    args = parser.parse_args()

    d = args.directory
    i = args.instrument
    f = args.filter

    return d, i, f


def filter_files(file_list):
    # Define the regular expression pattern
    pattern = r"^rads_adt_\w{2}_\w{7}\.nc$"
    
    # Use list comprehension to filter out files matching the pattern
    filtered_files = [file for file in file_list if not re.match(pattern, file)]
    
    return filtered_files


def main():

    # dir_name, instrument_name, filter_string = ParseArgs()

    data_root_dir = '/lfs/h1/ops/prod/dcom'
    #? date = '20250327'
    # date = '20250328'
    # date = '20250329'
    date = '20250330'

    # instrument_data = {
        # "adt":
        # "sst":
    # }
# instruments = [
    # {"name": "Instrument1", "directory": "/path/to/instrument1", "filter_string": "*.nc"},
    # {"name": "Instrument2", "directory": "/path/to/instrument2", "filter_string": "*.txt"},
    # {"name": "Instrument3", "directory": "/path/to/instrument3", "filter_string": "*.csv"},
# ]

    # filters = [
        # 'rads_adt_??_???????.nc',
        # '??????????????-????--L3?_GHRSST-*.nc',
        # 'AMSR2-SEAICE*.nc',
        # 'SM_OPER*.nc',
        # 'SMAP*.h5'
    # ]

    # instrument_subdir = 'wgrdbul/adt'
    # instrument_name = "adt"
    # # filter_string = "rads_adt"
    # filter_string = r"^rads_adt_\w{2}_\w{7}\.nc$"
    # filter_string = 'rads_adt_??_???????.nc'

    instrument_subdir = 'sst'
    instrument_name = "sst"
    # # filter_string = "L3"
    # # filter_string = r"^-....--L3?.*GHRSST-.*\.nc$"
    # # filter_string = '??????????????-????--L3?_GHRSST-*.nc'
    filter_string = '*L3*.nc'

    # instrument_subdir = 'seaice/pda'
    # instrument_name = "seaice"
    # # filter_string = "AMSR2"
    # # filter_string = r"^AMSR2-SEAICE.*\.nc$"
    # # filter_string = r"^AMSR2-SEAICE-[A-Za-z0-9_-]+_v\d+r\d+_GW\d+s\d{14}_e\d{14}_c\d{14}\.nc$"
    # filter_string = 'AMSR2-SEAICE*.nc'



    # instrument_subdir = 'wtxtbul/satSSS/SMOS'
    # # instrument_name = "smos"
    # instrument_name = "SM_OPER"
    # # filter_string = "SM_OPER"
    # # filter_string = r'^SM_OPER.*\.nc$'
    # filter_string = 'SM_OPER*.nc'

    # instrument_subdir = 'wtxtbul/satSSS/SMAP'
    # instrument_name = "smap"
    # # filter_string = "SMAP"
    # filter_string = 'SMAP*.h5'

    dir_name = data_root_dir + "/" + date + "/" + instrument_subdir

    # Check if the directory exists and is a valid directory or symlink
    if not os.path.exists(dir_name):
        print(f"Error: The path '{dir_name}' does not exist.")
        sys.exit(1)
    
    if not (os.path.isdir(dir_name) or os.path.islink(dir_name)):
        print(f"Error: '{dir_name}' is neither a directory nor a symbolic link.")
        sys.exit(1)
    
    # Generate the list of files in the directory
    files = [f for f in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, f))]

    print(f"Total {len(files)} files in directory '{dir_name}'")
    # for file in files:
        # print(file)

    if instrument_name:
        files = select_by_instrument(files, instrument_name)
        print(f"\nSelected {len(files)} files for '{instrument_name}'")

    if filter_string:
        # files = [filename for filename in files if filter_string in filename]
        # files = [file for file in files if not re.match(filter_string, file)]
        files = filter(files, filter_string)

    # for file in files:
        # print(file)

    filepaths = [os.path.join(dir_name, filename) for filename in files]

    latency_table = LatencyTable()
    latency_table.compute(filepaths, get_first_time_from_filename)
    # latency_table.print()
    # sys.exit(1)

    # print(f'instrument\t#files\tmin\tmax\tavg\tmedian')
    # n = latency_table.number_of_items()
    # min = latency_table.min_latency()
    # max = latency_table.max_latency()
    # avg = latency_table.avg_latency()
    # median = latency_table.median_latency()
    # print(f'{instrument_name}\t\t{n}\t{min}\t{max}\t{avg}\t{median}')
# # latency_table.print()

    print(f'Latency stats for {instrument_name}')
    print(f'directory: {dir_name}')
    latency_table.stats()


if __name__ == "__main__":
    main()

'''
Hi Ed,

I forgot to mention that not all files in these directories should be used for the latency evaluation: 
/lfs/h1/ops/prod/dcom/YYYYMMDD/wgrdbul/adt 
/lfs/h1/ops/prod/dcom/YYYYMMDD/sst                   
/lfs/h1/ops/prod/dcom/YYYYMMDD/seaice/pda     *AMSR2* 
/lfs/h1/ops/prod/dcom/YYYYMMDD/wtxtbul/satSSS/SMOS   SM_OPER*
/lfs/h1/ops/prod/dcom/YYYYMMDD/wtxtbul/satSSS/SMAP     SMAP*

Use only:
/lfs/h1/ops/prod/dcom/YYYYMMDD/wgrdbul/adt/rads_adt_??_???????.nc
/lfs/h1/ops/prod/dcom/YYYYMMDD/sst/YYYYMMDDHHMMSS-????--L3?_GHRSST-*.nc     

The rest of the directories you can use in full:
/lfs/h1/ops/prod/dcom/YYYYMMDD/seaice/pda/AMSR2-SEAICE*.nc 
/lfs/h1/ops/prod/dcom/YYYYMMDD/wtxtbul/satSSS/SMOS/SM_OPER*.nc
/lfs/h1/ops/prod/dcom/YYYYMMDD/wtxtbul/satSSS/SMAP/SMAP*.h5

thanks, iliana
'''
