from fastapi import FastAPI, APIRouter
from fastapi.testclient import TestClient
from src.routers import movie
app = FastAPI()
# router = APIRouter()
app.include_router(movie.router, tags=["Movie"])
client = TestClient(app)

movie_id="573a1390f29313caabcd587d"
invalid_movie_id="abcd"
unmatched_movie_id="65f73fa4f1ef0a9a45276f27"

def test_get_movie():
    response = client.get(
        f"/movies/{movie_id}"
    )
    assert response.status_code == 200
    assert response.json() == [{
        
    
        "_id": "573a1390f29313caabcd587d",
        "plot": "At 10 years old, Owens becomes a ragged orphan when his sainted mother dies. The Conways, who are next door neighbors, take Owen in, but the constant drinking by Jim soon puts Owen on the ...",
        "genres": [
            "Biography",
            "Crime",
            "Drama"
        ],
        "runtime": 72,
        "rated": "PASSED",
        "cast": [
            "John McCann",
            "James A. Marcus",
            "Maggie Weston",
            "Harry McCoy"
        ],
        "num_mflix_comments": 1,
        "poster": "https://m.media-amazon.com/images/M/MV5BNDkxZGU4NmMtODJlNy00YzA2LTg4ZGMtNGFlNzAyNzcxOTM1XkEyXkFqcGdeQXVyOTM3MjcyMjI@._V1_SY1000_SX677_AL_.jpg",
        "title": "Regeneration",
        "fullplot": "At 10 years old, Owens becomes a ragged orphan when his sainted mother dies. The Conways, who are next door neighbors, take Owen in, but the constant drinking by Jim soon puts Owen on the street. By 17, Owen learns that might is right. By 25, Owen is the leader of his own gang who spend most of their time gambling and drinking. But Marie comes into the gangster area of town and everything changes for Owen as he falls for Marie. But he cannot tell her so, so he comes to her settlement to find education and inspiration. But soon, his old way of life will rise to confront him again.",
        "languages": [
            "English"
        ],
        "released": "1915-09-13 00:00:00",
        "directors": [
            "Raoul Walsh"
        ],
        "writers": [
            "Owen Frawley Kildare (book)",
            "Raoul Walsh (adapted from the book: \"My Mamie Rose\")",
            "Carl Harbaugh (adapted from the book: \"My Mamie Rose\")"
        ],
        "awards": {
            "wins": 1,
            "nominations": 0,
            "text": "1 win."
        },
        "lastupdated": "2015-08-14 01:28:18.957000000",
        "year": 1915,
        "imdb": {
            "rating": 6.8,
            "votes": 626,
            "id": 5960
        },
        "countries": [
            "USA"
        ],
        "type": "movie",
        "poster_path": "/jWNif4E8ZRhqRBItr0FWVMz1ooO.jpg",
        "backdrop_path": "/kMVOGxOzn0ukgcOg8GLwpDpIOC6.jpg",
        "dvd": "2001-11-27 00:00:00",
        "lastUpdated": "2015-09-17 17:22:42"
    
    }

    ]

# changes done due to this
def test_get_movie_invalid_id():         
    response = client.get(
        f"/movies/{invalid_movie_id}"
    )
    assert response.status_code == 500
    assert response.json()=={
    "detail": "'abcd' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string"
}

def test_get_movie_emptyid():
    response = client.get(
        "/movies/"
    )
    assert response.status_code == 404
    assert response.json()=={
    "detail": "Not Found"
}
    
def test_get_movie_unmatched_id():
    response = client.get(
        f"movies/{unmatched_movie_id}"
    )
    assert response.status_code == 200
    assert response.json()==[]

