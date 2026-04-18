import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from rapidfuzz import process

# SAMPLE DATASET (Real Movies)
movies = pd.DataFrame({
    'movie_id': [1,2,3,4,5,6,7,8],
    'title': [
        'Titanic',
        'The Notebook',
        'Inception',
        'Interstellar',
        'The Dark Knight',
        'Joker',
        'Avengers: Endgame',
        'La La Land'
    ],
    'genre': [
        'Romance Drama',
        'Romance Drama',
        'Sci-Fi Action',
        'Sci-Fi Drama',
        'Action Crime',
        'Drama Thriller',
        'Action Sci-Fi',
        'Romance Musical'
    ]
})

# USER RATINGS 
ratings = pd.DataFrame({
    'user_id': [1,1,2,2,3,3,4,4],
    'movie_id': [1,3,2,4,1,5,6,7],
    'rating': [5,4,5,4,4,5,4,5]
})
# TF-IDF 
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(movies['genre'])

content_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

#Collaborative Filtering
user_movie_matrix = ratings.pivot(index='user_id', columns='movie_id', values='rating').fillna(0)
user_similarity = cosine_similarity(user_movie_matrix)


def predict_rating(user_id, movie_id):
    if movie_id not in user_movie_matrix.columns:
        return 0
    
    sim_scores = user_similarity[user_id-1]
    movie_ratings = user_movie_matrix[movie_id]
    
    pred = (sim_scores @ movie_ratings) / (sum(sim_scores) + 1e-5)
    return round(pred, 2)


def get_movie_index(movie_name):
    movie_list = movies['title'].tolist()
    
    match, score, _ = process.extractOne(movie_name, movie_list)
    
    if score < 60:
        print("Movie not found properly. Try again.")
        exit()
    
    return movies[movies['title'] == match].index[0]


def recommend_movies(user_id, movie_name, top_n=5):
    
    movie_index = get_movie_index(movie_name)
    
    # Content similarity scores
    sim_scores = list(enumerate(content_sim[movie_index]))
    
    # Sort by similarity
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:]
    
    recommendations = []
    
    for i, score in sim_scores:
        movie_id = movies.iloc[i]['movie_id']
        
        # Predict rating
        pred_rating = predict_rating(user_id, movie_id)
        
        # Hybrid Score 
        final_score = (0.6 * score) + (0.4 * pred_rating / 5)
        
        recommendations.append((
            movies.iloc[i]['title'],
            movies.iloc[i]['genre'],
            round(pred_rating,2),
            round(final_score,2)
        ))
    
    # Convert to DataFrame
    rec_df = pd.DataFrame(recommendations, columns=['title','genre','predicted_rating','score'])
    
    return rec_df.sort_values(by='score', ascending=False).head(top_n)

#input
user_id = int(input("Enter User ID (1-4): "))
movie_name = input("Enter your favorite movie: ")
top_n = int(input("How many recommendations do you want (Top N): "))

#output
result = recommend_movies(user_id, movie_name, top_n)

print("\nTop", top_n, "Recommended Movies:\n")
print(result)