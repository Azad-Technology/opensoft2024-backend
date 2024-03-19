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

  Response:

  ```json5
  {
    "status": "success",
    "message": "User created successfully.",
    "token": {jwt_token},
    "type": "Basic"
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
    "token": {jwt_token},
    "type": {subtype}
  }
  ```

- **Get Movie by ID**:
  Endpoint: `GET /movies/{movie_id}`

  Response:

  ```json5
  {
    _id: "573a1390f29313caabcd446f",
    plot: "A greedy tycoon decides, on a whim, to corner the world market in wheat. This doubles the price of bread, forcing the grain's producers into charity lines and further into poverty. The film...",
    genres: ["Short", "Drama"],
    runtime: 14,
    cast: [
      "Frank Powell",
      "Grace Henderson",
      "James Kirkwood",
      "Linda Arvidson",
    ],
    num_mflix_comments: 1,
    title: "A Corner in Wheat",
    fullplot: "A greedy tycoon decides, on a whim, to corner the world market in wheat. This doubles the price of bread, forcing the grain's producers into charity lines and further into poverty. The film continues to contrast the ironic differences between the lives of those who work to grow the wheat and the life of the man who dabbles in its sale for profit.",
    languages: ["English"],
    released: "1909-12-13T00:00:00",
    directors: ["D.W. Griffith"],
    rated: "G",
    awards: {
      wins: 1,
      nominations: 0,
      text: "1 win.",
    },
    lastupdated: "2015-08-13 00:46:30.660000000",
    year: 1909,
    imdb: {
      rating: 6.6,
      votes: 1375,
      id: 832,
    },
    countries: ["USA"],
    type: "movie",
    tomatoes: {
      viewer: {
        rating: 3.6,
        numReviews: 109,
        meter: 73,
      },
      lastUpdated: "2015-05-11T18:36:53",
    },
  }
  ```

