import os
from src.util import encrypt_externally, decrypt_externally
import json


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
    # full_path = os.path.join(dir_path, file_name)
    full_path = os.path.join(dir_path, "keys", file_name)

    # Check if the file exists
    if os.path.exists(full_path):
        return True
    else:
        return False

def create_requirement_file(file_name, input):
    dir_path = os.path.dirname(os.path.realpath(__file__))  
    # full_path = os.path.join(dir_path, file_name)
    full_path = os.path.join(dir_path, "keys", file_name)
    if file_name[0] == '.':
        encrypt_externally(input, file_name)
    else:
        parts = file_name.split('.')
        if len(parts) > 1:
            if parts[-1] == 'json':
                try:
                    json.loads(input)
                    with open(full_path, 'w') as file:
                        json.dump(input, file, indent=4)
                except ValueError:
                    raise ValueError("Input must be in JSON form!")
                
            elif parts[-1] == 'txt':
                with open(full_path, 'w') as file:
                    file.write(input)

def get_requirement_file(file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))  
    # full_path = os.path.join(dir_path, file_name)
    full_path = os.path.join(dir_path, file_name)
    if file_name[0] == '.':
        full_path = os.path.join(dir_path, "keys", file_name)
        try:
            return decrypt_externally(file_name)
        except: 
            return ""
    else:
        parts = file_name.split('.')
        if len(parts) > 1:
            if parts[-1] == 'json':
                try:
                    with open(full_path, 'r') as json_file:
                        data = json.load(json_file)
                        # Convert JSON data to string
                        json_string = json.dumps(data)
                        return json_string
                except:
                    return ""
            elif parts[-1] == 'txt':
                try:
                    with open(full_path, 'r') as text_file:
                        text_string = text_file.read()
                        return text_string
                except:
                    return ""