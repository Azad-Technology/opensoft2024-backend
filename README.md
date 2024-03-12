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
        "_id": "573a1390f29313caabcd4803",
        "plot": "Cartoon figures announce, via comic strip balloons, that they will move - and move they do, in a wildly exaggerated style.",
        "genres": [
            "Animation",
            "Short",
            "Comedy"
        ],
        "runtime": 7,
        "cast": [
            "Winsor McCay"
        ],
        "num_mflix_comments": 0,
        "poster": "https://m.media-amazon.com/images/M/MV5BYzg2NjNhNTctMjUxMi00ZWU4LWI3ZjYtNTI0NTQxNThjZTk2XkEyXkFqcGdeQXVyNzg5OTk2OA@@._V1_SY1000_SX677_AL_.jpg",
        "title": "Winsor McCay, the Famous Cartoonist of the N.Y. Herald and His Moving Comics",
        "fullplot": "Cartoonist Winsor McCay agrees to create a large set of drawings that will be photographed and made into a motion picture. The job requires plenty of drawing supplies, and the cartoonist must also overcome some mishaps caused by an assistant. Finally, the work is done, and everyone can see the resulting animated picture.",
        "languages": [
            "English"
        ],
        "released": "1911-04-08T00:00:00",
        "directors": [
            "Winsor McCay",
            "J. Stuart Blackton"
        ],
        "writers": [
            "Winsor McCay (comic strip \"Little Nemo in Slumberland\")",
            "Winsor McCay (screenplay)"
        ],
        "awards": {
            "wins": 1,
            "nominations": 0,
            "text": "1 win."
        },
        "lastupdated": "2015-08-29 01:09:03.030000000",
        "year": 1911,
        "imdb": {
            "rating": 7.3,
            "votes": 1034,
            "id": 1737
        },
        "countries": [
            "USA"
        ],
        "type": "movie",
        "tomatoes": {
            "viewer": {
                "rating": 3.4,
                "numReviews": 89,
                "meter": 47
            },
            "lastUpdated": "2015-08-20T18:51:24"
        }
    },
    {
        "_id": "573a1390f29313caabcd50e5",
        "plot": "The cartoonist, Winsor McCay, brings the Dinosaurus back to life in the figure of his latest creation, Gertie the Dinosaur.",
        "genres": [
            "Animation",
            "Short",
            "Comedy"
        ],
        "runtime": 12,
        "cast": [
            "Winsor McCay",
            "George McManus",
            "Roy L. McCardell"
        ],
        "num_mflix_comments": 0,
        "poster": "https://m.media-amazon.com/images/M/MV5BMTQxNzI4ODQ3NF5BMl5BanBnXkFtZTgwNzY5NzMwMjE@._V1_SY1000_SX677_AL_.jpg",
        "title": "Gertie the Dinosaur",
        "fullplot": "Winsor Z. McCay bets another cartoonist that he can animate a dinosaur. So he draws a big friendly herbivore called Gertie. Then he get into his own picture. Gertie walks through the picture, eats a tree, meets her creator, and takes him carefully on her back for a ride.",
        "languages": [
            "English"
        ],
        "released": "1914-09-15T00:00:00",
        "directors": [
            "Winsor McCay"
        ],
        "writers": [
            "Winsor McCay"
        ],
        "awards": {
            "wins": 1,
            "nominations": 0,
            "text": "1 win."
        },
        "lastupdated": "2015-08-18 01:03:15.313000000",
        "year": 1914,
        "imdb": {
            "rating": 7.3,
            "votes": 1837,
            "id": 4008
        },
        "countries": [
            "USA"
        ],
        "type": "movie",
        "tomatoes": {
            "viewer": {
                "rating": 3.7,
                "numReviews": 29
            },
            "lastUpdated": "2015-08-10T19:20:03"
        }
    },
    {
        "_id": "573a13a5f29313caabd13572",
        "plot": "Cartoon figures announce, via comic strip balloons, that they will move - and move they do, in a wildly exaggerated style.",
        "genres": [
            "Animation",
            "Short",
            "Comedy"
        ],
        "runtime": 7,
        "cast": [
            "Winsor McCay"
        ],
        "poster": "https://m.media-amazon.com/images/M/MV5BYzg2NjNhNTctMjUxMi00ZWU4LWI3ZjYtNTI0NTQxNThjZTk2XkEyXkFqcGdeQXVyNzg5OTk2OA@@._V1_SY1000_SX677_AL_.jpg",
        "title": "Winsor McCay, the Famous Cartoonist of the N.Y. Herald and His Moving Comics",
        "fullplot": "Cartoonist Winsor McCay agrees to create a large set of drawings that will be photographed and made into a motion picture. The job requires plenty of drawing supplies, and the cartoonist must also overcome some mishaps caused by an assistant. Finally, the work is done, and everyone can see the resulting animated picture.",
        "languages": [
            "English"
        ],
        "released": "1911-04-08T00:00:00",
        "directors": [
            "Winsor McCay",
            "J. Stuart Blackton"
        ],
        "writers": [
            "Winsor McCay (comic strip \"Little Nemo in Slumberland\")",
            "Winsor McCay (screenplay)"
        ],
        "awards": {
            "wins": 1,
            "nominations": 0,
            "text": "1 win."
        },
        "lastupdated": "2015-08-31 01:05:38.577000000",
        "year": 1911,
        "imdb": {
            "rating": 7.3,
            "votes": 1036,
            "id": 1737
        },
        "countries": [
            "USA"
        ],
        "type": "movie",
        "num_mflix_comments": 0
    }
  ] 
  ```

- **Get Movie by cast**:
  Endpoint: `GET /cast/{cast_name}`

  Response:

  ```json5
  [
    {
        "_id": "573a1390f29313caabcd4803",
        "plot": "Cartoon figures announce, via comic strip balloons, that they will move - and move they do, in a wildly exaggerated style.",
        "genres": [
            "Animation",
            "Short",
            "Comedy"
        ],
        "runtime": 7,
        "cast": [
            "Winsor McCay"
        ],
        "num_mflix_comments": 0,
        "poster": "https://m.media-amazon.com/images/M/MV5BYzg2NjNhNTctMjUxMi00ZWU4LWI3ZjYtNTI0NTQxNThjZTk2XkEyXkFqcGdeQXVyNzg5OTk2OA@@._V1_SY1000_SX677_AL_.jpg",
        "title": "Winsor McCay, the Famous Cartoonist of the N.Y. Herald and His Moving Comics",
        "fullplot": "Cartoonist Winsor McCay agrees to create a large set of drawings that will be photographed and made into a motion picture. The job requires plenty of drawing supplies, and the cartoonist must also overcome some mishaps caused by an assistant. Finally, the work is done, and everyone can see the resulting animated picture.",
        "languages": [
            "English"
        ],
        "released": "1911-04-08T00:00:00",
        "directors": [
            "Winsor McCay",
            "J. Stuart Blackton"
        ],
        "writers": [
            "Winsor McCay (comic strip \"Little Nemo in Slumberland\")",
            "Winsor McCay (screenplay)"
        ],
        "awards": {
            "wins": 1,
            "nominations": 0,
            "text": "1 win."
        },
        "lastupdated": "2015-08-29 01:09:03.030000000",
        "year": 1911,
        "imdb": {
            "rating": 7.3,
            "votes": 1034,
            "id": 1737
        },
        "countries": [
            "USA"
        ],
        "type": "movie",
        "tomatoes": {
            "viewer": {
                "rating": 3.4,
                "numReviews": 89,
                "meter": 47
            },
            "lastUpdated": "2015-08-20T18:51:24"
        }
    },
    {
        "_id": "573a1390f29313caabcd50e5",
        "plot": "The cartoonist, Winsor McCay, brings the Dinosaurus back to life in the figure of his latest creation, Gertie the Dinosaur.",
        "genres": [
            "Animation",
            "Short",
            "Comedy"
        ],
        "runtime": 12,
        "cast": [
            "Winsor McCay",
            "George McManus",
            "Roy L. McCardell"
        ],
        "num_mflix_comments": 0,
        "poster": "https://m.media-amazon.com/images/M/MV5BMTQxNzI4ODQ3NF5BMl5BanBnXkFtZTgwNzY5NzMwMjE@._V1_SY1000_SX677_AL_.jpg",
        "title": "Gertie the Dinosaur",
        "fullplot": "Winsor Z. McCay bets another cartoonist that he can animate a dinosaur. So he draws a big friendly herbivore called Gertie. Then he get into his own picture. Gertie walks through the picture, eats a tree, meets her creator, and takes him carefully on her back for a ride.",
        "languages": [
            "English"
        ],
        "released": "1914-09-15T00:00:00",
        "directors": [
            "Winsor McCay"
        ],
        "writers": [
            "Winsor McCay"
        ],
        "awards": {
            "wins": 1,
            "nominations": 0,
            "text": "1 win."
        },
        "lastupdated": "2015-08-18 01:03:15.313000000",
        "year": 1914,
        "imdb": {
            "rating": 7.3,
            "votes": 1837,
            "id": 4008
        },
        "countries": [
            "USA"
        ],
        "type": "movie",
        "tomatoes": {
            "viewer": {
                "rating": 3.7,
                "numReviews": 29
            },
            "lastUpdated": "2015-08-10T19:20:03"
        }
    },
    {
        "_id": "573a13a5f29313caabd13572",
        "plot": "Cartoon figures announce, via comic strip balloons, that they will move - and move they do, in a wildly exaggerated style.",
        "genres": [
            "Animation",
            "Short",
            "Comedy"
        ],
        "runtime": 7,
        "cast": [
            "Winsor McCay"
        ],
        "poster": "https://m.media-amazon.com/images/M/MV5BYzg2NjNhNTctMjUxMi00ZWU4LWI3ZjYtNTI0NTQxNThjZTk2XkEyXkFqcGdeQXVyNzg5OTk2OA@@._V1_SY1000_SX677_AL_.jpg",
        "title": "Winsor McCay, the Famous Cartoonist of the N.Y. Herald and His Moving Comics",
        "fullplot": "Cartoonist Winsor McCay agrees to create a large set of drawings that will be photographed and made into a motion picture. The job requires plenty of drawing supplies, and the cartoonist must also overcome some mishaps caused by an assistant. Finally, the work is done, and everyone can see the resulting animated picture.",
        "languages": [
            "English"
        ],
        "released": "1911-04-08T00:00:00",
        "directors": [
            "Winsor McCay",
            "J. Stuart Blackton"
        ],
        "writers": [
            "Winsor McCay (comic strip \"Little Nemo in Slumberland\")",
            "Winsor McCay (screenplay)"
        ],
        "awards": {
            "wins": 1,
            "nominations": 0,
            "text": "1 win."
        },
        "lastupdated": "2015-08-31 01:05:38.577000000",
        "year": 1911,
        "imdb": {
            "rating": 7.3,
            "votes": 1036,
            "id": 1737
        },
        "countries": [
            "USA"
        ],
        "type": "movie",
        "num_mflix_comments": 0
    }
  ]
  ```