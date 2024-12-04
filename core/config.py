from dotenv import load_dotenv
import os

load_dotenv()

PG_USERNAME = "postgres"
PG_PASSWORD = "python$_venv"
PG_HOST = "localhost:5432"
SECRET_KEY = os.getenv("SECRET_KEY")