def test_top_series():
    response = client.get(
        "/top_series"
    )
    assert response.status_code == 200
    assert response.json()==[
    {
        "_id": "573a139ff29313caabd003c4",
        "plot": "The story of Easy Company of the US Army 101st Airborne division and their mission in WWII Europe from Operation Overlord through V-J Day.",
        "genres": [
            "Action",
            "Drama",
            "History"
        ],
        "runtime": 705,
        "poster": "https://m.media-amazon.com/images/M/MV5BMTI3ODc2ODc0M15BMl5BanBnXkFtZTYwMjgzNjc3._V1_SY1000_SX677_AL_.jpg",
        "title": "Band of Brothers",
        "released": "2001-09-09 00:00:00",
        "year": 2001,
        "imdb": {
            "rating": 9.6,
            "votes": 183802,
            "id": 185906
        },
        "poster_path": "/9z36SDiSdsHk2GjbZ1MjqGsag6p.jpg",
        "backdrop_path": "/nCsKxSNONvUYEi1AXRXRmq6MWUb.jpg"
    },
    {
        "_id": "573a13b8f29313caabd4c241",
        "plot": "Emmy Award winning, 11-episodes, 5-years in the making, the most expensive nature documentary series ever commissioned by the BBC, and the first to be filmed in high definition.",
        "genres": [
            "Documentary"
        ],
        "runtime": 60,
        "poster": "https://m.media-amazon.com/images/M/MV5BNmZlYzIzMTItY2EzYS00YTEyLTg0ZjEtMDMzZjM3ODdhN2UzXkEyXkFqcGdeQXVyNjI0MDg2NzE@._V1_SY1000_SX677_AL_.jpg",
        "title": "Planet Earth",
        "released": "2007-03-25 00:00:00",
        "year": 2006,
        "imdb": {
            "rating": 9.5,
            "votes": 82896,
            "id": 795176
        },
        "poster_path": "/dCiVCPHOWhT1MEXWfe3vZPnTOB8.jpg",
        "backdrop_path": "/5krduK75j61udNXJCxQChM9OE2h.jpg"
    },
    {
        "_id": "573a1398f29313caabcebc0b",
        "plot": "A comprehensive survey of the American Civil War.",
        "genres": [
            "Documentary",
            "History",
            "War"
        ],
        "runtime": 680,
        "poster": "https://m.media-amazon.com/images/M/MV5BZDc1NzI2MGEtZDA2Yy00ZWExLTgwYmItNjU3N2QyYmM0MzYwXkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_SY1000_SX677_AL_.jpg",
        "title": "The Civil War",
        "released": "1990-09-23 00:00:00",
        "year": 1990,
        "imdb": {
            "rating": 9.4,
            "votes": 4625,
            "id": 98769
        },
        "poster_path": "/eYmzt4EfYlY5VzUqGu5BL5tscKP.jpg",
        "backdrop_path": "/pI0ke4M5OK2803ZufylqNpFnId2.jpg"
    },
    {
        "_id": "573a1397f29313caabce7c4b",
        "plot": "Astronomer Carl Sagan leads us on an engaging guided tour of the various elements and cosmological theories of the universe.",
        "genres": [
            "Documentary"
        ],
        "runtime": 60,
        "poster": "https://m.media-amazon.com/images/M/MV5BMTY4MGQyNjgtMzdmZS00MjQ5LWIyMzItYjYyZmQzNjVhYjMyXkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_SY1000_SX677_AL_.jpg",
        "title": "Cosmos",
        "released": "1980-09-28 00:00:00",
        "year": 1980,
        "imdb": {
            "rating": 9.3,
            "votes": 17174,
            "id": 81846
        },
        "poster_path": "/wquuj8Xlum4rUXCahVWbYSHpdzN.jpg",
        "backdrop_path": "/19T7pPt5y5vV8PKNqdpft8mxMUb.jpg"
    },
    {
        "_id": "573a1398f29313caabcea40a",
        "plot": "Ten television drama films, each one based on one of the Ten Commandments.",
        "genres": [
            "Drama"
        ],
        "runtime": 572,
        "poster": "https://m.media-amazon.com/images/M/MV5BZWIzNDIzMTYtN2RiZS00NjA1LWFjNzMtOWQ0MDYxNWI1YTJiXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_SY1000_SX677_AL_.jpg",
        "title": "The Decalogue",
        "released": "1989-12-10 00:00:00",
        "year": 1989,
        "imdb": {
            "rating": 9.2,
            "votes": 10958,
            "id": 92337
        },
        "poster_path": "/ipZEwcNtdqnt8SkkOoGO5sX4jPH.jpg",
        "backdrop_path": "/vMB1sHLkLugteLiT6NEkqKClOmP.jpg"
    },
    {
        "_id": "573a13d1f29313caabd8e8c6",
        "plot": "Like all life forms, humanity partially adapts to types of natural environment, yet also tends to change them. Each episode examines how life differs for men and nature in some type of ...",
        "genres": [
            "Documentary"
        ],
        "poster": "https://m.media-amazon.com/images/M/MV5BMjdhZjQzYjYtM2FmNS00Y2ExLThjODEtZGQzY2M3OWYzYzc0XkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_SY1000_SX677_AL_.jpg",
        "title": "Human Planet",
        "released": "2011-01-13 00:00:00",
        "year": 2011,
        "imdb": {
            "rating": 9.2,
            "votes": 9057,
            "id": 1806234
        },
        "poster_path": "/4l2hSCxYGiIgvd2P7RDtCSTmuMm.jpg",
        "backdrop_path": "/7U8jKj45KhpcEuk6nDjxpCRvusX.jpg"
    },
    {
        "_id": "573a13a7f29313caabd1a365",
        "plot": "Mammoth series, five years in the making, taking a look at the rich tapestry of life in the world's oceans.",
        "genres": [
            "Documentary"
        ],
        "runtime": 50,
        "poster": "https://m.media-amazon.com/images/M/MV5BZGFhMGNmNDktYjY0Mi00YWE1LTlmMDQtZTBiNmU4NGYzZjZkXkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_SY1000_SX677_AL_.jpg",
        "title": "The Blue Planet",
        "released": "2002-01-27 00:00:00",
        "year": 2001,
        "imdb": {
            "rating": 9.2,
            "votes": 7093,
            "id": 296310
        },
        "poster_path": "/rEeEdSM1ammUzjkpumVZJj2pWQy.jpg",
        "backdrop_path": "/m7xwb5hbFSID3gzVDlAm8uM45NX.jpg"
    },
    {
        "_id": "573a13f0f29313caabdd9d6e",
        "plot": "Two brothers find themselves lost in a mysterious land and try to find their way home.",
        "genres": [
            "Animation",
            "Adventure",
            "Comedy"
        ],
        "poster": "https://m.media-amazon.com/images/M/MV5BYjQwZDhhNzctNTZjYy00NjYzLWE3ZjctNGQwZWY2Zjg5NTgwL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_SY1000_SX677_AL_.jpg",
        "title": "Over the Garden Wall",
        "released": "2014-11-03 00:00:00",
        "year": 2014,
        "imdb": {
            "rating": 9.2,
            "votes": 4139,
            "id": 3718778
        }
    },
    {
        "_id": "573a13d6f29313caabda05f3",
        "plot": "Focuses on life and the environment in both the Arctic and Antarctic.",
        "genres": [
            "Documentary"
        ],
        "runtime": 60,
        "poster": "https://m.media-amazon.com/images/M/MV5BOGM5YWU2N2QtYjVhZi00MzYyLTk0ODctYmVlNDZlMjU5N2Q5XkEyXkFqcGdeQXVyMzU3MTc5OTE@._V1_SY1000_SX677_AL_.jpg",
        "title": "Frozen Planet",
        "released": "2012-03-18 00:00:00",
        "year": 2011,
        "imdb": {
            "rating": 9.2,
            "votes": 5903,
            "id": 2092588
        },
        "poster_path": "/1FJ1ZdLrwjFS0usafLQROvlGgN3.jpg"
    },
    {
        "_id": "573a13c9f29313caabd7a481",
        "plot": "David Attenborough's legendary BBC crew explains and shows wildlife all over planet earth in 10 episodes. The first is an overview the challenges facing life, the others are dedicated to ...",
        "genres": [
            "Documentary"
        ],
        "poster": "https://m.media-amazon.com/images/M/MV5BMzc0NzY3MjA0Nl5BMl5BanBnXkFtZTcwNTE3NzQyMw@@._V1._CR0,1,361,471_SY264_CR12,0,178,264_AL_.jpg",
        "title": "Life",
        "released": "2009-10-12 00:00:00",
        "year": 2009,
        "imdb": {
            "rating": 9.2,
            "votes": 16807,
            "id": 1533395
        },
        "poster_path": "/wztfli5NgYDgurVgShNflvnyA3Z.jpg",
        "backdrop_path": "/nNh7vHHISVAaziJEqAq0P9iL52w.jpg"
    }
]
    
