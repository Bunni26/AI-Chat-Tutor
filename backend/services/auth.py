import jwt
from datetime import datetime, timedelta
from contextlib import contextmanager
from flask import current_app, request, jsonify
from functools import wraps

from backend.database import SessionLocal
from backend.models import User

@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class AuthService:
    def __init__(self, app=None):
        if app:
            self.secret_key = app.config.get('SECRET_KEY', 'your-secret-key-here')
        else:
            self.secret_key = 'your-secret-key-here'
        self.expiration_minutes = 60

    def create_token(self, user_id, email):
        payload = {
            'user_id': user_id,
            'email': email,
            'exp': datetime.utcnow() + timedelta(minutes=self.expiration_minutes)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')

    def verify_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def register_user(self, username, email, password):
        with get_db_session() as db:
            existing_user = db.query(User).filter(
                (User.email == email) | (User.username == username)
            ).first()
            if existing_user:
                raise ValueError('Username or email already registered')

            user = User(username=username, email=email)
            user.set_password(password)
            db.add(user)
            db.commit()
            db.refresh(user)  # Ensures data is loaded before session closes

            # ✅ Return plain dict to avoid DetachedInstanceError
            return {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }

    def login_user(self, email, password):
        with get_db_session() as db:
            user = db.query(User).filter_by(email=email).first()
            if not user or not user.check_password(password):
                raise ValueError('Invalid email or password')

            token = self.create_token(user.id, user.email)
            return {
                'token': token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }

# ✅ Token Required Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        try:
            token = token.replace('Bearer ', '')
            auth_service = AuthService()
            payload = auth_service.verify_token(token)
            if not payload:
                return jsonify({'error': 'Invalid token'}), 401
            request.user = payload
        except Exception:
            return jsonify({'error': 'Token verification failed'}), 401
        return f(*args, **kwargs)
    return decorated