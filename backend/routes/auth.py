import os
import sys
import traceback

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from flask import Blueprint, request, jsonify
from backend.services.auth import AuthService

auth_bp = Blueprint('auth', __name__)

# ✅ REGISTER ROUTE
@auth_bp.route('/register', methods=['POST'])
def register_user():
    auth_service = AuthService()
    try:
        data = request.get_json(force=True)
        print("Parsed JSON data:", data)

        if not data:
            return jsonify({'error': 'Invalid or missing JSON data'}), 400

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        print("Username:", username)
        print("Email:", email)
        print("Password:", "[REDACTED]")

        if not all([isinstance(username, str), isinstance(email, str), isinstance(password, str)]):
            return jsonify({'error': 'All fields must be strings'}), 400

        if not username.strip() or not email.strip() or not password.strip():
            return jsonify({'error': 'Username, email and password cannot be empty'}), 400

        user = auth_service.register_user(username, email, password)

        return jsonify({
            'message': 'User registered successfully',
            'user': user
        }), 201

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500

# ✅ LOGIN ROUTE — FIXED
@auth_bp.route('/login', methods=['POST'])
def login_user():
    auth_service = AuthService()
    try:
        data = request.get_json(force=True)
        print("Login request data:", data)

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        result = auth_service.login_user(email, password)
        
        print("Login result:", result)

        if not result or 'token' not in result:
            return jsonify({'error': 'Invalid email or password'}), 401

        return jsonify(result), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 401
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'Login failed: {str(e)}'}), 500

# ✅ GET CURRENT USER ROUTE
@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Token is missing'}), 401

    try:
        token = token.replace('Bearer ', '')
        auth_service = AuthService()
        payload = auth_service.verify_token(token)
        if not payload:
            return jsonify({'error': 'Invalid token'}), 401

        return jsonify({
            'user': {
                'id': payload['user_id'],
                'email': payload['email']
            }
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'Failed to get user'}), 500