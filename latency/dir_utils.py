import os


def dir_file_paths(directory):
    path_list = []

    # Check if directory exists
    if not os.path.isdir(directory):
        raise ValueError(f"{directory} is not a valid directory")

    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        # Skip if it's not a file
        if os.path.isfile(filepath):
            path_list.append(filepath)
        else:
            continue

    return path_list
