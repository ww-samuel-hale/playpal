from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import text
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
import requests
import json
from models import User, db
from igdb.wrapper import IGDBWrapper

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

db.init_app(app)

bcrypt = Bcrypt(app)

# Send a POST request to https://id.twitch.tv/oauth2/token providing it the CLIENT ID and CLIENT SECRET
auth = requests.post(
    'https://id.twitch.tv/oauth2/token',
    params={
        'client_id': os.getenv('IGDB_CLIENT_ID'),
        'client_secret': os.getenv('IGDB_CLIENT_SECRET'),
        'grant_type': 'client_credentials'
    })

# Get the access token from the response
access_token = auth.json()['access_token']

# Authenticate with the IGDB API
wrapper = IGDBWrapper(os.getenv('IGDB_CLIENT_ID'), access_token)

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

    # Check if the username or email already exists in the database
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify(message="Username already exists"), 409
    
    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    # Create a new user
    new_user = User(username=username, password=hashed_password, email=email)
    
    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(message="User registered successfully"), 200

@app.route('/api/login', methods=['POST'])
def login():
    # Get the login credentials
    username = request.json.get('username')
    password = request.json.get('password')

    # Fetch the user from the database by username
    # and get the stored hashed password
    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        # Authentication successful
        return jsonify(message="Login successful"), 200
    else:
        # Authentication failed
        return jsonify(message="Invalid username or password"), 401
    
### IGDB API ENDPOINTS ###
# Get Games
@app.route('/api/games', methods=['GET'])
def get_games():
    games_array = wrapper.api_request(
            'games',
            'fields id, name; offset 0; where platforms=48;'
          )
    
    games = json.loads(games_array)
    
    return jsonify(games), 200


# Generate game recommendation card
@app.route('/api/recommendation', methods=['GET'])
def get_recommendation():
    recommendation_array = wrapper.api_request(
            'games',
            'fields id, name, cover, genres, platforms, rating, summary; where rating > 80; limit 10;'
          )
    
    recommendations = json.loads(recommendation_array)

    for recommendation in recommendations:
        # Round off the rating to a whole number
        recommendation['rating'] = round(recommendation['rating'])

        game_cover_array = wrapper.api_request(
            'artworks',
            'fields url; where game = ' + str(recommendation['id']) + '; limit 1;'
        )

        game_cover = json.loads(game_cover_array)

        # modify recommendation to include cover url
        if len(game_cover) > 0:
            recommendation['cover'] = game_cover[0]['url']
        else:
            recommendation['cover'] = '../FrontEnd/public/logo192.png'

        # Convert genres array from genre id's to genre names
        genres_array = wrapper.api_request(
            'genres',
            'fields name; where id = (' + ', '.join(str(genre_id) for genre_id in recommendation['genres']) + ');'
        )

        genres = json.loads(genres_array)

        recommendation['genres'] = [genre['name'] for genre in genres]

        # Modify platforms array from platform id's to platform names
        platforms_array = wrapper.api_request(
            'platforms',
            'fields name; where id = (' + ', '.join(str(platform_id) for platform_id in recommendation['platforms']) + ');'
        )

        platforms = json.loads(platforms_array)

        recommendation['platforms'] = [platform['name'] for platform in platforms]
    
    return jsonify(recommendations), 200    
    

if __name__ == '__main__':
    app.run(debug=True)
