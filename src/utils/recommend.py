from sklearn.feature_extraction.text import TfidfVectorizer
from src.db import Movies
import os
import joblib
from sklearn.metrics.pairwise import linear_kernel
from bson import ObjectId

async def init_tfidf_vectorizer():
    """
    Initializes the TfidfVectorizer.
    """
    if os.path.exists('tfidf_vectorizer.pkl'):
        tfidf_vectorizer, movie_ids = joblib.load('tfidf_vectorizer.pkl')
        return tfidf_vectorizer, movie_ids
    all_movie_data = []
    movie_ids = []
    movies = await Movies.find().to_list(25000)
    for movie in movies:
        movie_id = movie['_id']
        movie_ids.append(movie_id)
        movie_cast = " "
        if "cast" in movie:
            for cast in movie["cast"]:
                movie_cast+= (' ' + cast)

        movie_directors = " "
        if "directors" in movie:
            for director in movie["directors"]:
                movie_directors+= (' ' + director)

        movie_genres = " "
        if "genres" in movie:
            for genre in movie["genres"]:
                movie_genres+= (' ' + genre)
        
        movie_countries = " "
        if "countries" in movie:
            for country in movie["countries"]:
                movie_countries+= (' ' + country)
                
        movie_plot = movie.get('plot', "")
        all_movie_data.append(movie['title'] + ' ' + movie_genres*2 + movie_cast*2 + movie_directors*2 + movie_countries*2 + ' ' + movie_plot)
    
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(all_movie_data)

    joblib.dump((tfidf_vectorizer, movie_ids), 'tfidf_vectorizer.pkl')
    return tfidf_vectorizer, tfidf_matrix, movie_ids


def user_clicked_movies(user_clicked_movies):
    """
    Transforms user-clicked movies into TF-IDF vectors using the initialized TF-IDF vectorizer.
    """

    user_clicked_data = []
    for movie in user_clicked_movies:
        movie_cast = " "
        if "cast" in movie:
            for cast in movie["cast"]:
                movie_cast+= (' ' + cast)

        movie_directors = " "
        if "directors" in movie:
            for director in movie["directors"]:
                movie_directors+= (' ' + director)

        movie_genres = " "
        if "genres" in movie:
            for genre in movie["genres"]:
                movie_genres+= (' ' + genre)
        
        movie_countries = " "
        if "countries" in movie:
            for country in movie["countries"]:
                movie_countries+= (' ' + country)
                
        movie_plot = movie.get('plot', "")
        user_clicked_data.append(movie['title'] + ' ' + movie_genres*2 + movie_cast*2 + movie_directors*2 + movie_countries*2 + ' ' + movie_plot)
    
    return user_clicked_data

async def get_recommendations(user_clicked_data, top_n=10):
    print("Getting recommendations")
    user_data = []
    for id in user_clicked_data:
        movie = await Movies.find_one({"_id": ObjectId(id)})
        user_data.append(movie)
    tfidf_vectorizer, all_movies_matrix, movie_ids = await init_tfidf_vectorizer()

    modified_user_data = user_clicked_movies(user_data)
    user_clicked_matrix = all_movies_matrix.transform(modified_user_data)
    cosine_similarities = linear_kernel(user_clicked_matrix, all_movies_matrix)
    indices = cosine_similarities.argsort()[0][::-1][:top_n]
    recommended_movies = []
    for index in indices:
        id = movie_ids[index]
        movie = await Movies.find_one({"_id": id})
        movie['_id'] = str(movie['_id'])
        recommended_movies.append(movie)
    return recommended_movies



