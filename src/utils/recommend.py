from sklearn.feature_extraction.text import TfidfVectorizer
from src.db import Movies
import os
import joblib
from sklearn.metrics.pairwise import linear_kernel
from bson import ObjectId
# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.stem import WordNetLemmatizer
import string

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

# Initialize WordNet Lemmatizer
# lemmatizer = WordNetLemmatizer()

# Custom tokenizer function with lemmatization
# def lemmatize_text(text):
#     """
#     Lemmatizes the text.
#     """
#     tokens = word_tokenize(text)
#     tokens = [token for token in tokens if token not in string.punctuation]
#     tokens = [lemmatizer.lemmatize(token) for token in tokens]
#     return tokens

# # Custom preprocessor function to lower case the text
# def preprocess_text(text):
#     """
#     Preprocesses the text.
#     """
#     text = text.lower()
#     return text

# # Get English stopwords
# stop_words = set(stopwords.words('english'))
# stop_words = list(stop_words)

async def init_tfidf_vectorizer():
    """
    Initializes the TfidfVectorizer.
    """
    if os.path.exists('tfidf_vectorizer.pkl'):
        tfidf_vectorizer, movie_ids, all_docs_tfidf = joblib.load('tfidf_vectorizer.pkl')
        return tfidf_vectorizer, movie_ids, all_docs_tfidf
    all_movie_data = []
    movie_ids = []
    movies = await Movies.find().to_list(25000)
    index = 0
    for movie in movies:
        movie_id = movie['_id']
        movie_ids.append({
            'index': index,
            '_id': movie_id
        })
        index+=1
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
                
        # movie_plot = " "
        # if "plot" in movie:
        #     movie_plot = movie.get('plot', "")
        
        all_movie_data.append(movie['title'] + ' ' + movie_genres*5 + movie_cast*2 + movie_directors*2 + movie_countries*2)
    
    # tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words, preprocessor=preprocess_text, tokenizer=lemmatize_text, max_features=2000, token_pattern=None)
    tfidf_vectorizer = TfidfVectorizer()
    all_docs_tfidf = tfidf_vectorizer.fit_transform(all_movie_data)

    joblib.dump((tfidf_vectorizer, movie_ids, all_docs_tfidf), 'tfidf_vectorizer.pkl')
    return tfidf_vectorizer, movie_ids, all_docs_tfidf


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
                
        # movie_plot = movie.get('plot', "")
        user_clicked_data.append(movie['title'] + ' ' + movie_genres*5 + movie_cast*2 + movie_directors*2 + movie_countries*2)
    
    return user_clicked_data


async def get_recommendations(user_clicked_data, top_n=10):
    print("Getting recommendations")
    user_data = []
    for id in user_clicked_data:
        movie = await Movies.find_one({"_id": ObjectId(id)})
        user_data.append(movie)
    modified_user_data = user_clicked_movies(user_data)
    tfidf_vectorizer, movie_ids, all_docs_tfidf = await init_tfidf_vectorizer()

    user_clicked_tfidf = tfidf_vectorizer.transform(modified_user_data)
    cosine_similarities = linear_kernel(user_clicked_tfidf, all_docs_tfidf)
    similar_indices = cosine_similarities.argsort(axis=1)[:, ::-1].flatten()
    recommended_movies = []
    clicked_movie_ids = set(user_clicked_data)
    for i in similar_indices:
        movie_id = movie_ids[i]['_id']
        if str(movie_id) not in clicked_movie_ids:
            movie = await Movies.find_one({"_id": ObjectId(movie_id)})
            movie['_id'] = str(movie['_id'])
            recommended_movies.append({
                '_id': movie['_id'],
                'title': movie['title'],
                'poster_path': movie.get('poster_path', ""),
                'year': movie['year'],
                'imdb': movie['imdb'],
                'backdrop_path': movie.get('backdrop_path', ""),
                'genres': movie['genres'],
                'plot': movie.get('plot', ""),
                'year': movie['year'],
                'poster': movie.get('poster', ""),
            })
            # print(cosine_similarities[0][i])
        if len(recommended_movies) >= top_n:
            break
    return recommended_movies