def test_top_series_with_count():
    response = client.get(
        "/top_series/?count=1"
    )
    assert response.status_code == 200
    assert response.json()==[
        {
        "_id": "573a139ff29313caabd003c4",
        "plot": "The story of Easy Company of the US Army 101st Airborne division and their mission in WWII Europe from Operation Overlord through V-J Day.",
        "genres": [
            "Action",
            "Drama",
            "History"
        ],
        "runtime": 705,
        "poster": "https://m.media-amazon.com/images/M/MV5BMTI3ODc2ODc0M15BMl5BanBnXkFtZTYwMjgzNjc3._V1_SY1000_SX677_AL_.jpg",
        "title": "Band of Brothers",
        "released": "2001-09-09 00:00:00",
        "year": 2001,
        "imdb": {
            "rating": 9.6,
            "votes": 183802,
            "id": 185906
        },
        "poster_path": "/9z36SDiSdsHk2GjbZ1MjqGsag6p.jpg",
        "backdrop_path": "/nCsKxSNONvUYEi1AXRXRmq6MWUb.jpg"
    }
    ]

def test_top_series_with_count0():
    response = client.get(
        "/top_series/?count=0"
    )
    assert response.status_code == 200
    assert response.json()==[]

def test_top_series_with_count_less_0():
    response = client.get(
        "/top_series/?count=-1"
    )
    assert response.status_code == 200
    assert response.json()==[]


def comments_of_a_movie():
    response = client.get(
        f"/movies/{movie_id}/comments"
    )
    assert response.status_code == 200
    assert response.json()==[
    {
        "_id": "6601e68009297414fe9074b0",
        "name": "warror",
        "email": "warror@example.com",
        "movie_id": "573a1390f29313caabcd587d",
        "text": "Great Movie",
        "date": "2024-03-26 02:32:56"
    },
    {
        "_id": "5a9427648b0beebeb6957a38",
        "name": "Yara Greyjoy",
        "email": "gemma_whelan@gameofthron.es",
        "movie_id": "573a1390f29313caabcd587d",
        "text": "Nobis incidunt ea tempore cupiditate sint. Itaque beatae hic ut quis.",
        "date": "2012-11-26 11:00:57"
    }
]
def comments_of_a_movie_with_count():
    response = client.get(
        f"/movies/{movie_id}/comments/?count=1"
    )
    assert response.status_code == 200
    assert response.json()==[
    {
        "_id": "6601e68009297414fe9074b0",
        "name": "warror",
        "email": "warror@example.com",
        "movie_id": "573a1390f29313caabcd587d",
        "text": "Great Movie",
        "date": "2024-03-26 02:32:56"
    }
]

