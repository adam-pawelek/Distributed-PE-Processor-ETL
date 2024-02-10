import os
import json


def load_config(environment):
    """
    Load JSON config based on the environment ('development' or 'production').
    """
    if environment not in ('development', 'production', 'e2e'):
        raise ValueError("environment must be either 'development', 'production' or 'e2e")

    config_path = os.path.join('config', f'{environment}.json')

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, 'r') as file:
        try:
            config = json.load(file)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError("Invalid JSON format", e.doc, e.pos) from None

    return config
