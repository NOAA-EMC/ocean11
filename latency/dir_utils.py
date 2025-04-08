import os
import time



# return a list of paths for all files in a dir
def dir_file_paths(directory):

    # Check if directory exists
    # if not os.path.isdir(directory):
        # raise ValueError(f"{directory} is not a valid directory")

    real_dir = is_dir_or_symlink_to_dir(directory)
    if not real_dir:
        return None

    path_list = []
    # Iterate through all files in the directory
    for filename in os.listdir(real_dir):
        filepath = os.path.join(real_dir, filename)
        # Skip if it's not a file
        if os.path.isfile(filepath):
            path_list.append(filepath)
        else:
            continue

    return path_list


    
# case insensitive
def select_by_instrument(files, instrument_name):
    # print(f"selecting for instrument |{instrument_name}|")
    filtred_files = []
    for file in files:
        if instrument_name.lower() in file.lower():  # (case insensitive)
            filtred_files.append(file)
            # print(f'matching..... |{file}|')
    return filtred_files



def is_file_or_symlink_to_file(path):
    # Check if the path is a regular file or symlink to a file
    return os.path.isfile(path) or (os.path.islink(path) and os.path.isfile(os.path.realpath(path)))

def is_dir_or_symlink_to_dir(path):
    # Check if the path is a directory or symlink to a directory
    if os.path.isdir(path):
        return path
    elif os.path.islink(path):
        real_path = os.path.realpath(path)
        if os.path.isdir(real_path):
            return real_path
    return None

# def get_files_in_dir(path):
    # # Check if the path is a directory or symlink to a directory
    # real_dir = is_dir_or_symlink_to_dir(path)
    # if real_dir:
        # files = []
        # # Walk through the directory and get all file paths
        # for root, dirs, files_in_dir in os.walk(real_dir):
            # for file in files_in_dir:
                # files.append(os.path.join(root, file))
        # return files
    # return []







# follows sym links
# returns empty list if dir doesn't exist
def list_files_recursive_relative_path(directory):
    files_list = []
    for root, _, files in os.walk(directory, followlinks=True):
        for file in files:
            # Get the full path of the file
            file_path = os.path.join(root, file)
            # Get the relative path of the file from the directory
            relative_path = os.path.relpath(file_path, directory)
            files_list.append(relative_path)
    return files_list


'''
def list_files(input_dir_path):
    # logger.debug(f"Preparing a list of files.")
    # files = get_dir_files(input_dir_path)
    # files = list_files_in_subdirectories(input_dir_path)
    # files = list_files_recursive_relative_path(input_dir_path)
    files = []
    for dir in input_dir_path:
        dir_files = list_files_recursive_relative_path(input_dir_path)
        # files.append(dir_files)
        files.extend(dir_files)

    # print(f"files >>>>>>>>>>>>>>>>>>> {type(files)} length = {len(files)}")
    # print(f"files[0] >>>>>>>>>>>>>>>>>>> {type(files[0])} length = {len(files[0])}")

    return files
'''