def comments_of_a_movie_with_count_0():
    response = client.get(
        f"/movies/{movie_id}/comments/?count=0"
    )
    assert response.status_code == 200
    assert response.json()==[] 

def comments_of_a_movie_with_count_less_0():
    response = client.get(
        f"/movies/{movie_id}/comments/?count=-1"
    )
    assert response.status_code == 200
    assert response.json()==[]


def comments_of_a_movies_unmatched_id():
    response = client.get(
        f"/movies/{unmatched_movie_id}/comments"
    )
    assert response.status_code == 200
    assert response.json()==[]


def comments_of_a_movies_invalid_id():
    response = client.get(
        f"/movies/{invalid_movie_id}/comments"
    )
    assert response.status_code == 500
    assert response.json()=={
    "detail": "'573a190f19313caabcd587d' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string"
}

def test_related_movies():
    response = client.get(
        f"/movies/{movie_id}/related_movies"
    )
    assert response.status_code == 200
    assert response.json()==[
    {
        "_id": "573a1393f29313caabcdc4a8",
        "plot": "After being released from prison, notorious thief Roy Earle is hired by his old boss to help a group of inexperienced criminals plan and carry out the robbery of a California resort.",
        "genres": [
            "Adventure",
            "Crime",
            "Drama"
        ],
        "runtime": 100,
        "poster": "https://m.media-amazon.com/images/M/MV5BYTRhN2I1NGYtM2NlMC00MmNlLTlhYWQtNzA1YjM4ZTQ3NTJjXkEyXkFqcGdeQXVyMDQ2Njk1Ng@@._V1_SY1000_SX677_AL_.jpg",
        "title": "High Sierra",
        "fullplot": "Roy 'Mad Dog' Earle is broken out of prison by an old associate who wants him to help with an upcoming robbery. When the robbery goes wrong and a man is shot and killed Earle is forced to go on the run, and with the police and an angry press hot on his tail he eventually takes refuge among the peaks of the Sierra Nevadas, where a tense siege ensues. But will the Police make him regret the attachments he formed with two women during the brief planning of the robbery.",
        "languages": [
            "English"
        ],
        "released": "1941-01-25 00:00:00",
        "year": 1941,
        "imdb": {
            "rating": 7.6,
            "votes": 10801,
            "id": 33717
        },
        "poster_path": "/fkP6yy25Wja6Sn3AIlZ4F1BWsy0.jpg",
        "backdrop_path": "/6AcvQvapwSI0fw2j9fVUxMOkwNB.jpg",
        "title_similarity": 0.0,
        "languages_intersection": 1,
        "genre_intersection": 2,
        "cast_intersection": 0,
        "director_intersection": 1,
        "region_intersection": 1,
        "relevance_score1": 0.0014500473484848485,
        "relevance_score": 223.3000946969697
    },
    {
        "_id": "573a1392f29313caabcd980d",
        "plot": "A young hoodlum rises up through the ranks of the Chicago underworld, even as a gangster's accidental death threatens to spark a bloody mob war.",
        "genres": [
            "Crime",
            "Drama"
        ],
        "runtime": 83,
        "poster": "https://m.media-amazon.com/images/M/MV5BZmJhZTU2NjEtZWM4MC00ZWU3LWEyOWUtMDgxNzI4ZTllYjcwXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_SY1000_SX677_AL_.jpg",
        "title": "The Public Enemy",
        "fullplot": "Tom Powers and Matt Doyle are best friends and fellow gangsters, their lives frowned upon by Tom's straight laced brother, Mike, and Matt's straight laced sister, Molly. From their teen-aged years into young adulthood, Tom and Matt have an increasingly lucrative life, bootlegging during the Prohibition era. But Tom in particular becomes more and more brazen in what he is willing to do, and becomes more obstinate and violent against those who either disagree with him or cross him. When one of their colleagues dies in a freak accident, a rival bootlegging faction senses weakness among Tom and Matt's gang, which is led by Paddy Ryan. A gang war ensues, resulting in Paddy suggesting that Tom and Matt lay low. But because of Tom's basic nature, he decides instead to take matters into his own hands.",
        "languages": [
            "English"
        ],
        "released": "1931-04-23 00:00:00",
        "year": 1931,
        "imdb": {
            "rating": 7.8,
            "votes": 12384,
            "id": 22286
        },
        "poster_path": "/vVxdaRMprQO2DM4AFyJ6C4qZSFO.jpg",
        "backdrop_path": "/oXLaGV0VOqQhXdUmQpm6KGsSpu1.jpg",
        "title_similarity": 0.0,
        "languages_intersection": 1,
        "genre_intersection": 2,
        "cast_intersection": 0,
        "director_intersection": 0,
        "region_intersection": 1,
        "relevance_score1": 0.0032913669064748197,
        "relevance_score": 201.78273381294963
    },
    {
        "_id": "573a1392f29313caabcd9ca6",
        "plot": "An ambitious and near insanely violent gangster climbs the ladder of success in the mob, but his weaknesses prove to be his downfall.",
        "genres": [
            "Action",
            "Crime",
            "Drama"
        ],
        "runtime": 93,
        "poster": "https://m.media-amazon.com/images/M/MV5BYmMxZTU2ZDUtM2Y1MS00ZWFmLWJlN2UtNzI0OTJiOTYzMTk3XkEyXkFqcGdeQXVyMjUxODE0MDY@._V1_SY1000_SX677_AL_.jpg",
        "title": "Scarface",
        "fullplot": "Johnny Lovo rises to the head of the bootlegging crime syndicate on the south side of Chicago following the murder of former head, Big Louis Costillo. Johnny contracted Big Louis' bodyguard, Tony Camonte, to make the hit on his boss. Tony becomes Johnny's second in command. Johnny is not averse to killing anyone who gets in his and Johnny's way. As Tony is thinking bigger than Johnny and is not afraid of anyone or anything, Tony increasingly makes decisions on his own instead of following Johnny's orders, especially in not treading on the north side run by an Irish gang led by a man named O'Hara, of whom Johnny is afraid. Tony's murder spree increases, he taking out anyone who stands in his and Johnny's way of absolute control on the south side, and in Tony's view absolute control of the entire city. Tony's actions place an unspoken strain between Tony and Johnny to the point of the two knowing that they can't exist in their idealized world with the other. Tony's ultimate downfall may be one of two women in his life: Poppy, Johnny's girlfriend to who Tony is attracted; and Tony's eighteen year old sister, Cesca, who is self-professed to be older mentally than her years much to Tony's chagrin, he who will do anything to protect her innocence. Cesca ultimately comes to the realization that she is a lot more similar to her brother than she first imagined.",
        "languages": [
            "English"
        ],
        "released": "1932-04-09 00:00:00",
        "year": 1932,
        "imdb": {
            "rating": 7.8,
            "votes": 18334,
            "id": 23427
        },
        "poster_path": "/iQ5ztdjvteGeboxtmRdXEChJOHh.jpg",
        "backdrop_path": "/sctvs9cUwJD15qlTlrsh2BXsK75.jpg",
        "title_similarity": 0.0,
        "languages_intersection": 1,
        "genre_intersection": 2,
        "cast_intersection": 0,
        "director_intersection": 0,
        "region_intersection": 1,
        "relevance_score1": 0.002831816179709293,
        "relevance_score": 199.86363235941857
    },
    {
        "_id": "573a1391f29313caabcd935e",
        "plot": "Rico is a small-time hood who knocks off gas stations for whatever he can take. He heads east and signs up with Sam Vettori's mob. A New Year's Eve robbery at Little Arnie Lorch's casino ...",
        "genres": [
            "Crime",
            "Drama",
            "Film-Noir"
        ],
        "runtime": 79,
        "poster": "https://m.media-amazon.com/images/M/MV5BYzE4ZTI3MDQtMTE5MS00MzQxLTkwZGMtYWM5MjU2MzE3OTk5XkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_SY1000_SX677_AL_.jpg",
        "title": "Little Caesar",
        "fullplot": "Rico is a small-time hood who knocks off gas stations for whatever he can take. He heads east and signs up with Sam Vettori's mob. A New Year's Eve robbery at Little Arnie Lorch's casino results in the death of the new crime commissioner Alvin McClure. Rico's good friend Joe Massara, who works at the club as a professional dancer, works as the gang's lookout man and wants out of the gang. Rico is ambitious and eventually takes over Vettori's gang; he then moves up to the next echelon pushing out Diamond Pete Montana. When he orders Joe to dump his girlfriend Olga and re-join the gang, Olga decides there's only one way out for them.",
        "languages": [
            "English"
        ],
        "released": "1931-01-25 00:00:00",
        "year": 1931,
        "imdb": {
            "rating": 7.4,
            "votes": 8049,
            "id": 21079
        },
        "poster_path": "/1K3Q1tAHHA5Sdtja2pPALBQevA7.jpg",
        "backdrop_path": "/8i8Epd76HEX5ZAqbG1QboRFiiJm.jpg",
        "title_similarity": 0.0,
        "languages_intersection": 1,
        "genre_intersection": 2,
        "cast_intersection": 0,
        "director_intersection": 0,
        "region_intersection": 1,
        "relevance_score1": 0.0030935613682092564,
        "relevance_score": 199.7871227364185
    },
    {
        "_id": "573a1392f29313caabcda0a5",
        "plot": "Queen Christina of Sweden is a popular monarch who is loyal to her country. However, when she falls in love with a Spanish envoy, she must choose between the throne and the man she loves.",
        "genres": [
            "Biography",
            "Drama",
            "History"
        ],
        "runtime": 99,
        "poster": "https://m.media-amazon.com/images/M/MV5BMjIyMjg1ODk4OF5BMl5BanBnXkFtZTgwNDA0NzkxMjE@._V1_SY1000_SX677_AL_.jpg",
        "title": "Queen Christina",
        "fullplot": "Queen Christina of Sweden is a dominant European ruler in the 17th century, and has never thought of romance. However, she accidentally and secretly falls in love with an emissary from Spain, even though a marriage between the two seems out of the question.",
        "languages": [
            "English",
            "Spanish"
        ],
        "released": "1934-02-09 00:00:00",
        "year": 1933,
        "imdb": {
            "rating": 7.9,
            "votes": 5260,
            "id": 24481
        },
        "poster_path": "/lGGYwoBp21CzF7cMzNPcOr6i6iw.jpg",
        "backdrop_path": "/1aIOpvWDAd6zrJ31Dw88U5ALWT0.jpg",
        "title_similarity": 0.0,
        "languages_intersection": 1,
        "genre_intersection": 2,
        "cast_intersection": 0,
        "director_intersection": 0,
        "region_intersection": 1,
        "relevance_score1": 0.0006178331356267299,
        "relevance_score": 194.83566627125344
    },
    {
        "_id": "573a1391f29313caabcd8e8f",
        "plot": "Prime Minister of Great Britain Benjamin Disraeli outwits the subterfuge of the Russians and chicanery at home in order to secure the purchase of the Suez Canal.",
        "genres": [
            "Biography",
            "Drama",
            "History"
        ],
        "runtime": 90,
        "poster": "https://m.media-amazon.com/images/M/MV5BMTc1NTAxOTExMV5BMl5BanBnXkFtZTgwMDk1MjgwMjE@._V1_SY1000_SX677_AL_.jpg",
        "title": "Disraeli",
        "fullplot": "Biopic of the famed British Prime Minister focusing on his concern about Russia's growing interest in the Indian subcontinent and his attempts to buy the Suez Canal. He sees the Canal as the key strategic resource in maintaining the Empire in the East but is unpopular in many quarters. With antisemitism rife at the time, Disraeli finds little support for his plan to purchase the canal or his foreign policy in general. There is no doubt that the Russians are plotting against British interests and he is surrounded by spies, even in his office at 10 Downing St. When the Bank of England refuses to finance the purchase of the available shares he turns to private sources to raise the available cash only to find the conspirators one step ahead of him.",
        "languages": [
            "English"
        ],
        "released": "1929-11-01 00:00:00",
        "year": 1929,
        "imdb": {
            "rating": 6.5,
            "votes": 694,
            "id": 19823
        },
        "poster_path": "/eVJpfh42k1SXkwyAQGzEdM3xSvf.jpg",
        "backdrop_path": "/lAhQmZJkcL3CjIyfzA3cDQeOLo.jpg",
        "title_similarity": 0.0,
        "languages_intersection": 1,
        "genre_intersection": 2,
        "cast_intersection": 0,
        "director_intersection": 0,
        "region_intersection": 1,
        "relevance_score1": 0.0013326226012793177,
        "relevance_score": 194.66524520255862
    },
    {
        "_id": "573a1392f29313caabcda224",
        "plot": "Elizabeth Barrett's tyrannical father has forbidden any of his family to marry. Nevertheless, Elizabeth falls in love with the poet Robert Browning.",
        "genres": [
            "Biography",
            "Drama",
            "Romance"
        ],
        "runtime": 109,
        "poster": "https://m.media-amazon.com/images/M/MV5BY2Q4ZDBkMzEtNWM4ZC00MDRjLWIwNDItZTNkYWZjOGE5MjYwXkEyXkFqcGdeQXVyMDI2NDg0NQ@@._V1_SY1000_SX677_AL_.jpg",
        "title": "The Barretts of Wimpole Street",
        "fullplot": "In 1845 London, the Barrett family is ruled with an iron fist by its stern widowed patriarch, Edward Moulton-Barrett. His nine grown children are afraid of him more than they love him. One of his rules is that none of his children are allowed to marry, which does not sit well with youngest daughter Henrietta as she loves and wants to marry Captain Surtees Cook. Of the nine, the one exception is his daughter Elizabeth, who abides faithfully to her father's wishes. Elizabeth does not think too much about the non-marriage rule as she has an unknown chronic illness which has kept her bedridden. She feels her life will not be a long one. With her time, she writes poetry, which she shares by correspondence with another young poet, Robert Browning. Elizabeth's outlook on her life changes when she meets Mr. Browning for the first time, he who has fallen in love with her without even having met her. She, in return, falls in love with him after their meeting. With Mr. Browning's love and support, Elizabeth tries to get well and enjoy life, this all against the thoughts of her father, who physically and emotionally traps Elizabeth and by association all of his children, all in the name of protecting her and them in the name of God.",
        "languages": [
            "English"
        ],
        "released": "1934-09-21 00:00:00",
        "year": 1934,
        "imdb": {
            "rating": 7.1,
            "votes": 1003,
            "id": 24865
        },
        "poster_path": "/u0RVhFCtUXsHO7s3F7K3208BAJs.jpg",
        "backdrop_path": "/lLmI59EA1gYKuOLVIHt1n7N0CnN.jpg",
        "title_similarity": 0.0,
        "languages_intersection": 1,
        "genre_intersection": 2,
        "cast_intersection": 0,
        "director_intersection": 0,
        "region_intersection": 1,
        "relevance_score1": 0.0021044923495635434,
        "relevance_score": 193.6089846991271
    },
    {
        "_id": "573a1392f29313caabcdb5a9",
        "plot": "A priest tries to stop a gangster from corrupting a group of street kids.",
        "genres": [
            "Crime",
            "Drama",
            "Film-Noir"
        ],
        "runtime": 97,
        "poster": "https://m.media-amazon.com/images/M/MV5BY2JhZmJmOTQtMjg5Ni00N2M4LTlkNDAtOTc0ZGQ2MTJhNDM4XkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_SY1000_SX677_AL_.jpg",
        "title": "Angels with Dirty Faces",
        "fullplot": "Rocky Sullivan and Jerry Connolly were tough kids who grew up together in the toughest part of New York --- Hell's Kitchen. Early on, Rocky gets sent to reform school, where he learns how to be a first class criminal. Jerry, who had escaped from the law, goes straight and becomes a priest. As adults, they reunite in the old neighborhood: Jerry works with the kids who, like he and Rocky, could end up on either side of the law. Rocky has returned looking for a safe place to stay till he can get back into his old racketeering organization -- something that his old partner isn't anxious to have happen. Lots of rapid fire wisecracks, roughhousing and gunfire ensues.",
        "languages": [
            "English"
        ],
        "released": "1938-11-26 00:00:00",
        "year": 1938,
        "imdb": {
            "rating": 8.0,
            "votes": 15019,
            "id": 29870
        },
        "poster_path": "/k23E4UAcow8eczLRmVCMdukL4Mx.jpg",
        "backdrop_path": "/bb36aEZwEvK2L01mgWQuC506CZg.jpg",
        "title_similarity": 0.0,
        "languages_intersection": 1,
        "genre_intersection": 2,
        "cast_intersection": 0,
        "director_intersection": 0,
        "region_intersection": 1,
        "relevance_score1": 0.0015358854437323172,
        "relevance_score": 192.07177088746462
    },
    {
        "_id": "573a1392f29313caabcdb7c1",
        "plot": "The tragic life of Marie Antoinette, who became queen of France in her late teens.",
        "genres": [
            "Biography",
            "Drama",
            "History"
        ],
        "runtime": 149,
        "poster": "https://m.media-amazon.com/images/M/MV5BNjM4NjQzNTQzM15BMl5BanBnXkFtZTgwOTI0MDgyMTE@._V1_SY1000_SX677_AL_.jpg",
        "title": "Marie Antoinette",
        "fullplot": "The life of Marie Antoinette (1755-1793) from betrothal and marriage in 1770 to her beheading. At first, she's a Hapsburg teenager isolated in France, living a virgin's life in the household of the Dauphin, a shy solitary man who would like to be a locksmith. Marie discovers high society, with the help of Orleans and her brothers-in-law. Her foolishness is at its height when she meets a Swedish count, Axel de Fersen. He helps her see her fecklessness. In the second half of the film, she avoids an annulment, becomes queen, bears children, and is a responsible ruler. The affair of the necklace and the general poverty of France feed revolution. She faces death with dignity.",
        "languages": [
            "English"
        ],
        "released": "1938-08-26 00:00:00",
        "year": 1938,
        "imdb": {
            "rating": 7.6,
            "votes": 1988,
            "id": 30418
        },
        "poster_path": "/cybXGmv8Rjd5Os8Xml6YxMBQ0Zt.jpg",
        "backdrop_path": "/hlbRkinr9YcC3UOc871Df5zu9Ly.jpg",
        "title_similarity": 0.0,
        "languages_intersection": 1,
        "genre_intersection": 2,
        "cast_intersection": 0,
        "director_intersection": 0,
        "region_intersection": 1,
        "relevance_score1": 0.0022171442687747038,
        "relevance_score": 191.8342885375494
    },
    {
        "_id": "573a1392f29313caabcdb5fc",
        "plot": "Against all odds Father Flanagan starts \"Boys' Town\" after hearing a convict's story. Whitey Marsh comes there. He runs away but, hungry, returns. He runs away again but, when friend Pee ...",
        "genres": [
            "Biography",
            "Drama"
        ],
        "runtime": 96,
        "poster": "https://m.media-amazon.com/images/M/MV5BMWUwMWRmYTYtY2Q2MS00ZTRlLTljNjQtNzlkMmRjNjllNjNlXkEyXkFqcGdeQXVyMjUxODE0MDY@._V1_SY1000_SX677_AL_.jpg",
        "title": "Boys Town",
        "fullplot": "Against all odds Father Flanagan starts \"Boys' Town\" after hearing a convict's story. Whitey Marsh comes there. He runs away but, hungry, returns. He runs away again but, when friend Pee Wee is hit by a car, returns. He runs away and joins his brother's gang. Flanagan and the boys capture the crooks and the reward saves the town.",
        "languages": [
            "English",
            "Hebrew"
        ],
        "released": "1938-09-09 00:00:00",
        "year": 1938,
        "imdb": {
            "rating": 7.3,
            "votes": 3715,
            "id": 29942
        },
        "poster_path": "/jGwKOZvPItNSocHFAg1USbhKR6c.jpg",
        "backdrop_path": "/pvvUqgvDXu8aLd5VqgrfOccnrnP.jpg",
        "title_similarity": 0.0,
        "languages_intersection": 1,
        "genre_intersection": 2,
        "cast_intersection": 0,
        "director_intersection": 0,
        "region_intersection": 1,
        "relevance_score1": 0.0028020113897976495,
        "relevance_score": 191.8040227795953
    }
]
    
