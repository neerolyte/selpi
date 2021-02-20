from dotenv import load_dotenv
from pathlib import Path
import os

# Preference order will be:
#  1) existing environment variables
#  2) .env.local
#  3) .env.dist
# .env.local is used instead of .env to avoid interacting with pipenv
load_dotenv(dotenv_path=Path('.') / '.env.local')
load_dotenv(dotenv_path=Path('.') / '.env.dist')

def getb(key: bytes) -> bytes:
    return os.getenvb(b'SELPI_' + key)
