import snowflake.connector
import json
import sys
from pathlib import Path

if __name__ == '__main__':
    current_dir = Path(__file__).parent.absolute()
    project_root = current_dir.parent.parent
    sys.path.insert(0, str(project_root))

from src.util import get_requirement_file

class SnowflakeManager:
    _instance = None

    def __new__(cls, config_file="config_storage/snowflake_connector.json"):
        if cls._instance is None:
            cls._instance = super(SnowflakeManager, cls).__new__(cls)
            try:
                config = get_requirement_file(config_file)[1]
                cls._instance.account = config['account']
                cls._instance.user = config['user']
                cls._instance.password = config['password']
                cls._instance.database = config['database']
                cls._instance.warehouse = config['warehouse']

            except FileNotFoundError:
                print(f"Config file '{config_file}' not found.")
            except json.JSONDecodeError:
                print(f"Error decoding JSON from '{config_file}'.")
            # Initialize your Snowflake connection here
            # try:
            #     config = get_requirement_file(config_file)[1]
            #     cls._instance.conn = snowflake.connector.connect(
            #         user= config['user'],
            #         password= config['password'],
            #         account= config['account']
            #     )
            # except FileNotFoundError:
            #     print(f"Config file '{config_file}' not found.")
            # except json.JSONDecodeError:
            #     print(f"Error decoding JSON from '{config_file}'.")
        return cls._instance

    def set_config(self, config_file="config_storage/snowflake_connector.json", args = None):
        try:
            config = get_requirement_file(config_file)[1]
            if isinstance(args, dict):
                if 'account' in args:
                    self.account = args['account']
                else:
                    self.account = config['account']

                if 'user' in args:
                    self.user = args['user']
                else:
                    self.user = config['user']

                if 'password' in args:
                    self.password = args['password']
                else:
                    self.password = config['password']

                if 'database' in args:
                    self.database = args['database']
                else:
                    self.database = config['database']

                if 'warehouse' in args:
                    self.warehouse = args['warehouse']
                else:
                    self.warehouse = config['warehouse']
            else:
                self.account = config['account']
                self.user = config['user']
                self.password = config['password']
                self.database = config['database']
                self.warehouse = config['warehouse']

        except FileNotFoundError:
            if isinstance(args, dict):
                if 'account' in args:
                    self.account = args['account']
                if 'user' in args:
                    self.user = args['user']
                if 'password' in args:
                    self.password = args['password']
                if 'database' in args:
                    self.account = args['database']
                if 'warehouse' in args:
                    self.account = args['warehouse']
            print(f"Config file '{config_file}' not found.")
        except json.JSONDecodeError:
            if isinstance(args, dict):
                if 'account' in args:
                    self.account = args['account']
                if 'user' in args:
                    self.user = args['user']
                if 'password' in args:
                    self.password = args['password']
                if 'database' in args:
                    self.account = args['database']
                if 'warehouse' in args:
                    self.account = args['warehouse']
            print(f"Error decoding JSON from '{config_file}'.")

    def get_config(self):
        config = {}
        config['account'] = self.account
        config['user'] = self.user
        config['password'] = self.password
        config['database'] = self.database
        config['warehouse'] = self.warehouse
        return config
            
    def query(self, sql):
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
    
    def connect(self):
        if not (self.account or self.user or self.password):
            raise ValueError("Invalid Config !!! Ensure Config is Set")
        try:
            self.conn = snowflake.connector.connect(
                account=self.account,
                user=self.user,
                password=self.password,
                database=self.database,
                warehouse=self.warehouse
                # role=self.role
            )
            # self.cursor = self.connection.cursor()
            print("Connected to Snowflake successfully.")
        except Exception as e:
            print("Error connecting to Snowflake:", str(e))

    def fetch_metadata():
        manager = SnowflakeManager()
        databases = manager.query("SHOW DATABASES")

        db_structure = {}
        for db in databases:
            
            db_name = db[1]  # Adjust index based on your query's result set
            schemas = manager.query(f"SHOW SCHEMAS IN DATABASE {db_name}")
            
            db_structure[db_name] = {}
            for schema in schemas:
                schema_name = schema[1]  # Adjust index based on your query's result set
                tables = manager.query(f"SHOW TABLES IN SCHEMA {db_name}.{schema_name}")
                
                db_structure[db_name][schema_name] = {}
                for table in tables:
                    table_name = table[1]  # Adjust index based on your query's result set
                    columns = manager.query(f"SHOW COLUMNS IN TABLE {db_name}.{schema_name}.{table_name}")
                    
                    table_structure = {}
                    for column in columns:
                        column_name = column[2]  # Adjust index based on your query's result set
                        data_type = column[7]  # Adjust index based on your query's result set
                        table_structure[column_name] = data_type
                    
                    db_structure[db_name][schema_name][table_name] = table_structure

        return db_structure
    
if __name__ == '__main__':
    a = SnowflakeManager()
    a.set_config()
    a.connect()
    print("success!")
    