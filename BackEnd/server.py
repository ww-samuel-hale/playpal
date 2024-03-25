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
import time

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

### FUNCTIONS ###
# Example Object
# filters = {
#     ageRatings: ['E']
#     gameEngines: ['Unreal']
#     gameModes: ['Battle Royale']
#     genres: (2) ['Arcade', 'Card & Board Game']
#     languages: ['English']
#     platforms: ['PC (Microsoft Windows)']
#     playerPerspectives: ['First person']
#     releaseDate: (2) ['After 1990', 'Before July']
#     themes: ['Action']
# }
def construct_query(filters):
    query_parts = []

    if 'genres' in filters and filters['genres']:
        genres_query = ','.join([f'"{genre}"' for genre in filters['genres']])
        query_parts.append(f"genres.name = ({genres_query})")

    if 'platforms' in filters and filters['platforms']:
        platforms_query = ','.join([f'"{platform}"' for platform in filters['platforms']])
        query_parts.append(f"platforms.name = ({platforms_query})")

    if 'themes' in filters and filters['themes']:
        themes_query = ','.join([f'"{theme}"' for theme in filters['themes']])
        query_parts.append(f"themes.name = ({themes_query})")
    
    if 'gameModes' in filters and filters['gameModes']:
        gameModes_query = ','.join([f'"{gameMode}"' for gameMode in filters['gameModes']])
        query_parts.append(f"game_modes.name = ({gameModes_query})")
        
    if 'playerPerspectives' in filters and filters['playerPerspectives']:
        playerPerspectives_query = ','.join([f'"{playerPerspective}"' for playerPerspective in filters['playerPerspectives']])
        query_parts.append(f"player_perspectives.name = ({playerPerspectives_query})")
        
    if 'gameEngines' in filters and filters['gameEngines']:
        gameEngines_query = ','.join([f'"{gameEngine}"' for gameEngine in filters['gameEngines']])
        query_parts.append(f"game_engines.name = ({gameEngines_query})")
        
    if 'languages' in filters and filters['languages']:
        languages_query = ','.join([f'"{language}"' for language in filters['languages']])
        query_parts.append(f"language_supports.language.name = ({languages_query})")
        
    if 'ageRatings' in filters and filters['ageRatings']:
        ageRatings_query = ','.join([f'{ageRating}' for ageRating in filters['ageRatings']])
        query_parts.append(f"age_ratings.rating = ({ageRatings_query})")
        
    if 'releaseDate' in filters and filters['releaseDate']:
        for releaseDate in filters['releaseDate']:
            operator = ">" if releaseDate.startswith("After") else "<"
            value = releaseDate[6:] if releaseDate.startswith("After") else releaseDate[7:]
            if value.isdigit():  # it's a year
                query_parts.append(f"release_dates.y {operator} {value}")
            elif value in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']:  # it's a month
                month_number = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'].index(value) + 1
                query_parts.append(f"release_dates.m {operator} {month_number}")
                
    if 'rating' in filters and filters['rating']:
        query_parts.append(f"rating {filters['rating']}")

    # Join all parts of the query
    if query_parts:
        where_clause = 'where ' + ' & '.join(query_parts) + ';'
    else:
        where_clause = ''

    # Construct the full query
    query = f"fields id, name, cover.url, genres.name, platforms.name, rating, summary; {where_clause} limit 100;"
    return query

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
        return jsonify(message="Login successful", username=user.username), 200
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
@app.route('/api/recommendation', methods=['POST'])
def get_recommendation():
    filters = request.json
    query = construct_query(filters)
    recommendation_array = wrapper.api_request('games', query)
    
    recommendations = json.loads(recommendation_array)

    for recommendation in recommendations:
        # Round off the rating to a whole number
        recommendation['rating'] = round(recommendation['rating'])

        # Modify recommendation to include cover url
        if 'cover' in recommendation and 'url' in recommendation['cover']:
            recommendation['cover'] = recommendation['cover']['url']
        else:
            recommendation['cover'] = '../FrontEnd/public/logo192.png'

        # Check if genres exist and extract their names
        if 'genres' in recommendation:
            recommendation['genres'] = [genre['name'] for genre in recommendation['genres']]
        else:
            recommendation['genres'] = []

        # Check if platforms exist and extract their names
        if 'platforms' in recommendation:
            recommendation['platforms'] = [platform['name'] for platform in recommendation['platforms']]
        else:
            recommendation['platforms'] = []
            
        if 'summary' not in recommendation:
            recommendation['summary'] = 'No summary available.'
    
    return jsonify(recommendations), 200    



if __name__ == '__main__':
    app.run(debug=True)
