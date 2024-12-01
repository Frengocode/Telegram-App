from dotenv import load_dotenv
import os

load_dotenv()

PG_USERNAME = os.getenv("PG_USERNAME", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "python$_venv")
PG_HOST = os.getenv("PG_HOST", "localhost:5432")
