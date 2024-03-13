<br/>
<br/>
<h1 align="center">OPEN SOFT 2024 BACKEND</h1>


## Project Structure
The project is structured as follows, ensuring modular and organized management of various functionalities:


```
project_root
│
├── src
│   ├── routers
│   │   └── auth.py
│   ├── config.py
│   ├── db.py
│   ├── main.py
│   ├── __init__.py
│   └── schemas.py
├── .env
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

<br />
<br />

<h2> Setup and Installation</h2>

<h3>Setup</h3>
<ol>
    <strong>Install dependencies</strong>:
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
  <br />
  <li>
    <strong>Setup environment variables</strong>:
    <ul>
      <li>Copy the <code>.env.example</code> to a new file called <code>.env</code>.
        <pre><code>cp .env.example .env</code></pre>
      </li>
      <li>Open the <code>.env</code> file and populate it with the necessary values for each variable:
        <ul>
          <li><code>JWT_KEY</code>: Enter a secure key for encoding and decoding JSON Web Tokens.</li>
          <li><code>CORS_ORIGINS</code>: Define the allowed origins for Cross-Origin Resource Sharing. Use <code>*</code> for allowing all origins in a development environment.</li>
          <li><code>DATABASE_URL</code>: Input the connection URI for your MongoDB Instance</li>
        </ul>
      </li>
    </ul>
  </li>
  <br />
  <li>
    <strong>Run the application</strong>:
    <pre><code>uvicorn src.main:app --reload</code></pre>
    <p>This will start the FastAPI application with hot reloading enabled.</p>
  </li>
</ol>

<br />
<br />



## Usage

- **User SignUp**:
  Endpoint: `POST /signup`

  Request:
  ```json5
  {
    "name": str,
    "email": str,
    "password": str
  }
  ```

- **User Login**:
  Endpoint: `POST /login`

  Request:
  ```json5
  {
    "email": str,
    "password": str
  }
  ```
  Response:
  ```json5
  {
    "status": "success",
    "token": {jwt_token}
  }
  ```



- **Get Movie by ID**:
  Endpoint: `GET /movies/{_id}`

  Response:

  ```json5
  {
    "_id": "573a1390f29313caabcd446f",
    "plot": "A greedy tycoon decides, on a whim, to corner the world market in wheat. This doubles the price of bread, forcing the grain's producers into charity lines and further into poverty. The film...",
    "genres": [
        "Short",
        "Drama"
    ],
    "runtime": 14,
    "cast": [
        "Frank Powell",
        "Grace Henderson",
        "James Kirkwood",
        "Linda Arvidson"
    ],
    "num_mflix_comments": 1,
    "title": "A Corner in Wheat",
    "fullplot": "A greedy tycoon decides, on a whim, to corner the world market in wheat. This doubles the price of bread, forcing the grain's producers into charity lines and further into poverty. The film continues to contrast the ironic differences between the lives of those who work to grow the wheat and the life of the man who dabbles in its sale for profit.",
    "languages": [
        "English"
    ],
    "released": "1909-12-13T00:00:00",
    "directors": [
        "D.W. Griffith"
    ],
    "rated": "G",
    "awards": {
        "wins": 1,
        "nominations": 0,
        "text": "1 win."
    },
    "lastupdated": "2015-08-13 00:46:30.660000000",
    "year": 1909,
    "imdb": {
        "rating": 6.6,
        "votes": 1375,
        "id": 832
    },
    "countries": [
        "USA"
    ],
    "type": "movie",
    "tomatoes": {
        "viewer": {
            "rating": 3.6,
            "numReviews": 109,
            "meter": 73
        },
        "lastUpdated": "2015-05-11T18:36:53"
    }
  }
  ```
  

- **Get Movie by Director**:
  Endpoint: `GET /director/{director_name}`

  Response:

  ```json5
  [
    {
        "_id": "573a1390f29313caabcd5a93",
        "runtime": 78,
        "poster": "https://m.media-amazon.com/images/M/MV5BMjAwNTIxMjE5N15BMl5BanBnXkFtZTgwODc1Mjg1MzE@._V1_SY1000_SX677_AL_.jpg",
        "title": "Civilization",
        "released": "1916-06-02T00:00:00",
        "imdb": {
            "rating": 6.3,
            "votes": 162,
            "id": 6517
        },
        "tomatoes": {
            "viewer": {
                "rating": 0.0,
                "numReviews": 7
            },
            "lastUpdated": "2015-08-07T18:42:35"
        }
    }
    ...
    ]
  ```

- **Get Movie by cast**:
  Endpoint: `GET /cast/{cast_name}`

  Response:

  ```json5
    [
    {
        "_id": "573a1390f29313caabcd5a93",
        "runtime": 78,
        "poster": "https://m.media-amazon.com/images/M/MV5BMjAwNTIxMjE5N15BMl5BanBnXkFtZTgwODc1Mjg1MzE@._V1_SY1000_SX677_AL_.jpg",
        "title": "Civilization",
        "released": "1916-06-02T00:00:00",
        "imdb": {
            "rating": 6.3,
            "votes": 162,
            "id": 6517
        },
        "tomatoes": {
            "viewer": {
                "rating": 0.0,
                "numReviews": 7
            },
            "lastUpdated": "2015-08-07T18:42:35"
        }
    }
    ...
    ]
  ```

- **Get Movie by genre**:
  Endpoint: `GET /genre/{genre_name}`
  
  Response:

    ```json5
   [
    {
        "_id": "573a1392f29313caabcd9cfb",
        "runtime": 100,
        "poster": "https://m.media-amazon.com/images/M/MV5BNTVlMDAwMDQtMTEzMC00YjhlLWEyYTctNjMzN2M0NGI0MTEwXkEyXkFqcGdeQXVyNDE5MTU2MDE@._V1_SY1000_SX677_AL_.jpg",
        "title": "Tarzan the Ape Man",
        "released": "1932-04-02T00:00:00",
        "imdb": {
            "rating": 7.2,
            "votes": 5182,
            "id": 23551
        },
        "tomatoes": {
            "viewer": {
                "rating": 3.5,
                "numReviews": 948,
                "meter": 69
            },
            "critic": {
                "rating": 7.8,
                "numReviews": 13,
                "meter": 100
            },
            "lastUpdated": "2015-09-12T18:54:59",
            "rotten": 0,
            "production": "MGM Home Entertainment",
            "fresh": 13
        }
    },
    ...
    {
        "_id": "573a1393f29313caabcdcc03",
        "runtime": 124,
        "poster": "https://m.media-amazon.com/images/M/MV5BMjU0MDY5OWEtNmMzNC00ZTJmLWIxNmMtM2U3NWNmNTY5ODA5XkEyXkFqcGdeQXVyMDI2NDg0NQ@@._V1_SY1000_SX677_AL_.jpg",
        "title": "Air Force",
        "released": "1943-03-20T00:00:00",
        "imdb": {
            "rating": 7.1,
            "votes": 2040,
            "id": 35616
        },
        "tomatoes": {
            "viewer": {
                "rating": 3.6,
                "numReviews": 372,
                "meter": 70
            },
            "dvd": "2007-06-05T00:00:00",
            "critic": {
                "rating": 7.6,
                "numReviews": 8,
                "meter": 88
            },
            "lastUpdated": "2015-09-10T18:52:13",
            "rotten": 1,
            "production": "WARNER BROTHERS PICTURES",
            "fresh": 7
        }
    }
    ]
    ```
