import os
from sqlalchemy import create_engine, text
import psycopg2

class DataBase:
    def __init__(self, db_configs):
        self.configs = db_configs
        try:
            self.engine = create_engine(f"postgresql+psycopg2://{self.configs['USER']}:{self.configs['PASSWORD']}@{self.configs['HOST']}:{self.configs['HOST_PORT']}/{self.configs['DATA_BASE']}")
        except Exception as e:
             print(f"Error occurred while creating database engine: {e}")
             self.engine = None
    def SchemaIfo(self, schema_name):
            """
            Creates a schema in the database if it does not already exist.

            Args:
                schema_name (str): The name of the schema to be created.
            """
            schema_info_context =f"DataBase schema info : {schema_name} \n"
            try:
                with self.engine.connect() as connection:
                    # retrieve the list of tables in the schema
                    results = connection.execute(text(f"SELECT table_name FROM information_schema.tables WHERE table_schema = :schema"), {'schema': schema_name})
                    tables = results.fetchall()
                    # iterate through the tables and retrieve their column information
                    for table in tables:
                        schema_info_context += f"Table: {table[0]}\n"
                        results = connection.execute(text(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = :schema AND table_name = :table"), {'schema': schema_name, 'table': table[0]})
                        columns = results.fetchall()
                        # iterate through the columns and retrieve their data types
                        for column in columns:
                            column_name , data_type = column
                            schema_info_context += f"Column: {column_name}, Data Type: {data_type}\n"
                        # adding sample data for each table
                        results = connection.execute(text(f"SELECT * FROM {schema_name}.{table[0]} LIMIT 5;"))
                        sample_data = results.fetchall()
                        schema_info_context += f"Sample Data: {sample_data}\n"
                        for row in sample_data:
                            schema_info_context += f"Row: {row}\n"
            except Exception as e:
                print(f"Error occurred while creating schema '{schema_name}': {e}")
            return schema_info_context
    def execute_query(self, query):
        try:
            with self.engine.connect() as connection:
                results = connection.execute(text(query))
                return results.fetchall()
        except Exception as e:
            print(f"Error occurred while executing query: {e}")
            return []





