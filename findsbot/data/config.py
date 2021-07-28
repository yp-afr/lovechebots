import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN_FINDS")
PGUSER = os.getenv("PGUSER")
PGPASSWORD = os.getenv("PGPASSWORD")
PGHOST = os.getenv("PGHOST")
PGDATABASE = os.getenv("PGDATABASE")
SUPERUSER = os.getenv("SU")

POSTGRES_URI = f"postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}/{PGDATABASE}"
