from sentence_transformers import SentenceTransformer
import torch
from src.db import Embedded_movies_new
from src import schemas


# embedder = SentenceTransformer('bert-base-nli-mean-tokens')
embedder = SentenceTransformer('all-MiniLM-L6-v2')

corpus = [
    "A man is eating food.",
    "A man is eating a piece of bread.",
    "The girl is carrying a baby.",
    "A man is riding a horse.",
    "A woman is playing violin.",
    "Two men pushed carts through the woods.",
    "A man is riding a white horse on an enclosed ground.",
    "A monkey is playing drums.",
    "A cheetah is running behind its prey.",
]

# create vector embeddings and print their shapes

def get_embedding(corpus):
    embedding = embedder.encode(corpus, convert_to_tensor=True)
    return embedding, embedding.shape

# embed = get_embedding(corpus=corpus)
# print(embed)

async def embed_movie(movie: dict):
    movie_embedding = await Embedded_movies_new.find_one({"_id": movie['_id']})
    if movie_embedding:
        return
    else:
        embedding, _ = get_embedding([movie['plot']])
        # convert tensor to list
        embedding = embedding.tolist()[0]
        movie_embedding = {
            "_id": movie["_id"],
            "embedding": embedding
        }
        await Embedded_movies_new.insert_one(movie_embedding)
        return movie_embedding

