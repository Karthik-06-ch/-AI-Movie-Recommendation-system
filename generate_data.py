import pandas as pd
import random
import os

def generate_movie_data():
    movies = [
        {"title": "Inception", "genres": "Action, Sci-Fi, Thriller", "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.", "cast": "Leonardo DiCaprio, Joseph Gordon-Levitt", "rating": 8.8, "mood": "Excited", "poster": "https://image.tmdb.org/t/p/w500/oYuLEt3zVCKq57qu2F8dT7NIa6f.jpg", "imdb_url": "https://www.imdb.com/title/tt1375666/"},
        {"title": "The Dark Knight", "genres": "Action, Crime, Drama", "description": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.", "cast": "Christian Bale, Heath Ledger", "rating": 9.0, "mood": "Excited", "poster": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg", "imdb_url": "https://www.imdb.com/title/tt0468569/"},
        {"title": "The Matrix", "genres": "Action, Sci-Fi", "description": "When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth--the life he knows is the elaborate deception of an evil cyber-intelligence.", "cast": "Keanu Reeves, Laurence Fishburne", "rating": 8.7, "mood": "Motivated", "poster": "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg", "imdb_url": "https://www.imdb.com/title/tt0133093/"},
        {"title": "Avengers: Endgame", "genres": "Action, Adventure, Drama", "description": "After the devastating events of Infinity War, the Avengers assemble once more in order to reverse Thanos' actions and restore balance to the universe.", "cast": "Robert Downey Jr., Chris Evans", "rating": 8.4, "mood": "Excited", "poster": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg", "imdb_url": "https://www.imdb.com/title/tt4154796/"},
        {"title": "Fight Club", "genres": "Drama", "description": "An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into much more.", "cast": "Brad Pitt, Edward Norton", "rating": 8.8, "mood": "Motivated, Excited", "poster": "https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg", "imdb_url": "https://www.imdb.com/title/tt0137523/"},
        {"title": "Forrest Gump", "genres": "Drama, Romance", "description": "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75.", "cast": "Tom Hanks, Robin Wright", "rating": 8.8, "mood": "Happy, Relaxed", "poster": "https://image.tmdb.org/t/p/w500/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg", "imdb_url": "https://www.imdb.com/title/tt0109830/"},
        {"title": "The Shawshank Redemption", "genres": "Drama", "description": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.", "cast": "Tim Robbins, Morgan Freeman", "rating": 9.3, "mood": "Motivated, Relaxed", "poster": "https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg", "imdb_url": "https://www.imdb.com/title/tt0111161/"},
        {"title": "Titanic", "genres": "Drama, Romance", "description": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.", "cast": "Leonardo DiCaprio, Kate Winslet", "rating": 7.9, "mood": "Sad, Romance", "poster": "https://image.tmdb.org/t/p/w500/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg", "imdb_url": "https://www.imdb.com/title/tt0120338/"},
        {"title": "Spider-Man: Into the Spider-Verse", "genres": "Animation, Action, Adventure", "description": "Teen Miles Morales becomes the Spider-Man of his universe, and must join with five spider-powered individuals from other dimensions to stop a threat for all realities.", "cast": "Shameik Moore, Jake Johnson", "rating": 8.4, "mood": "Happy, Excited", "poster": "https://image.tmdb.org/t/p/w500/iiZZdoQBEYBv6id8su7ImL0oCbD.jpg", "imdb_url": "https://www.imdb.com/title/tt4633694/"},
        {"title": "Parasite", "genres": "Comedy, Drama, Thriller", "description": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.", "cast": "Song Kang-ho, Lee Sun-kyun", "rating": 8.5, "mood": "Excited", "poster": "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg", "imdb_url": "https://www.imdb.com/title/tt6751668/"},
        {"title": "Gladiator", "genres": "Action, Adventure, Drama", "description": "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.", "cast": "Russell Crowe, Joaquin Phoenix", "rating": 8.5, "mood": "Motivated", "poster": "https://image.tmdb.org/t/p/w500/ty8TGRuvJLPUmAR1H1nRIsgwvim.jpg", "imdb_url": "https://www.imdb.com/title/tt0172495/"},
        {"title": "The Godfather", "genres": "Crime, Drama", "description": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.", "cast": "Marlon Brando, Al Pacino", "rating": 9.2, "mood": "Relaxed", "poster": "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg", "imdb_url": "https://www.imdb.com/title/tt0068646/"}
    ]
    
    df = pd.DataFrame(movies)
    df.insert(0, 'movie_id', range(1, 1 + len(df)))
    
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/movies.csv', index=False)
    
    # Generate some user interactions
    users = range(1, 11) # 10 users
    interactions = []
    for u in users:
        # each user watches 3 to len(df) movies
        num_watched = random.randint(3, len(df))
        watched = random.sample(list(df['movie_id']), num_watched)
        for w in watched:
            interactions.append({
                "user_id": u,
                "movie_id": w,
                "rating": random.randint(1, 5)
            })
    
    df_interact = pd.DataFrame(interactions)
    df_interact.to_csv('data/ratings.csv', index=False)

if __name__ == "__main__":
    generate_movie_data()
    print("Data generated successfully.")
