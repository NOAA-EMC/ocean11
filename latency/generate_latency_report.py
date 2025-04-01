import os
from dir_utils import dir_file_paths
from date_utils import get_first_time_from_filename
from latency_table import LatencyTable
from bufr_latency import *


# sort a latency table according to instrument
def list_of_bufr_latency_tables(latency_table):
    instrument_latency_tables = {}
    for filepath, latency in latency_table.latency_table.items():
        filename = os.path.basename(filepath)
        instrument = extract_bufr_instrument(filename)
        if instrument not in instrument_latency_tables:
            instrument_latency_tables[instrument] = LatencyTable()
        instrument_latency_tables[instrument].latency_table[filepath] = latency
    return instrument_latency_tables



def combined_bufr_latency_table(data_dir):
    combined_latency = LatencyTable()

    for cycle in ['00', '06', '12', '18']:
        cycle_dir = os.path.join(data_dir, cycle, 'atmos')
        # print(f'cycle_dir = {cycle_dir}')
        
        if os.path.isdir(cycle_dir):
            # Call the function to get the latency table for 'atmos' for this cycle
            file_paths = dir_file_paths(cycle_dir)
            # print(f'file_paths = {file_paths}')
            latency_table = LatencyTable()
            latency_table.compute(file_paths, get_bufr_ob_time)
            # print(f'latency_table = {latency_table}')
            
            combined_latency.add(latency_table)
    
    return combined_latency


# list of latency tables, one for each instrument
def list_of_instrument_latency_tables(data_dir):
    # Initialize a list to store latency tables for each instrument
    instrument_latency_tables = {}

    # Loop over the cycles 00, 06, 12, 18
    for cycle in ['00', '06', '12', '18']:
        cycle_dir = os.path.join(data_dir, cycle, 'ocean')
        # print(f'cycle_dir = {cycle_dir}')
        
        if os.path.isdir(cycle_dir):
            # Loop through the subdirectories of 'ocean' which represent instruments
            for instrument_dir in os.listdir(cycle_dir):
                instrument_path = os.path.join(cycle_dir, instrument_dir)
                # print(f'instrument_dir = {instrument_dir}')
                
                # Check if it's a valid directory (or symlink)
                if os.path.isdir(instrument_path) or os.path.islink(instrument_path):
                    # Call the function to get the latency table for this instrument
                    # print(f'instrument_path = {instrument_path}')
                    file_paths = dir_file_paths(instrument_path)
                    latency_table = LatencyTable()
                    latency_table.compute(file_paths, get_first_time_from_filename)
                    
                    # Store or combine latency table (assuming merging by instrument name)
                    if instrument_dir not in instrument_latency_tables:
                        instrument_latency_tables[instrument_dir] = latency_table
                    else:
                        instrument_latency_tables[instrument_dir].add(latency_table)

    # Return a list of latency tables for each instrument across all cycles
    return instrument_latency_tables



def print_latency_report(latency_table_list):
    print(f'instrument\t#files\tmin\tmax\tavg\tmean')
    for instrument, latency_table in latency_table_list.items():
        n = latency_table.number_of_items()
        min = latency_table.min_latency()
        max = latency_table.max_latency()
        avg = latency_table.max_latency()
        median = latency_table.median_latency()
        print(f'{instrument}\t{n}\t{min}\t{max}\t{avg}\t{median}')
        # latency_table.print()
        # latency_table.stats()




# Mindo's data on hercules:
# data_dir = '/work/noaa/da/marineda/gfs-marine/data/obs/gfs.20230425'

if __name__ == '__main__':
    # Check command-line argument
    if len(sys.argv) != 2:
        print("Usage: python report_latency.py <directory>")
        sys.exit(1)

    data_dir = sys.argv[1]

    ocean_dir_latency_table_list = list_of_instrument_latency_tables(data_dir)
    print_latency_report(ocean_dir_latency_table_list)


    bufr_latency_table = combined_bufr_latency_table(data_dir)
    # bufr_latency_table.print()
    instrument_table_list = list_of_bufr_latency_tables(bufr_latency_table)
    print_latency_report(instrument_table_list)
