import json
import os
from dataclasses import dataclass


@dataclass
class ServerConfig:
    port: int
    host: str
    debug: bool


@dataclass
class DatabaseConfig:
    hostname: str
    username: str
    password: str
    database: str
    instance: str
    driver: str = None

class Config:
    server: ServerConfig
    database: DatabaseConfig
    config_path: str = None

    def init_from_jsonfile(self, config_path=None):
        if config_path is None:
            self.config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "config.json",
            )
        with open(self.config_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)
            self.server = ServerConfig(**config_data["server"])
            self.database = DatabaseConfig(**config_data["database"])
    
    def from_dict(self, config_dict: dict):
        self.server = ServerConfig(**config_dict["server"])
        self.database = DatabaseConfig(**config_dict["database"])
    
    def to_dict(self) -> dict:
        return {
            "server": {
                "port": self.server.port,
                "host": self.server.host,
                "debug": self.server.debug,
            },
            "database": {
                "hostname": self.database.hostname,
                "username": self.database.username,
                "password": self.database.password,
                "database": self.database.database,
                "instance": self.database.instance,
                "driver": self.database.driver if self.database.driver else None,
            },
        }
