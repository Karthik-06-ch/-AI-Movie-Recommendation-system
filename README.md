# AI Movie Recommendation System (AIFlix)

AIFlix is a modern, AI-powered web application that provides personalized movie recommendations based on user preferences, genres, ratings, watch history, and emotional mood. The UI is designed to mimic a high-end streaming service like Netflix, featuring smooth animations, horizontal scrolling carousels, dark-theme aesthetics, and dynamic content injection.

## 🚀 Features

- **Personalized Onboarding (Cold Start):** When a new user logs in, they select their favorite genres. The system uses Natural Language Processing (NLP) to build a synthetic user profile and recommends mathematically similar movies.
- **Machine Learning Engine:** Powered by `scikit-learn`, the system merges movie titles, genres, descriptions, and cast into textual "Feature Strings" and uses **TF-IDF Vectorization** alongside **Cosine Similarity** to calculate algorithmic Match Percentages.
- **Interactive UI:** 
  - Dynamic **"Watch on IMDb"** buttons redirect users to official movie pages.
  - A functional **Watchlist ("My List")** stored in the browser's local storage.
  - Interactive mood pills (Happy, Excited, Relaxed, Motivated, Sad) instantly filter movie results.
  - Dynamic Toast notifications for interactive feedback (Thumbs Up/Down, Added to list).
- **Synthetic Data Generator:** A custom python script (`generate_data.py`) dynamically creates the movie database utilizing real movie data and official TMDB poster images.

## 💻 Tech Stack

- **Backend:** Python, Flask
- **Machine Learning:** Pandas, NumPy, Scikit-Learn
- **Frontend:** HTML5, CSS3, Vanilla JavaScript

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Karthik-06-ch/-AI-Movie-Recommendation-system.git
   cd -AI-Movie-Recommendation-system
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate the Movie Data:**
   Run the data generator to create the `movies.csv` and `ratings.csv` datasets.
   ```bash
   python generate_data.py
   ```

4. **Start the Flask Server:**
   ```bash
   python app.py
   ```

5. **View the Application:**
   Open your browser and navigate to `http://localhost:5000`

## 📁 Project Structure

* `app.py`: The main Flask server application handling API routes.
* `generate_data.py`: Script to generate/reset the movie datasets and user interactions.
* `ml/recommender.py`: The machine learning core that computes TF-IDF matrices and Cosine Similarities.
* `templates/index.html`: The fully responsive Netflix-style frontend markup.
* `static/css/style.css`: Custom CSS focused on modern aesthetics and micro-animations.
* `static/js/main.js`: Client-side logic for DOM manipulation, local storage, and API fetching.
