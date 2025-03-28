import sys
import netCDF4


def get_attr_by_name(file_path, name):
    dataset = netCDF4.Dataset(file_path, 'r')
    if name in dataset.ncattrs():
        return getattr(dataset, name)
    else:
        return None

def print_global_attributes(file_path):
    dataset = netCDF4.Dataset(file_path, 'r')
    print("Global Attributes:")
    for attr in dataset.ncattrs():
        print(f"{attr}: {getattr(dataset, attr)}")
        # if attr == 'date_created':
            # print('CCCCCCCCCCCC')

# # If you want to print attributes of a specific variable, you can do so:
# variable_name = 'your_variable_name'  # Replace with the name of the variable
# if variable_name in dataset.variables:
    # variable = dataset.variables[variable_name]
    # print(f"\nAttributes of variable '{variable_name}':")
    # for attr in variable.ncattrs():
        # print(f"{attr}: {getattr(variable, attr)}")

    dataset.close()


def print_var(file_path, variable_name):
    dataset = netCDF4.Dataset(file_path, 'r')

    if variable_name in dataset.variables:
        variable = dataset.variables[variable_name]
        print(f"\nAttributes of variable '{variable_name}':")
        for attr in variable.ncattrs():
            print(f"{attr}: {getattr(variable, attr)}")
    
        # Print the value of the variable
        print(f"\nValues of the variable '{variable_name}':")
        print(variable[:])  # Prints the entire array (it can be large!)

        dataset.close()



if __name__ == '__main__':
    # Check command-line argument
    if len(sys.argv) != 2:
        print("Usage: python print_nc_attributes.py <file>")
        sys.exit(1)
    
    nc_file = sys.argv[1]
    try:
        print_global_attributes(nc_file)
        name = 'date_created'
        print(f"{name}: {get_attr_by_name(nc_file, name)}")
        # print_var(nc_file, variable_name)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
