from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
CORS(app)

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

### TEST API ENDPOINTS ###
@app.route('/api/test_db', methods=['GET'])
def test_db():
    try:
        db.session.query(text("1")).from_statement(text("SELECT 1")).all()
        return jsonify({'message': 'Database connection successful.'}), 200
    except Exception as e:
        return jsonify({'message': 'Database connection failed.', 'error': str(e)}), 500

@app.route('/api/hello', methods=['GET'])
def get_hello():
    return jsonify({'message': 'Hello from Flask!'}), 200

### LOGIN/REGISTER API ENDPOINTS ###
@app.route('/api/register', methods=['POST'])
def register():
    # Get the password from the request
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Store the hashed password in the database instead of the plain one
    new_user = db

    return jsonify(message="User registered successfully"), 200

@app.route('/api/login', methods=['POST'])
def login():
    # Get the login credentials
    username = request.json.get('username')
    password = request.json.get('password')

    # Fetch the user from the database by username
    # and get the stored hashed password
    user = db.session.query(user_table).filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        # Authentication successful
        return jsonify(message="Login successful"), 200
    else:
        # Authentication failed
        return jsonify(message="Invalid username or password"), 401

if __name__ == '__main__':
    app.run(debug=True)