- **Get Movie by Director**:
  Endpoint: `GET /director/{director_name}/?count=3`

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
  Endpoint: `GET /cast/{cast_name}/?count=2`

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

  ]
  ```

- **Get top count number of series by imdb rating**:
  Endpoint: `GET /imdb/?count={count}`

  Response:

  ```json5
  [
   {
      "_id": "573a139ff29313caabd003c4",
      "runtime": 705,
      "poster": "https://m.media-amazon.com/images/M/MV5BMTI3ODc2ODc0M15BMl5BanBnXkFtZTYwMjgzNjc3._V1_SY1000_SX677_AL_.jpg",
      "title": "Band of Brothers",
      "released": "2001-09-09T00:00:00",
      "imdb": {
          "rating": 9.6,
          "votes": 183802,
          "id": 185906
      },
      "tomatoes": {
          "viewer": {
              "rating": 2.0,
              "numReviews": 15
          },
          "dvd": "2009-03-17T00:00:00",
          "lastUpdated": "2015-09-12T17:15:33"
      }
  },
  ...

  ]
  ```

  - **Get top count number of movies by imdb rating**:
    Endpoint: `GET /imdb/?count={count}`

  Response:

  ```json5
  [
   {
        "_id": "573a13f0f29313caabdda542",
        "runtime": 78,
        "poster": "https://m.media-amazon.com/images/M/MV5BMTU4MTcwMzU5Ml5BMl5BanBnXkFtZTgwOTQwMzM2NDE@._V1_SY1000_SX677_AL_.jpg",
        "title": "A Brave Heart: The Lizzie Velasquez Story",
        "released": "2015-09-25T00:00:00",
        "imdb": {
            "rating": 9.4,
            "votes": 45,
            "id": 3735302
        }
   }
  ...

  ]
  ```

- **Get top count number of series for a genre**:
  Endpoint: `GET /genre_top/{genre_name}/?count={count}`

  Response:

  ```json5
  [
   {
      "_id": "573a139ff29313caabd003c4",
      "runtime": 705,
      "poster": "https://m.media-amazon.com/images/M/MV5BMTI3ODc2ODc0M15BMl5BanBnXkFtZTYwMjgzNjc3._V1_SY1000_SX677_AL_.jpg",
      "title": "Band of Brothers",
      "released": "2001-09-09T00:00:00",
      "imdb": {
          "rating": 9.6,
          "votes": 183802,
          "id": 185906
      },
      "tomatoes": {
          "viewer": {
              "rating": 2.0,
              "numReviews": 15
          },
          "dvd": "2009-03-17T00:00:00",
          "lastUpdated": "2015-09-12T17:15:33"
      }
  },
  ...

  ]
  ```

  - **Get top count number of series or movies for a genre**:
    Endpoint: `GET /genre_top/{genre_name}/?count={count}`

  Response:

  ```json5
  [
   {
      "_id": "573a139ff29313caabd003c4",
      "runtime": 705,
      "poster": "https://m.media-amazon.com/images/M/MV5BMTI3ODc2ODc0M15BMl5BanBnXkFtZTYwMjgzNjc3._V1_SY1000_SX677_AL_.jpg",
      "title": "Band of Brothers",
      "released": "2001-09-09T00:00:00",
      "imdb": {
          "rating": 9.6,
          "votes": 183802,
          "id": 185906
      },
      "tomatoes": {
          "viewer": {
              "rating": 2.0,
              "numReviews": 15
          },
          "dvd": "2009-03-17T00:00:00",
          "lastUpdated": "2015-09-12T17:15:33"
      }
  },
  ...

  ]
  ```

- **Get top count number of movies for a genre**:
  Endpoint: `GET /genre_top/{genre_name}/?count={count}`

  Response:

  ```json5
  [
   {
        "_id": "573a13f0f29313caabdda542",
        "runtime": 78,
        "poster": "https://m.media-amazon.com/images/M/MV5BMTU4MTcwMzU5Ml5BMl5BanBnXkFtZTgwOTQwMzM2NDE@._V1_SY1000_SX677_AL_.jpg",
        "title": "A Brave Heart: The Lizzie Velasquez Story",
        "released": "2015-09-25T00:00:00",
        "imdb": {
            "rating": 9.4,
            "votes": 45,
            "id": 3735302
        }
   },
  ...

  ]
  ```

  **Get top count number of movies or series in a country**:
  Endpoint: `GET /countries_top/{country_name}/?count={count}`

  Response:

  ```json5
  [
   {
      "_id": "573a139ff29313caabd003c4",
      "runtime": 705,
      "poster": "https://m.media-amazon.com/images/M/MV5BMTI3ODc2ODc0M15BMl5BanBnXkFtZTYwMjgzNjc3._V1_SY1000_SX677_AL_.jpg",
      "title": "Band of Brothers",
      "released": "2001-09-09T00:00:00",
      "imdb": {
          "rating": 9.6,
          "votes": 183802,
          "id": 185906
      },
      "tomatoes": {
          "viewer": {
              "rating": 2.0,
              "numReviews": 15
          },
          "dvd": "2009-03-17T00:00:00",
          "lastUpdated": "2015-09-12T17:15:33"
      }
  },
  ...

  ]
  ```

  - **Get top count number of series in a country**:
    Endpoint: `GET /genre_top/{genre_name}/?count={count}`

  Response:

  ```json5
  [
   {
      "_id": "573a139ff29313caabd003c4",
      "runtime": 705,
      "poster": "https://m.media-amazon.com/images/M/MV5BMTI3ODc2ODc0M15BMl5BanBnXkFtZTYwMjgzNjc3._V1_SY1000_SX677_AL_.jpg",
      "title": "Band of Brothers",
      "released": "2001-09-09T00:00:00",
      "imdb": {
          "rating": 9.6,
          "votes": 183802,
          "id": 185906
      },
      "tomatoes": {
          "viewer": {
              "rating": 2.0,
              "numReviews": 15
          },
          "dvd": "2009-03-17T00:00:00",
          "lastUpdated": "2015-09-12T17:15:33"
      }
  },
  ...

  ]
  ```

- **Get top count number of movies in a genre**:
  Endpoint: `GET /genre_top/{genre_name}/?count={count}`

  Response:

  ```json5
  [
   {
        "_id": "573a13f0f29313caabdda542",
        "runtime": 78,
        "poster": "https://m.media-amazon.com/images/M/MV5BMTU4MTcwMzU5Ml5BMl5BanBnXkFtZTgwOTQwMzM2NDE@._V1_SY1000_SX677_AL_.jpg",
        "title": "A Brave Heart: The Lizzie Velasquez Story",
        "released": "2015-09-25T00:00:00",
        "imdb": {
            "rating": 9.4,
            "votes": 45,
            "id": 3735302
        }
   },
  ...

  ]
  ```

- **Update user email and password**:
  Endpoint: `PATCH /update_user/?new_email={new_email}&new_pass={new_pass}`

  Response:

  ```json5
  [
    {
      message: "Password updated successfully.",
      user: {
        _id: "65f80524e83724b666e03962",
        name: "Warrior",
        email: "warrior@example.com",
        password: "$2b$12$oiGs4x3erffC/O56CxUA6ec.awL6SDvkcRdUb4O1TX60Td3vafPci",
      },
    },
  ]
  ```

- **Create comment**:
  Endpoint: `POST /comment`

  Request:

  ```json5
  {
    "movie_name": str,
    "comment": str
  }
  ```

- **Update user subscription**:
  Endpoint: `PATCH /update_subs/{new_subscription}`

  Response:

  ```json5
  [
    {
      message: "Your subscription has been changed from Basic to Gold .",
      user: {
        _id: "65f80524e83724b666e03962",
        name: "Warrior",
        email: "shv1@example.com",
        password: "Example@password2",
        last_change: "2024-03-18",
        role: "user",
        subtype: "Gold",
      },
    },
  ]
  ```

- **Cancel user subscription**:
  Endpoint: `PATCH /cancel_subs`

  Response:

  ```json5
  [
    {
      message: "Your subscription has been changed from Gold to Basic .",
      user: {
        _id: "65f80524e83724b666e03962",
        name: "Warrior",
        email: "shv1@example.com",
        password: "Example@password2",
        last_change: "2024-03-18",
        role: "user",
        subtype: "Basic",
      },
    },
  ]
  ```

- **Get recommended movies from movie id**:
  Endpoint: `GET /movies/{movie_id}/related_movies/?count=1`

  Response:

  ```json5
  [
  {
    "_id": "573a13a7f29313caabd1c099",
    "imdb": {
      "rating": 7.8,
      "votes": 341206,
      "id": 304141
    },
    "genres": [
      "Adventure",
      "Family",
      "Fantasy"
    ],
    "title": "Harry Potter and the Prisoner of Azkaban",
    "tomatoes": {
      "website": "http://azkaban.warnerbros.com/",
      "viewer": {
        "rating": 3.8,
        "numReviews": 1163226,
        "meter": 86
      },
      "dvd": "2004-11-22T00:00:00",
      "critic": {
        "rating": 7.9,
        "numReviews": 249,
        "meter": 91
      },
      "boxOffice": "$249.4M",
      "consensus": "Under the assured direction of Alfonso Cuaron, Harry Potter and the Prisoner of Azkaban triumphantly strikes a delicate balance between technical wizardry and complex storytelling.",
      "rotten": 23,
      "production": "Warner Bros. Pictures",
      "lastUpdated": "2015-09-12T17:26:42",
      "fresh": 226
    },
    "poster": "https://m.media-amazon.com/images/M/MV5BMTY4NTIwODg0N15BMl5BanBnXkFtZTcwOTc0MjEzMw@@._V1_SY1000_SX677_AL_.jpg",
    "released": "2004-06-04T00:00:00",
    "runtime": 142,
    "title_similarity": 4,
    "genre_intersection": 3,
    "cast_intersection": 0,
    "director_intersection": 0,
    "region_intersection": 2,
    "relevance_score1": 8.112341772151899,
    "relevance_score": 237.4987341772152
  }
  ...
  ]
  ```

  - **Get comments for a movie**:
  Endpoint: `GET /movies/573a13a3f29313caabd0d4c5/comments/?count=1`

  Response:

  ```json5
  [
  {
    "_id": "5a9427658b0beebeb6968ea9",
    "name": "Joffrey Baratheon",
    "email": "jack_gleeson@gameofthron.es",
    "movie_id": "573a13a3f29313caabd0d4c5",
    "text": "Eos qui voluptate tempora recusandae quaerat eaque laudantium. Aliquam qui vero est suscipit. Architecto similique numquam quia placeat.",
    "date": "2017-06-20T03:01:39"
  }
  ...
  ]
  ```

  - **Get Recent Movies**:
  Endpoint: `GET /recent_movies/?count=1`

  Response:

  ```json5
  [
  {
    "_id": "573a13f8f29313caabde8d7a",
    "runtime": 89,
    "poster": "https://m.media-amazon.com/images/M/MV5BMTUzNjIyOTU1Ml5BMl5BanBnXkFtZTgwMjEzNzI2NzE@._V1_SY1000_SX677_AL_.jpg",
    "title": "The Treasure",
    "released": "2016-03-23T00:00:00",
    "imdb": {
      "rating": 7.5,
      "votes": 217,
      "id": 4515684
    }
  }
  ]
  ```

  - **Get movies from user's country**:
  Endpoint : `GET /my_country/?ip=8.8.8.8&count=3`

  Response:

  ```json5
  [
  {
    "_id": "573a13adf29313caabd2af91",
    "runtime": 160,
    "title": "Love is God",
    "released": "2003-01-14T00:00:00",
    "imdb": {
      "rating": 8.9,
      "votes": 4584,
      "id": 367495
    }
  }
  ...
  ]
  ```