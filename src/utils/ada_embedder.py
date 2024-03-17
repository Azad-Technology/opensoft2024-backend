from transformers import GPT2TokenizerFast
from sentence_transformers import SentenceTransformer
from src.db import Embedded_movies2
from src import schemas

embedder = SentenceTransformer('bert-base-nli-mean-tokens')
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


def get_embedding(corpus):
    embedding = embedder.encode(corpus, convert_to_tensor=True)
    return embedding, embedding.shape

async def embed_movie(movie):
    movie_embedding = await Embedded_movies2.find_one({"_id": movie['_id']})
    if movie_embedding:
        return
    else:
        embedding, _ = get_embedding([movie['plot']])
        embedding = embedding.tolist()[0]
        embeddings_bson = [float(value) for value in embedding]
        movie['embedding'] = embeddings_bson
        await Embedded_movies2.insert_one(movie_embedding)
        return movie_embedding

