import os
from dir_utils import dir_file_paths
from latency_from_filename import *
from bufr_latency import *
# from latency_from_filename import compute_latency_table, print_latency_table, latency_stats



def combine_bufr_latency_tables(data_dir):
    # Initialize a dictionary to store combined latency tables
    combined_latency = {}

    # cycle_latency_table = []

    # Loop over the cycles 00, 06, 12, 18
    for cycle in ['00', '06', '12', '18']:
        cycle_dir = os.path.join(data_dir, cycle, 'atmos')
        # print(f'cycle_dir = {cycle_dir}')
        
        if os.path.isdir(cycle_dir):
            # Call the function to get the latency table for 'atmos' for this cycle
            # cycle_latency = compute_bufr_latency_table('atmos')
            file_paths = dir_file_paths(cycle_dir)
            # print(f'file_paths = {file_paths}')
            latency_table = compute_bufr_latency_table(file_paths)
            # print(f'latency_table = {latency_table}')
            
            # Combine latency data (here we just update, adjust depending on your data structure)
            combined_latency.update(latency_table)
    
    return combined_latency



def combine_ocean_latency_tables(data_dir):
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
                    # latency_table = compute_latency1_table(instrument_dir)
                    # print(f'instrument_path = {instrument_path}')
                    file_paths = dir_file_paths(instrument_path)
                    latency_table = compute_latency_table(file_paths)
                    # print_latency_table(latency_table)
                    
                    # Store or combine latency table (assuming merging by instrument name)
                    if instrument_dir not in instrument_latency_tables:
                        # instrument_latency_tables[instrument_dir] = []
                        instrument_latency_tables[instrument_dir] = latency_table
                    else:
                        instrument_latency_tables[instrument_dir].update(latency_table)
                    
                    # Append the current cycle's latency table for this instrument
                    # instrument_latency_tables[instrument_dir].append(latency_table)
                    # instrument_latency_tables[instrument_dir].extend(latency_table)
    
    # Return a list of latency tables for each instrument across all cycles
    return instrument_latency_tables



if __name__ == '__main__':
    # Check command-line argument
    if len(sys.argv) != 2:
        print("Usage: python report_latency.py <directory>")
        sys.exit(1)

    data_dir = sys.argv[1]


# Mindo's data on hercules:
# data_dir = '/work/noaa/da/marineda/gfs-marine/data/obs/gfs.20230425'

# bufr_latency = combine_bufr_latency_tables(data_dir)
# print("Combined Atmos Latency Table:", bufr_latency)

ocean_latency = combine_ocean_latency_tables(data_dir)
# print("Combined Ocean Latency Tables by Instrument:", ocean_latency)

# print(type(ocean_latency))

for instrument_dir, latency_table in ocean_latency.items():
    print(f'{instrument_dir}')
    latency_stats(latency_table)
    # print_latency_table(latency_table)


bufr_latency_table = combine_bufr_latency_tables(data_dir)
print_latency_table(bufr_latency_table)
