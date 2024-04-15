from flask import Flask, jsonify, request, current_app
from flask_cors import CORS
from sqlalchemy import text
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
import requests
import json
from models import User, UserFilter, FilterCategory, Game, UserGameInteraction, db
from igdb.wrapper import IGDBWrapper
import time
from sqlalchemy import and_
import random
from collections import defaultdict
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np
from collections.abc import Iterable

recommendation_cache = defaultdict(set)

all_genres = ["Point-and-click",
        "Fighting",
        "Shooter",
        "Music",
        "Platform",
        "Puzzle",
        "Racing",
        "Real Time Strategy (RTS)",
        "Role-playing (RPG)",
        "Simulator",
        "Sport",
        "Strategy",
        "Turn-based strategy (TBS)",
        "Tactical",
        "Hack and slash/Beat 'em up",
        "Quiz/Trivia",
        "Pinball",
        "Adventure",
        "Indie",
        "Arcade",
        "Visual Novel",
        "Card & Board Game",
        "MOBA"]
all_themes = ["Action",
        "Fantasy",
        "Science fiction",
        "Horror",
        "Thriller",
        "Survival",
        "Historical",
        "Stealth",
        "Comedy",
        "Business",
        "Drama",
        "Non-fiction",
        "Sandbox",
        "Educational",
        "Kids",
        "Open world",
        "Warfare",
        "Party",
        "4X (explore, expand, exploit, and exterminate)",
        "Erotic",
        "Mystery",
        "Romance"]
all_game_modes = [ 
        "Single player",
        "Multiplayer",
        "Co-operative",
        "Split screen",
        "Massively Multiplayer Online (MMO)",
        "Battle Royale"]

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
        where_clause = ' & '.join(query_parts)
        where_clause = ' & ' + where_clause if where_clause else ''
    else:
        where_clause = ''

    # Construct the full query
    query = f"fields id, name, cover.url, genres.name, platforms.name, rating, summary, release_dates.y, game_modes.name, themes.name; where rating != null & summary != null & genres != null & platforms != null {where_clause} ; limit 500;"
    return query

def update_recommendation_cache(user_id, recommendations):
    """Update the cache with new recommendations."""
    # Convert the set to a list to have a predictable order for removal
    cached_list = list(recommendation_cache[user_id])

    # Add new game IDs to the cache
    new_ids = [game['id'] for game in recommendations]
    cached_list.extend(new_ids)

    # If the cache exceeds 200 items, remove the oldest 100 items
    if len(cached_list) > 200:
        cached_list = cached_list[100:]

    # Convert the list back to a set for fast lookup and update the cache
    recommendation_cache[user_id] = set(cached_list)


def adjust_query_for_exclusions(original_query, excluded_game_ids):
    """
    Adjust the IGDB API query to exclude specific game IDs.

    :param original_query: The original query string
    :param excluded_game_ids: A set or list of game IDs to exclude
    :return: The adjusted query string
    """
    # Split the query to insert the exclusions before '; limit 500;'
    query_parts = original_query.split('; limit 500;')
    
    # Construct the exclusion part of the query
    exclusions = ' & '.join([f'id != {game_id}' for game_id in excluded_game_ids])
    
    # Reconstruct the query with exclusions
    adjusted_query = f"{query_parts[0]} & {exclusions} ; limit 500;"

    return adjusted_query

def prepare_data(games):
    """Prepares data by filling missing values and combining features."""
    prepared_games = {}
    if isinstance(games, dict):
        games = [games]
    for game in games:
        prepared_game = {
            'themes': game.themes.strip('{}').replace('"', '').split(',') if game.themes != '' else ['No Themes'],
            'genre': game.genre.strip('{}').replace('"', '').split(',') if game.genre != '' else ['No Genre'],
            'game_modes': game.game_modes.strip('{}').replace('"', '').split(',') if game.game_modes != '' else ['No Game Modes'],
            'release_date': game.release_date if game.release_date != '' else 'No Release Date',
            'rating': game.rating if game.rating else 0
        }
        prepared_game['combined_features'] = f"{prepared_game['genre']} {prepared_game['themes']} {prepared_game['game_modes']} {prepared_game['release_date']} {prepared_game['rating']}"
        prepared_games[game.gameid] = prepared_game
    return prepared_games

def train_model(tfidf_matrix):
    """Calculates the cosine similarity matrix."""
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim

