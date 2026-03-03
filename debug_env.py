import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path("c:/Users/Nejdet TUT/Desktop/lms-yapayzeka-final-104/.env")
print(f"File exists: {env_path.exists()}")
load_dotenv(dotenv_path=env_path)

print(f"GEMINI_API_KEY: '{os.getenv('GEMINI_API_KEY')}'")
print(f"Keys in environ: {[k for k in os.environ.keys() if 'API' in k]}")
