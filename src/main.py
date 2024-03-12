from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import config
from src.db import db
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=config['CORS_ORIGINS'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = [
  {
    '$search': {
      'index': "compount-query-custom-score-tutorial",
      'text': {
        'query': "{\"genres\":{$eq:\"Aniaton\"}}",
        'path': {
          'wildcard': "*"
        },
        'fuzzy':{}
      }
    }
  }
]
# pipeline2 = [
#   {
#     '$search': {
#       'index': "autoComplete",
#       'autocomplete':{
#           'query': "Animat",
#           'path':'name',
#           'tokenOrder':'sequential'
#       }
#     }
#   },
#     {
#         '$limit':5
#     }
# ]
result = db['movies'].aggregate(pipeline)
print(result)
result=list(result)
for i in result[:5]:
    print(i['title'])
    # print(i['genres'])

@app.get("/")
async def root():
    print('Hello World')
    return {"message": "Hello World"}