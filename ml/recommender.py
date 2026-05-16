import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

class RecommenderSystem:
    def __init__(self, data_path='data'):
        self.movies_df = pd.read_csv(os.path.join(data_path, 'movies.csv'))
        self.ratings_df = pd.read_csv(os.path.join(data_path, 'ratings.csv'))
        self.cosine_sim = None
        self._build_model()
        
    def _build_model(self):
        # Combine features for content-based filtering
        # We'll use genres, description, and cast
        self.movies_df['combined_features'] = self.movies_df['genres'] + " " + \
                                              self.movies_df['description'] + " " + \
                                              self.movies_df['cast']
        
        # Fill missing values
        self.movies_df['combined_features'] = self.movies_df['combined_features'].fillna('')
        
        # Create TF-IDF matrix
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.tfidf.fit_transform(self.movies_df['combined_features'])
        
        # Compute Cosine Similarity
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
        
    def get_movie_by_id(self, movie_id):
        movie = self.movies_df[self.movies_df['movie_id'] == movie_id]
        if not movie.empty:
            return movie.iloc[0].to_dict()
        return None

    def get_trending_movies(self, top_n=10):
        # Trending based on rating
        trending = self.movies_df.sort_values(by='rating', ascending=False).head(top_n)
        return trending.to_dict('records')

    def get_movies_by_mood(self, mood, top_n=10):
        # Filter movies where mood contains the requested mood
        mood_movies = self.movies_df[self.movies_df['mood'].str.contains(mood, case=False, na=False)]
        return mood_movies.head(top_n).to_dict('records')

    def get_recommendations_by_movie(self, movie_title, top_n=5):
        # Find index of the movie
        try:
            idx = self.movies_df[self.movies_df['title'].str.lower() == movie_title.lower()].index[0]
        except IndexError:
            return []
            
        # Get similarity scores
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        
        # Sort by similarity
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top n (excluding the movie itself)
        sim_scores = sim_scores[1:top_n+1]
        
        movie_indices = [i[0] for i in sim_scores]
        recommendations = self.movies_df.iloc[movie_indices].copy()
        
        # Add similarity score for confidence
        recommendations['confidence'] = [round(sim_scores[i][1] * 100, 1) for i in range(len(sim_scores))]
        
        return recommendations.to_dict('records')
        
    def search_movies(self, query):
        mask = self.movies_df['title'].str.contains(query, case=False, na=False) | \
               self.movies_df['genres'].str.contains(query, case=False, na=False) | \
               self.movies_df['cast'].str.contains(query, case=False, na=False)
        return self.movies_df[mask].to_dict('records')

    def get_user_recommendations(self, user_id, top_n=10):
        # Simple collaborative filtering baseline or fallback to content-based on highest rated movie
        user_ratings = self.ratings_df[self.ratings_df['user_id'] == user_id]
        if user_ratings.empty:
            return self.get_trending_movies(top_n)
            
        # Get user's highest rated movie
        top_movie_id = user_ratings.sort_values(by='rating', ascending=False).iloc[0]['movie_id']
        top_movie_title = self.get_movie_by_id(top_movie_id)['title']
        
        return self.get_recommendations_by_movie(top_movie_title, top_n)

    def get_recommendations_by_preferences(self, preferences, top_n=10):
        # Create a synthetic user profile document based on their preferences
        user_profile = " ".join(preferences)
        
        # Transform the user profile using the existing TF-IDF vectorizer
        user_tfidf = self.tfidf.transform([user_profile])
        
        # Calculate cosine similarity between user profile and all movies
        sim_scores = cosine_similarity(user_tfidf, self.tfidf_matrix).flatten()
        
        # Sort the movies based on the similarity scores
        sim_scores_indices = sim_scores.argsort()[::-1]
        
        # Get top n
        top_indices = sim_scores_indices[:top_n]
        
        recommendations = self.movies_df.iloc[top_indices].copy()
        recommendations['confidence'] = [round(sim_scores[i] * 100, 1) for i in top_indices]
        
        return recommendations.to_dict('records')
