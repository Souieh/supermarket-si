import json
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure


class Database:
    _instance = None
    _config_file = "config.json"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.client = None
            cls._instance.db = None
            cls._instance.config = cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        if os.path.exists(self._config_file):
            with open(self._config_file, "r") as f:
                return json.load(f)
        return None

    def save_config(self, host, port, db_name, username=None, password=None):
        config = {
            "host": host,
            "port": int(port),
            "db_name": db_name,
            "username": username,
            "password": password
        }
        with open(self._config_file, "w") as f:
            json.dump(config, f)
        self.config = config

    def connect(self):
        if not self.config:
            return False, "Configuration not found"
        try:
            kwargs = {
                "host": self.config["host"],
                "port": self.config["port"],
                "serverSelectionTimeoutMS": 2000
            }
            if self.config.get("username") and self.config.get("password"):
                kwargs["username"] = self.config["username"]
                kwargs["password"] = self.config["password"]
                kwargs["authSource"] = "admin"

            self.client = MongoClient(**kwargs)
            # Check connection
            self.client.admin.command('ping')
            self.db = self.client[self.config["db_name"]]
            return True, "Connected successfully"
        except (ConnectionFailure, OperationFailure) as e:
            return False, str(e)

    def get_collection(self, name):
        if self.db is not None:
            return self.db[name]
        return None

    def better_get_collection(self, name):
        if name is None:
            raise Exception("Collection name cannot be None")

        if self.db is None:
            raise Exception("Database instance not initialized")
        collection = self.get_collection(name)
        if collection is None:
            raise Exception(f"Collection '{name}' not found")
        return collection

    def run_transaction(self, callback):
        """
        Runs a callback within a session and transaction.
        Note: Transactions require a replica set in MongoDB.
        For standalone instances, we fallback to non-transactional execution.
        """
        if self.client is None:
            raise Exception("Database not connected")

        try:
            with self.client.start_session() as session:
                with session.start_transaction():
                    return callback(session)
        except OperationFailure as e:
            # Fallback if transactions are not supported (e.g., standalone)
            if "Transaction" in str(e) or "replica set" in str(e):
                return callback(None)
            raise e
