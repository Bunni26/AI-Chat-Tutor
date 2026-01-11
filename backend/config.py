import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
# Use SQLite for development if MySQL env vars are not set
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

if all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    # Use MySQL if all environment variables are set
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    # Fallback to SQLite for development
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ai_coding_tutor.db')
    DATABASE_URL = f"sqlite:///{db_path}"
    print(f"Using SQLite database at: {db_path}")

# OpenAI / GROQ Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')