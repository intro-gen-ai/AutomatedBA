import snowflake.connector
import json
import sys
from pathlib import Path
import pandas as pd

if __name__ == '__main__':
    current_dir = Path(__file__).parent.absolute()
    project_root = current_dir.parent.parent
    sys.path.insert(0, str(project_root))

from src.util import validate_file_exists, create_requirement_file, get_requirement_file

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

    def query_df(self, sql):
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return pd.DataFrame(rows, columns=columns)
        finally:
            cursor.close()

        # cursor = self.conn.cursor()
        # try:
        #     cursor.execute(sql)
        #     return cursor.fetch_pandas_all()
        # finally:
        #     cursor.close()

    def connect(self, db = None):
        if db != None:
            self.database = db
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

    def fetch_metadata(self):
        self.connect()
        # manager = SnowflakeManager()
        data = (self.query_df("SHOW DATABASES"))['name']
        databases = [x for x in data if x not in ('SNOWFLAKE', 'SNOWFLAKE_SAMPLE_DATA', 'TASTY_BITES_DB', 'TASTY_BITES_SAMPLE_DATA')]

        db_structure = {}
        for db in databases:
            d1 = (self.query_df(f"SHOW SCHEMAS IN DATABASE {db}"))['name']
            schemas = [x for x in d1 if x not in ('INFORMATION_SCHEMA')]
            db_structure[db] = {}
            for schema in schemas:
                tables = (self.query_df(f"SHOW TABLES IN SCHEMA {db}.{schema}"))['name']
                db_structure[db][schema] = {}
                for table in tables:
                    columns = (self.query_df(f"DESCRIBE TABLE {db}.{schema}.{table}"))[['name','type']]
                    table_structure = columns.set_index('name')['type'].to_dict()

                    # table_structure = {}
                    # for column in columns:
                    #     column_name = column[0]  # Adjust index based on your query's result set
                    #     data_type = column[1]  # Adjust index based on your query's result set
                    #     table_structure[column_name] = data_type
                    
                    db_structure[db][schema][table] = table_structure

        return db_structure
    
    def set_schema(self, schema_file = "config_storage/snowflake_schema.json"):
        if hasattr(self, 'schema') and self.schema:
            return
        if validate_file_exists(schema_file):
            self.schema = get_requirement_file(schema_file)[1]
        else:
            temp = self.fetch_metadata()
            create_requirement_file(file_name = schema_file, input = temp)
            self.schema = temp

    def get_schema(self):
        if hasattr(self, 'schema') and self.schema:
            return self.schema
        else:
            self.set_schema()
            return self.schema
            
# if __name__ == '__main__':
#     a = SnowflakeManager()
#     a.set_config()
#     a.connect()
#     b = (a.query_df("SHOW DATABASES"))['name']
#     b = b.tolist()
#     schemas = (a.query_df(f"SHOW SCHEMAS IN DATABASE {b[1]}"))['name']
#     schemas = schemas.tolist()
#     print(schemas)
#     sc = (a.query_df(f"SHOW TABLES IN SCHEMA {b[1]}.{schemas[1]}"))['name']
#     print(sc) 
#     columns = a.query_df(f"SHOW COLUMNS IN TABLE {b[1]}.{schemas[1]}.{sc[1]}")[['column_name','data_type']]
#     print(columns.head(10))
#     column = (a.query_df(f"SHOW COLUMNS IN TABLE {b[1]}.{schemas[1]}.{sc[1]}"))[['column_name','data_type']]
#     print(f"{b[1]}.{schemas[1]}.{sc[1]}")
#     di = column.set_index('column_name')['data_type'].to_dict()
#     print(di)
#     columns = (a.query_df(f"DESCRIBE TABLE {b[1]}.{schemas[1]}.{sc[1]}"))[['name','type']]
#     table_structure = columns.set_index('name')['type'].to_dict()
#     print(table_structure)
    