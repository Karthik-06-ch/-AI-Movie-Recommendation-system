from flask import Flask, render_template, request, jsonify
from ml.recommender import RecommenderSystem
import os

app = Flask(__name__)

# Initialize Recommender System
recommender = RecommenderSystem()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/trending', methods=['GET'])
def get_trending():
    movies = recommender.get_trending_movies(15)
    return jsonify(movies)

@app.route('/api/mood', methods=['GET'])
def get_mood_recommendations():
    mood = request.args.get('mood', 'Happy')
    movies = recommender.get_movies_by_mood(mood, 15)
    return jsonify(movies)

@app.route('/api/recommend/movie', methods=['GET'])
def recommend_by_movie():
    title = request.args.get('title')
    if not title:
        return jsonify({"error": "No title provided"}), 400
    movies = recommender.get_recommendations_by_movie(title, 10)
    return jsonify(movies)

@app.route('/api/recommend/user', methods=['GET'])
def recommend_for_user():
    user_id = int(request.args.get('user_id', 1))
    movies = recommender.get_user_recommendations(user_id, 15)
    return jsonify(movies)

@app.route('/api/recommend/preferences', methods=['POST'])
def recommend_by_preferences():
    data = request.json
    genres = data.get('genres', [])
    if not genres:
        return jsonify([])
    movies = recommender.get_recommendations_by_preferences(genres, 15)
    return jsonify(movies)

@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if not query:
        return jsonify([])
    movies = recommender.search_movies(query)
    return jsonify(movies)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
