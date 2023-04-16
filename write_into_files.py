import os

# Define the code for each file
code_structure = {
    "app.py": "with open('input_file.txt', 'r') as file:\n    lines = file.readlines()\n    line_count = len(lines)\n    print(f'Number of lines: {line_count}')",
    "templates/index.html": "def double_count(count):\n    return count * 2"
}

def write_code_to_files(parent_dir, code_structure):
    """
    Write the provided code to the respective files in the specified parent directory.
    """
    for filepath, code in code_structure.items():
        # Create the full file path
        full_path = os.path.join(parent_dir, filepath)

        # Create the directories if they don't exist
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # Write the code to the file
        with open(full_path, 'w') as file:
            file.write(code)

# Set the name of the root directory
root_dir = 'projects'

# Write the code to the respective files
write_code_to_files(root_dir, code_structure)
