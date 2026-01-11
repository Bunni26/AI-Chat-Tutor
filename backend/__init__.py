from backend.app import app
from backend.config import DATABASE_URL
from backend.database import get_db_session  # ✅ now this will work
from backend.models import User, Conversation