def test_related_movies_with_count():
    response = client.get(
        f"/movies/{movie_id}/related_movies/?count=1"
    )
    assert response.status_code == 200
    assert response.json()==[
    {
        "_id": "573a1393f29313caabcdc4a8",
        "plot": "After being released from prison, notorious thief Roy Earle is hired by his old boss to help a group of inexperienced criminals plan and carry out the robbery of a California resort.",
        "genres": [
            "Adventure",
            "Crime",
            "Drama"
        ],
        "runtime": 100,
        "poster": "https://m.media-amazon.com/images/M/MV5BYTRhN2I1NGYtM2NlMC00MmNlLTlhYWQtNzA1YjM4ZTQ3NTJjXkEyXkFqcGdeQXVyMDQ2Njk1Ng@@._V1_SY1000_SX677_AL_.jpg",
        "title": "High Sierra",
        "fullplot": "Roy 'Mad Dog' Earle is broken out of prison by an old associate who wants him to help with an upcoming robbery. When the robbery goes wrong and a man is shot and killed Earle is forced to go on the run, and with the police and an angry press hot on his tail he eventually takes refuge among the peaks of the Sierra Nevadas, where a tense siege ensues. But will the Police make him regret the attachments he formed with two women during the brief planning of the robbery.",
        "languages": [
            "English"
        ],
        "released": "1941-01-25 00:00:00",
        "year": 1941,
        "imdb": {
            "rating": 7.6,
            "votes": 10801,
            "id": 33717
        },
        "poster_path": "/fkP6yy25Wja6Sn3AIlZ4F1BWsy0.jpg",
        "backdrop_path": "/6AcvQvapwSI0fw2j9fVUxMOkwNB.jpg",
        "title_similarity": 0.0,
        "languages_intersection": 1,
        "genre_intersection": 2,
        "cast_intersection": 0,
        "director_intersection": 1,
        "region_intersection": 1,
        "relevance_score1": 0.0014500473484848485,
        "relevance_score": 223.3000946969697
    }
]
    
