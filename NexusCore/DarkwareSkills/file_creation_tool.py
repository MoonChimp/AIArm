import os
from pathlib import Path

def create_file(file_name, content):
    """
    Create a new file with the specified name and content.

    Parameters:
        file_name (str): The name of the file to be created.
        content (str): The content to be written to the file.

    Returns:
        None
    """

    # Check if file already exists
    if os.path.exists(file_name):
        raise FileExistsError(f"File '{file_name}' already exists.")

    # Create directory if necessary
    file_path = Path(file_name)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Write content to file
    with open(file_name, 'w') as f:
        f.write(content)

# Usage examples
if __name__ == "__main__":
    create_file('example.txt', 'This is an example file.')