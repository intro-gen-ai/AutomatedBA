import json
import os

class ControlDict:
    _instance = None
    file_path = os.path.join(os.path.dirname(__file__), 'convert.json')

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ControlDict, cls).__new__(cls)
            cls._instance.data_dict = cls._read_dict_from_file(cls)
        return cls._instance

    @staticmethod
    def _write_dict_to_file(data_dict):
        """Write the dictionary to a JSON file."""
        with open(ControlDict.file_path, 'w') as file:
            json.dump(data_dict, file)

    @staticmethod
    def _read_dict_from_file(self):
        """Read and determine the format of the dictionary from the JSON file, converting if necessary."""
        try:
            with open(ControlDict.file_path, 'r') as file:
                data = json.load(file)
                check = False
                ret = data
                # Check if the dictionary is flat or nested
                if isinstance(data, dict):
                    # Check the first key to determine the format
                    first_key = next(iter(data))
                    if isinstance(first_key, str) and '(' in first_key and ')' in first_key:
                        # Assuming flat format with keys like '(char, num)'
                        nested_dict = {}
                        for key, value in data.items():
                            # Strip the parentheses and split by comma
                            key_tuple = key.strip('()').split(',', 1)
                            char = key_tuple[0].strip("'")
                            num = key_tuple[1].strip()
                            if char not in nested_dict:
                                nested_dict[char] = {}
                            nested_dict[char][num] = value
                        ret = nested_dict
                        check = True
                    else:
                        # Assuming it's already in the desired nested format
                        ret = data
            if check:
                _backup_and_rewrite_file(ControlDict.file_path, ret)
            return ret
        except FileNotFoundError:
            return {}

    def convert(self, char, num):
        """Return the value corresponding to the given (char, num) key from the loaded dictionary."""
        # temp = self.data_dict.get(char, {})
        # temp1 = temp.get(str(num), None)
        return self.data_dict.get(char, {}).get(str(num), None)  # Returns None if the key or char is not found

    def update(self, char, num, value):
        """Add or update a key-value pair in the dictionary and update the JSON file."""
        if char not in self.data_dict:
            self.data_dict[char] = {}
        self.data_dict[char][num] = value  # Update or add the key-value pair
        self._write_dict_to_file(self.data_dict)  # Write the updated dictionary back to the file

    def get_set(self, input):
        if input == None:
            return list(self.data_dict.keys())
        elif input in self.data_dict.keys():
            if isinstance(self.data_dict[input], dict):
                return list(self.data_dict[input].keys()), list(self.data_dict[input].values())
            else:
                raise ValueError("The value is not a dict")
        else:
            raise KeyError(f"Key '{input}' not found in the outer dictionary.")
    
    def get_dict(self, input):
        if input == None:
            return self.data_dict
        elif input in self.data_dict.keys():
            return self.data_dict[input]
        else:
            raise KeyError(f"Key '{input}' not found in the outer dictionary.")

def _backup_and_rewrite_file(file_path, nested_dict):
    base, extension = os.path.splitext(file_path)
    backup_file_path = f"{base}_oldForm{extension}"

    # rename 
    os.rename(file_path, backup_file_path)
    # overwrite
    with open(file_path, 'w') as file:
        json.dump(nested_dict, file)  