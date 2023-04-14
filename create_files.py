import json
import os

# with open('files/p1.txt', 'r') as f:
#     file_structure = json.load(f)
file_structure={"main.py":"","utilities":{"utility.py":""}}
def create_file_structure(parent_dir, file_structure):
    """
    Recursively create the file structure defined by a nested dictionary.
    """
    for name, value in file_structure.items():
        if isinstance(value, dict):
            # If the value is a dictionary, create a subdirectory and recursively call this function.
            subdir = os.path.join(parent_dir, name)
            os.makedirs(subdir, exist_ok=True)
            create_file_structure(subdir, value)
        else:
            # If the value is a string, create a file with the specified extension.
            filename = f'{name}.{value}'
            filepath = os.path.join(parent_dir, filename)
            with open(filepath, 'w') as f:
                pass  # Do nothing, just create an empty file.

# Set the name of the root directory
root_dir = 'projects'

# Create the file structure in the current working directory.
create_file_structure(root_dir, file_structure)
