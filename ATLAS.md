**Atlas Search Compound Query**:

- **Alter Score using constant option**

```python
import pymongo

# connect to your Atlas cluster
client = pymongo.MongoClient('<connection-string>')

# define pipeline
pipeline = [
  {'$search': {
      'index': 'compound-query-custom-score-tutorial',
      'compound': {
        'filter': [{'range': {'path': 'year', 'gte': 2013, 'lte': 2015}}],
        'should': [{'text': {'query': 'snow', 'path': 'title', 'score': {'constant': {'value': 5}}}}]},
      'highlight': {'path': 'title'}}},
  {'$limit': 10},
  {'$project': {'_id': 0, 'title': 1, 'year': 1,
    'score': {'$meta': 'searchScore'}, "highlights": {"$meta": "searchHighlights"}}}
]

# run pipeline
result = client['sample_mflix']['movies'].aggregate(pipeline)

# print results
for i in result:
    print(i)

```

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

<!-- /code_chunk_output -->

Uses the following compound clauses to query the collection:

1. **filter** clause with the range operator to search for movies between the years 2013 to 2015.

2. **should** clause with the text operator to query for the term snow in the title field and alter the score with the constant option. The constant option replaces all score results for the search term with 5.

Specifies the **highlight** option to return snippets of text from the title field that match the query. The snippets contain matching text specified with type: 'hit', and adjacent text specified with type: 'text'.

Uses the following pipeline stages:

1. **$limit** stage to limit the output to 10 results

2. **$project** stage to:
   - Exclude all fields except title and year
   - Add two fields named score and highlights

- **Alter Score using boost option(Single Weight Example)**

```python
import pymongo

# connect to your Atlas cluster
client = pymongo.MongoClient('<connection-string>')

# define pipeline
pipeline = [
  {'$search': {
      'index': 'compound-query-custom-score-tutorial',
      'compound': {
        'must': [{'range': {'path': 'year', 'gte': 2013, 'lte': 2015}}],
        'should': [{'text': {'query': 'snow', 'path': 'title', 'score': {'boost': {'value': 2}}}}]},
      'highlight': {'path': 'title'}}},
  {'$limit': 10},
  {'$project': {'_id': 0, 'title': 1, 'year': 1, 'score': {'$meta': 'searchScore'}, "highlights": {"$meta": "searchHighlights"}}}
]

# run pipeline
result = client['sample_mflix']['movies'].aggregate(pipeline)

# print results
for i in result:
    print(i)

```

- **Alter Score using boost option(Multiple Weight Example)**

```python
import pymongo
import dns

client = pymongo.MongoClient('<connection-string>')
result = client['sample_mflix']['movies'].aggregate([
    {
        '$search': {
            'index': 'compound-query-custom-score-tutorial',
            'compound': {
                'must': [
                    {
                        'text': {
                            'path': 'genres',
                            'query': 'comedy',
                            'score': {
                                'boost': {
                                    'value': 9
                                }
                            }
                        }
                    }, {
                        'text': {
                            'path': 'title',
                            'query': 'snow',
                            'score': {
                                'boost': {
                                    'value': 5
                                }
                            }
                        }
                    }
                ],
                'should': [
                    {
                        'range': {
                            'path': 'year',
                            'gte': 2013,
                            'lte': 2015,
                            'score': {
                                'boost': {
                                    'value': 3
                                }
                            }
                        }
                    }
                ]
            }
        }
    }, {
        '$limit': 10
    }, {
        '$project': {
            '_id': 0,
            'title': 1,
            'year': 1,
            'genres': 1,
            'score': {
                '$meta': 'searchScore'
            }
        }
    }
])

for i in result:
    print(i)

```

1. **$search** stage to query the collection. The query uses the following compound operator clauses with the boost option to prioritize some fields more than other fields:

   - **must** clause with the text operator to prioritize the genre comedy the most, followed by the term snow in the title field. The boost option applies weights to the fields.

   - **should** clause with the range operator to search for movies between the years 2013 to 2015.

1. **$limit** stage to limit the output to 10 results.

1. **$project** stage to:
   - Exclude all fields except title, year, and genres.
   - Add a field named score.

- _Difference Between constant and boost_:

1. **Boost**:
   - The boost option allows you to specify a boost factor for a particular field or condition in your search query.
   - When you boost a field or condition, documents matching that field or condition will have their relevance score increased, making them more likely to appear higher in the search results.
   - Boosting is useful when you want to emphasize certain fields or conditions in your search results.
   ```json
   {
     "query": {
       "text": {
         "path": "title",
         "query": "example",
         "boost": 2
       }
     }
   }
   ```
   - In this example, documents containing the term "example" in the "title" field will have their relevance score doubled compared to other documents.
2. **Constant**:
   - The constant option allows you to assign a constant value to a field or condition in your search query, disregarding the actual content of the field.
   - This is useful when you want to apply a constant boost or penalty to certain documents based on specific conditions, regardless of the actual content of the documents.
   ```json
   {
     "query": {
       "text": {
         "path": "title",
         "query": "example",
         "constant": 2
       }
     }
   }
   ```
   - In this example, all documents having the "category" field set to "electronics" will have their relevance score increased by a constant factor of 2, regardless of the content of the documents.

- **Alter Score using function option**

```python
import pymongo

# connect to your Atlas cluster
client = pymongo.MongoClient('<connection-string>')

# define pipeline
pipeline = [
  {'$search': {
      'index': 'compound-query-custom-score-tutorial',
      'compound': {
        'must': [{'range': {'path': 'year', 'gte': 2013, 'lte': 2015}}],
        'should': [{'text': {'query': 'snow', 'path': 'title',
                    'score': {'function': {
                        'add': [{'path': {'value': 'imdb.rating','undefined': 2}}, {'score': 'relevance'}]}}}}]},
      'highlight': {'path': 'title'}}},
  {'$limit': 10},
  {'$project': {'_id': 0, 'title': 1, 'year': 1, 'score': {'$meta': 'searchScore'}, "highlights": {"$meta": "searchHighlights"}}}
]

# run pipeline
result = client['sample_mflix']['movies'].aggregate(pipeline)

# print results
for i in result:
    print(i)

```

1. Function option basically allow us to score the data on the basis of imdb.ratings(that is any Field of choice and can provide default value if it may not exist).
2. **must** clause with the range operator to search for movies between the years 2013 to 2015.

3. **should** clause with the text operator to query for the term snow in the title field and alter the score with the **function** option. The function option adds the following using an arithmetic expression:

   - The relevance score of the query for the search term
   - The value of the numeric field named imdb.rating or the number 2 for those documents that do not have the imdb.rating field.

4. Specifies the highlight option to return snippets of text from the title field that match the query. The snippets contain matching text specified with type: 'hit', and adjacent text specified with type: 'text'.

Uses the following pipeline stages:

1. $limit stage to limit the output to 10 results
2. $project stage to:
   - Exclude all fields except title and year
   - Add two fields named score and highlights

### Highlight Search Terms in Results

Add fields to the result that displays search terms in their original context.
[Read more ](https://www.mongodb.com/docs/atlas/atlas-search/highlighting/)
