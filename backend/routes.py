from flask import Blueprint, request, jsonify
from backend.models import User, Conversation
from backend.database import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

bp = Blueprint('api', __name__)

@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not all([username, email, password]):
            return jsonify({'error': 'All fields are required'}), 400

        db = next(get_db())
        
        # Check if user already exists
        existing_user = db.query(User).filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 400

        # Create new user
        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )
        db.add(new_user)
        db.commit()
        
        return jsonify({'message': 'User registered successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        db = next(get_db())
        user = db.query(User).filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return jsonify({'error': 'Invalid credentials'}), 401

        return jsonify({
            'message': 'Login successful',
            'user_id': user.id,
            'username': user.username
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_id = data.get('user_id')
        message = data.get('message')

        if not user_id or not message:
            return jsonify({'error': 'User ID and message are required'}), 400

        db = next(get_db())
        
        # Save conversation
        conversation = Conversation(
            user_id=user_id,
            conversation_text=message,
            conversation_date=datetime.now()
        )
        db.add(conversation)
        db.commit()
        
        return jsonify({
            'message': 'Chat saved successfully',
            'conversation_id': conversation.id
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/chat/history/<int:user_id>', methods=['GET'])
def get_chat_history(user_id):
    try:
        db = next(get_db())
        
        # Get user's chat history
        conversations = db.query(Conversation).filter_by(user_id=user_id).all()
        
        return jsonify({
            'conversations': [
                {
                    'id': conv.id,
                    'message': conv.conversation_text,
                    'timestamp': conv.conversation_date.strftime('%Y-%m-%d %H:%M:%S')
                }
                for conv in conversations
            ]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