def test_related_movies_with_count_0():
    response = client.get(
        f"/movies/{movie_id}/related_movies/?count=0"
    )
    assert response.status_code == 500
    assert response.json()=={
    "detail": "the limit must be positive, full error: {'ok': 0.0, 'errmsg': 'the limit must be positive', 'code': 15958, 'codeName': 'Location15958', '$clusterTime': {'clusterTime': Timestamp(1711481716, 8), 'signature': {'hash': b'\\x8b9\\x7fl\\xe6\\\\\\x95D\\xd2\\xfd\\x8b0\\xef\\x0f\\xcbR\\xe0 \\xd7\\xd2', 'keyId': 7286942330160939011}}, 'operationTime': Timestamp(1711481716, 8)}"
}

def test_related_movies_with_count_less_0():
    response = client.get(
        f"/movies/{movie_id}/related_movies/?count=-1"
    )
    assert response.status_code == 500
    assert response.json()=={
    "detail": "the limit must be positive, full error: {'ok': 0.0, 'errmsg': 'the limit must be positive', 'code': 15958, 'codeName': 'Location15958', '$clusterTime': {'clusterTime': Timestamp(1711481716, 8), 'signature': {'hash': b'\\x8b9\\x7fl\\xe6\\\\\\x95D\\xd2\\xfd\\x8b0\\xef\\x0f\\xcbR\\xe0 \\xd7\\xd2', 'keyId': 7286942330160939011}}, 'operationTime': Timestamp(1711481716, 8)}"
}

def test_related_movies_invalid_id():
    response = client.get(
        f"/movies/{invalid_movie_id}/related_movies"
    )
    assert response.status_code == 500
    assert response.json()=={
    "detail": "'abcd' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string"
}
    
def test_related_movies_unmatched_id():
    response = client.get(
        f"/movies/{unmatched_movie_id}/related_movies"
    )
    assert response.status_code == 200
    assert response.json()==[]