import snowflake.connector
import json
import sys
from pathlib import Path

if __name__ == '__main__':
    current_dir = Path(__file__).parent.absolute()
    project_root = current_dir.parent.parent
    sys.path.insert(0, str(project_root))

from src.util import get_requirement_file
class SnowflakeInstance:
    def __init__(self, config_file='snowflake_connector.json'):
        try:
            config = get_requirement_file(config_file)[1]
            self.account = config['account']
            self.user = config['user']
            self.password = config['password']
            self.database = config['database']
            self.warehouse = config['warehouse']

        except FileNotFoundError:
            print(f"Config file '{config_file}' not found.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from '{config_file}'.")
    
    def get_config(self):
        config = {}
        config['account'] = self.account
        config['user'] = self.user
        config['password'] = self.password
        config['database'] = self.database
        config['warehouse'] = self.warehouse
        return config

    def connect(self):
        try:
            self.connection = snowflake.connector.connect(
                account=self.account,
                user=self.user,
                password=self.password,
                database=self.database,
                warehouse=self.warehouse,
                role=self.role
            )
            self.cursor = self.connection.cursor()
            print("Connected to Snowflake successfully.")
        except Exception as e:
            print("Error connecting to Snowflake:", str(e))

def main():
    a= SnowflakeInstance()
    print(a.get_config())

if __name__ == "__main__":
    main()