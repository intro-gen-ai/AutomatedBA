import os

def validate_file_exists(file_name):
    """
    Validates whether a file exists in a specified directory.

    Args:
    - file_name (str): The name of the file to validate.
    - dir_path (str): The directory path where the file should exist.

    Returns:
    - bool: True if the file exists in the specified directory, False otherwise.
    """
    # Construct the full path to the file
    dir_path = os.path.dirname(os.path.realpath(__file__))  
    full_path = os.path.join(dir_path, file_name)

    # Check if the file exists
    if os.path.exists(full_path):
        return True
    else:
        return False

