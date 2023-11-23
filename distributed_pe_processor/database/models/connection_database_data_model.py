from dataclasses import dataclass


@dataclass
class ConnectionDatabaseDataModel:
    url: str
    properties: str
    table_name: str



