# This function is built because db initialization
# and alembic migration cannot read data from loaded
# .env file in main.py

# Currently it only used by db.py and alembic/env.py

# Function may not be used in production.
# Set env variables using docker-compose.yml instead.

# from dotenv import load_dotenv

import os
from pathlib import Path
from dotenv import load_dotenv

# Get the absolute path to the .env.development file
base_dir = Path(__file__).resolve().parent
env_path = os.path.join(base_dir, '.env.development')

# Load environment variables once
load_dotenv(env_path)

def get_env(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        print(f"Warning: Environment variable {key} not found")
    return value