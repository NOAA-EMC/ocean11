#!/usr/bin/env python3
# exglobal_prep_ocean_obs.py
import os
import yaml
import argparse

from wxflow import Logger, cast_strdict_as_dtypedict
from prep_ocean_obs import PrepOceanObs


# Initialize root logger
logger = Logger(level='DEBUG', colored_log=True)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--config',
        type=str,
        help='Input YAML configuration', required=True
    )   
    args = parser.parse_args()
    config_file = args.config
    return config_file


def read_yaml_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)  # Parse YAML into a Python dictionary
            print("YAML contents:")
            # print(data)  # Simple print
            # Pretty print with formatting
            # print("\nPretty printed:")
            print(yaml.dump(data, indent=2))
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
    return data







if __name__ == '__main__':

    # Take configuration from environment and cast it as python dictionary
    config = cast_strdict_as_dtypedict(os.environ)

    config_file_name = parse_arguments()
    main_config = read_yaml_file(config_file_name)

    PDY = main_config["PDY"]
    cyc = main_config["cyc"]
    assim_freq = main_config["assim_freq"]
    RUN = main_config["RUN"]
    conversion_list_file_name = main_config["conversion_list_file_name"]
    save_list_file_name = main_config["save_list_file_name"]
    input_dir = main_config["input_dir"]
    output_dir = main_config["output_dir"]
    scratch_dir = main_config["scratch_dir"]

    print(f"PDY = {PDY}")
    print(f"cyc = {cyc}")
    print(f"assim_freq = {assim_freq}")
    print(f"RUN = {PDY}")
    print(f"conversion_list_file_name = {conversion_list_file_name}")
    print(f"save_list_file_name = {save_list_file_name}")
    print(f"input_dir = {input_dir}")
    print(f"output_dir = {output_dir}")
    print(f"scratch_dir = {scratch_dir}")



    

    # Instantiate the prepocnobs task
    PrepOcnObs = PrepOceanObs(config, main_config)
    PrepOcnObs.initialize()
    PrepOcnObs.run()
    PrepOcnObs.finalize()
