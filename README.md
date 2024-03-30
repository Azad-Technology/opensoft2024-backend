<br/>
<br/>
<h1 align="center">OPEN SOFT 2024 BACKEND</h1>

## Project Structure

The project is structured as follows, ensuring modular and organized management of various functionalities:
Backends:
```
project_root
│
├── src
│   ├── routers
│   │   └── auth.py
|   |   └── cast.py
|   |   └── countries.py
|   |   └── genre.py
|   |   └── movie.py
|   |   └── recommendation.py
|   |   └── search.py
|   |   └── user.py
|   ├── utils
|   |   └── recommend.py
|   ├── cache_system.py
│   ├── config.py
│   ├── db.py
│   ├── main.py
│   ├── __init__.py
│   └── schemas.py
├── .env
├── .env.example
├── .gitignore
├── README.md
├── ATLAS.md
├── tfidf_vectorizer.pkl
├── vercel.json
└── requirements.txt
```
```
project_root
│
├── src
│   ├── routers
│   │   └── embeddings.py
|   ├── utils
|   |   └── nlp.py
|   |   └── ada_embedder.py
|   ├── cache_system.py
│   ├── config.py
│   ├── db.py
│   ├── main.py
│   ├── __init__.py
│   └── schemas.py
├── .env
├── .env.example
├── .gitignore
└── requirements.txt
```

<br />
<br />

<h2> Setup and Installation</h2>
<h3>Environment Formation</h3>
<ol>
    <li>
        <strong>Clone The repo</strong>:
        <pre><code>git clone <Git Repo Link> </code></pre>
    </li>
</ol>
<h3>Environment Formation</h3>
<ol>
    <li>
        <strong>Make env folder</strong>:
        <pre><code>python -m venv env</code></pre>
        <p>This will make an env folder.</p>
    </li>
    <li>
        <strong>Activate environment</strong>:
        <pre><code>source env/bin/activate #For Linux
source env/Scripts/activate #For Windows on Git Bash</code></pre>
        <p>This will activate the env folder.</p>
    </li>
</ol>
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
          <li><code>MONGO_INITDB_DATABASE</code>: Input the connection URI for your MongoDB Instance</li>
          <li><code>JWT_KEY</code>: Enter a secure key for encoding and decoding JSON Web Tokens.</li>
          <li><code>CORS_ORIGIN</code>: Define the allowed origins for Cross-Origin Resource Sharing. Use * for allowing all origins in a development environment.</li>  
          <li><code>DATABASE_URL</code>: Input the connection URI for your MongoDB Instance</li> 
          <li><code>REDIS_URL</code>: Input the connection URI for your Redis Instance</li> 
          <li><code>REDIS_PORT</code>: Input the connection URI for your MongoDB Instance</li> 
          <li><code>LS_SIGNING_SECRET</code>: Enter a secure key for Lemon Squeezy.</li> 
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

## API Structures
<h3>Backends</h3>
<ol>
    <li>
        <link>https://lb.popkorn.tech/docs</link>
    </li>
    <li>
        <link>https://embed.popkorn.tech/docs</link>
    </li>
</ol>

## Tech Stacks Used
<h3>Tech Stacks Used are:</h3>
<ol>
    <li>
        <p>FastAPI</p>
    </li>
    <li>
        <p>MongoDB</p>
    </li>
    <li>
        <p>Redis</p>
    </li>
    <li>
        <p>Google API</p>
    </li>
</ol>