def get_recommendations(game_id, games, cosine_sim):
    """Generates game recommendations for a given game ID."""
    idx = games.index[games['gameid'] == game_id].tolist()[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    game_indices = [i[0] for i in sim_scores]
    return games['title'].iloc[game_indices]

def create_user_profile_vector(user_interactions, game_features, mlb_genre, mlb_theme, mlb_game_modes):
    # Initialize profile vectors for each feature type
    profile_genre = np.zeros(len(mlb_genre.classes_))
    profile_theme = np.zeros(len(mlb_theme.classes_))
    profile_game_modes = np.zeros(len(mlb_game_modes.classes_))
    
    # Loop through each user interaction
    for interaction in user_interactions:
        game_id = interaction.gameid
        game_data = game_features[game_id]
        
        # Encode each feature type
        genre_vector = mlb_genre.transform([game_data['genre']])
        theme_vector = mlb_theme.transform([game_data['themes']])
        game_modes_vector = mlb_game_modes.transform([game_data['game_modes']])
        
        # Apply interaction weight
        interaction_weight = 1 if interaction.interactiontype == 'like' else -1
        
        # Weight each feature vector by the interaction and game rating
        rating_weight = game_data['rating'] / 100  # Normalize game rating
        total_weight = interaction_weight * rating_weight
        
        # Update the profile vectors
        profile_genre += genre_vector[0] * total_weight
        profile_theme += theme_vector[0] * total_weight
        profile_game_modes += game_modes_vector[0] * total_weight
    
    # Combine the feature vectors into one profile vector and normalize
    profile_vector = np.concatenate([profile_genre, profile_theme, profile_game_modes])
    if np.linalg.norm(profile_vector) > 0:
        profile_vector /= np.linalg.norm(profile_vector)
    
    return profile_vector

def transform_game_features(candidate_games, mlb_genre, mlb_theme, mlb_game_modes):
    # Extract and transform the 'name' attributes for each game's genres, themes, and game modes
    genres = [[genre['name'] for genre in game['genres']] if 'genres' in game else [] for game in candidate_games]
    themes = [[theme['name'] for theme in game['themes']] if 'themes' in game else [] for game in candidate_games]
    game_modes = [[game_mode['name'] for game_mode in game['game_modes']] if 'game_modes' in game else [] for game in candidate_games]

    # Transform the features using the fitted MultiLabelBinarizers
    genre_matrix = mlb_genre.transform(genres)
    theme_matrix = mlb_theme.transform(themes)
    game_modes_matrix = mlb_game_modes.transform(game_modes)

    # Combine the matrices into a single feature matrix for all games
    combined_matrix = np.hstack((genre_matrix, theme_matrix, game_modes_matrix))

    return combined_matrix

    
def cosine_similarity(user_profile, candidate_games_matrix):
    # Calculate the cosine similarity between the user profile and candidate games
    similarity = np.dot(candidate_games_matrix, user_profile.T)
    
    return similarity

def calculate_similarity(user_profile_vector, game_features_matrix):
    similarity_scores = cosine_similarity(user_profile_vector.T, game_features_matrix)
        
    return similarity_scores


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
        current_app.logger.debug("Authentication successful")
        return jsonify(message="Login successful", username=user.username, user_id=user.userid), 200
    else:
        current_app.logger.debug("Authentication failed")
        current_app.logger.debug(f"Expected Hash: {user.password} Provided Password: {password}")
        return jsonify(message="Invalid username or password"), 401
    
### FILTER ENDPOINTS ###
@app.route('/api/user_filters', methods=['POST'])
def get_user_filters():
    # Get the user ID from the request
    user_id = request.json['user_id']
    
    # Get the filters from the database
    user_filters = UserFilter.query.filter_by(user_id=user_id).all()
    
    # Create an empty dictionary to store the filters
    filters = {}
    
    # Loop through the user filters and add them to the dictionary
    for user_filter in user_filters:
        category = FilterCategory.query.filter_by(category_id=user_filter.category_id).first()
        if category.category_name == 'ratings':
            filters[category.category_name] = user_filter.option_value
        else:
            if category.category_name not in filters:
                filters[category.category_name] = []
                filters[category.category_name].append(user_filter.option_value)
    
    return jsonify(filters), 200

@app.route('/api/user_filters', methods=['PUT'])
def update_user_filters():
    # Get the user ID from the request
    user_id = request.json.get('user_id')
    
    # Get the filters from the request
    filters = request.json.get('filters')
    
    # Delete the existing filters for the user
    UserFilter.query.filter_by(user_id=user_id).delete()
    
    # Loop through the filters and add them to the database
    for filter in filters:
        for option in filters[filter]:
            # Get the category ID from the database
            category = FilterCategory.query.filter_by(category_name=filter).first()
            
            # Create a new UserFilter object
            user_filter = UserFilter(
                user_id=user_id,
                category_id=category.category_id,
                option_value=option
            )
            db.session.add(user_filter)
        # Commit the changes to the database
        db.session.commit()
    
    return jsonify(message="Filters updated successfully"), 200

@app.route('/api/query', methods=['PUT'])
def update_query():
    # Get the user ID and query from the request
    user_id = request.json.get('user_id')
    filters = request.json.get('filters')
    
    # Construct the query
    query = construct_query(filters)
    
    # Update the query in the database
    # Find the user from user_id
    user = User.query.filter_by(userid=user_id).first()
    user.game_query = query
    db.session.commit()
    
    return jsonify(message="Query updated successfully"), 200


    
### IGDB API ENDPOINTS ###
# Get Games
@app.route('/api/games', methods=['GET'])
def get_games():
    user_id = request.json.get('user_id')
    
    # Get the user's query from the database
    user = User.query.filter_by(userid=user_id).first()
    query = user.game_query
    games_array = wrapper.api_request(
            'games',
            query
          )
    
    games = json.loads(games_array)
    
    return jsonify(games), 200


# Generate game recommendation card
@app.route('/api/recommendation', methods=['POST'])
def get_recommendation():
    user_id = request.json.get('user_id')
    
    # Get the user's query from the database
    user = User.query.filter_by(userid=user_id).first()
    query = user.game_query
    
    # Get the game IDs from UserGameInteraction for the user
    user_interactions = UserGameInteraction.query.filter_by(userid=user_id).all()
    excluded_game_ids = [interaction.gameid for interaction in user_interactions]
    print(user_interactions)

    game_ids = [interaction.gameid for interaction in user_interactions]
    games = Game.query.filter(Game.gameid.in_(game_ids)).all()  # Fix: Use 'in_' operator to filter games by IDs
    print(games)

    prepared_data = prepare_data(games)
    print(prepared_data)

    mlb_genre = MultiLabelBinarizer()
    mlb_theme = MultiLabelBinarizer()
    mlb_game_modes = MultiLabelBinarizer()
    
    mlb_genre.fit([all_genres])
    mlb_theme.fit([all_themes])
    mlb_game_modes.fit([all_game_modes])
    
    user_profile = create_user_profile_vector(user_interactions, prepared_data, mlb_genre, mlb_theme, mlb_game_modes)
    print(user_profile)
    
    # Adjust the query to exclude games that have already been recommended
    if excluded_game_ids:
        query = adjust_query_for_exclusions(query, excluded_game_ids)
    print(query)
    
    recommendation_array = wrapper.api_request('games', query)
    
    recommendations = json.loads(recommendation_array)
    
    recommendations_features = transform_game_features(recommendations, mlb_genre, mlb_theme, mlb_game_modes)
    
    similarity_scores = calculate_similarity(user_profile, recommendations_features)
    print(similarity_scores)
    
    sorted_indices = np.argsort(similarity_scores)[::-1]
    print(sorted_indices)
    
    top_indices = sorted_indices[:100]
    print(top_indices)
    
    top_games = [recommendations[i] for i in top_indices]
    print(top_games)
        
    # Update the cache with new recommendations
    update_recommendation_cache(user_id, top_games)

    for recommendation in top_games:
        # Round off the rating to a whole number
        if 'rating' in recommendation:
            recommendation['rating'] = round(recommendation['rating'])
        else:
            recommendation['rating'] = 'No rating available'

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
            
        if 'release_dates' in recommendation and 'y' in recommendation['release_dates'][0]:
            recommendation['release_date'] = recommendation['release_dates'][0]['y']
        else:
            recommendation['release_date'] = 'No release date available.'
        
        if 'game_modes' in recommendation:
            recommendation['game_modes'] = [game_mode['name'] for game_mode in recommendation['game_modes']]
        else:
            recommendation['game_modes'] = []
        
        if 'themes' in recommendation:
            recommendation['themes'] = [theme['name'] for theme in recommendation['themes']]
        else:
            recommendation['themes'] = []
    
    return jsonify(top_games), 200

# Handle interaction "Thumbs Up" or "Thumbs Down" for a game recommendation
@app.route('/api/interaction', methods=['POST'])
def handle_interaction():
    user_id = request.json.get('user_id')
    game_id = request.json.get('game_id')
    interaction_type = request.json.get('interaction_type')
    genre = request.json.get('genre')
    rating = request.json.get('rating')
    release_date = request.json.get('release_date')
    game_modes = request.json.get('game_modes')
    themes = request.json.get('themes')
    
    # game_modes and themes will be stored as arrays we need to convert them to strings
    game_modes = ','.join(game_modes)
    themes = ','.join(themes)
    genres = ','.join(genre)
    
    # Enter the game into the Games table if it does not exist 
    # Check if the game already exists in the Games table
    existing_game = Game.query.filter_by(gameid=game_id).first()

    # If the game does not exist, create a new entry in the Games table
    if not existing_game:
        new_game = Game(gameid=game_id, genre=genre, rating=rating, release_date=release_date, game_modes=game_modes, themes=themes)
        db.session.add(new_game)
        db.session.commit()
    
    # Check if a UserGameInteraction already exists for the given gameid and userid
    existing_interaction = UserGameInteraction.query.filter_by(userid=user_id, gameid=game_id).first()
    
    if existing_interaction:
        # Update the interactiontype
        existing_interaction.interactiontype = interaction_type
        db.session.commit()
    else:
        # Create a new UserGameInteraction object
        user_interaction = UserGameInteraction(
            userid=user_id,
            gameid=game_id,
            interactiontype=interaction_type
        )
        
        # Add the new interaction to the database
        db.session.add(user_interaction)
        db.session.commit()
    
    return jsonify(message="Interaction recorded successfully"), 200



if __name__ == '__main__':
    app.run(debug=True)
