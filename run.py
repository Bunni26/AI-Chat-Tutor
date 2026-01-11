import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import app

if __name__ == '__main__':
    app.run(debug=True, port=5000)
