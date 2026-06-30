import os
import sqlite3
from sqlite3 import Connection

class DbConnectionHandler:
    def __init__(self) -> None:
        self.__connection_string = "storage.db"
        self.__conn = None

    def connect(self) -> None:
        # Check if database needs initialization before connecting
        db_exists = os.path.exists(self.__connection_string) and os.path.getsize(self.__connection_string) > 0
        
        conn = sqlite3.connect(self.__connection_string, check_same_thread=False)
        self.__conn = conn
        
        if not db_exists:
            self.__init_database()
    
    def get_connection(self) -> Connection:
        return self.__conn

    def __init_database(self) -> None:
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        schema_path = os.path.join(project_root, "init", "schema.sql")
        
        if os.path.exists(schema_path):
            with open(schema_path, "r") as f:
                schema_script = f.read()
            try:
                self.__conn.executescript(schema_script)
                self.__conn.commit()
            except Exception as e:
                raise Exception(f"Failed to initialize database schema: {e}")
    

db_connection_handler = DbConnectionHandler()
