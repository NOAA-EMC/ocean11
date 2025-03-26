#!/usr/bin/env python3
from netCDF4 import Dataset
import sys

def is_netcdf_file(filepath):
    try:
        with Dataset(filepath, 'r'):
            return True
    except Exception:
        return False

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python check_if_netcdf_file.py <filepath>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    if is_netcdf_file(filepath):
        print(f"{filepath} is a NetCDF file")
    else:
        print(f"{filepath} is not a NetCDF file")
