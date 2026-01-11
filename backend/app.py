import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from backend.config import DATABASE_URL
from backend.services.bot import BotService

db = SQLAlchemy()

app = Flask(__name__)
CORS(app)

# Load environment variables
load_dotenv()

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

db.init_app(app)

# Initialize services
bot_service = BotService()

# Chat route - no authentication required
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message')
        context = data.get('context', [])

        # Process the message
        response = bot_service.process_message(user_message, context)
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/debug', methods=['POST'])
def debug_code():
    try:
        data = request.json
        code = data.get('code')
        language = data.get('language')

        result = bot_service.debug_code(code, language)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/optimize', methods=['POST'])
def optimize_code():
    try:
        data = request.json
        code = data.get('code')
        language = data.get('language')

        result = bot_service.optimize_code(code, language)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)