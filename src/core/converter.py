import json
import os

class ControlDict:
    _instance = None
    file_path = os.path.join(os.path.dirname(__file__), 'convert.json')
    mode = 1

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ControlDict, cls).__new__(cls)
            cls._instance.data_dict = cls._read_dict_from_file()
        return cls._instance

    @staticmethod
    def _write_dict_to_file(data_dict):
        """Write the dictionary to a JSON file."""
        with open(ControlDict.file_path, 'w') as file:
            json.dump(data_dict, file)

    @staticmethod
    def _read_dict_from_file():
        """Read and return the dictionary from the JSON file."""
        a = os.getcwd()
        b = ControlDict.file_path
        try:
            with open(ControlDict.file_path, 'r') as file:
                data_dict = json.load(file)
                return data_dict
        except FileNotFoundError:
            return {}

    def convert(self, key):
        """Return the value corresponding to the given key from the loaded dictionary."""
        return self.data_dict.get(key, None)  # Returns None if the key is not found

    def update(self, key, value):
        """Add or update a key-value pair in the dictionary and update the JSON file."""
        self.data_dict[key] = value  # Update or add the key-value pair
        self._write_dict_to_file(self.data_dict)  # Write the updated dictionary back to the file


# import json

# def write_dict(data_dict, file_path):
#     """Write the dictionary to a JSON file."""
#     with open(file_path, 'w') as file:
#         json.dump(data_dict, file)

# def read_dict(file_path):
#     """Read and return the dictionary from the JSON file."""
#     try:
#         with open(file_path, 'r') as file:
#             data_dict = json.load(file)
#             return data_dict
#     except FileNotFoundError:
#         return {} 

# class ControlDict:

#     def __init__(self, decorated):
#         self.decorated = decorated

#     def instance(self):
#         try:
#             return self._instance
#         except AttributeError:
#             self._instance = self._decorated()
#             return self.instance
    
#     def __call__(self):
#         raise TypeError('Singletons must be accessed through instance()')
        
#     def __instancecheck__(self, inst):
#         return isinstance(inst, self._decorated)

