import os
from dotenv import load_dotenv

load_dotenv()

# Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SALT = os.getenv("DATA_SALT", "replace_with_random_salt")

# Data storage
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
DATA_FILE = os.path.join(DATA_DIR, "candidates.json")

EXIT_KEYWORDS = {"exit", "quit", "bye", "goodbye", "stop", "end"}
