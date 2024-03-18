from sentence_transformers import SentenceTransformer
from src.db import Embedded_movies

embedder = SentenceTransformer('bert-base-nli-mean-tokens')

def get_embedding(corpus):
    embedding = embedder.encode(corpus, convert_to_tensor=True)
    return embedding, embedding.shape

async def embed_movie(movie):
    movie_embedding = await Embedded_movies.find_one({"_id": movie['_id']})
    if movie_embedding:
        return
    else:
        embedding, _ = get_embedding([movie['plot']])
        embedding = embedding.tolist()[0]
        embeddings_bson = [float(value) for value in embedding]
        movie['embedding'] = embeddings_bson
        await Embedded_movies.insert_one(movie_embedding)
        return movie_embedding

