# primis-backend

## dev
```
uvicorn backend.__main__:app --reload --port 8000
```

## src
```
----backend
    |   dependencies.py
    |   __main__.py
    |   __init__.py
    |
    +---routers
    |       ws.py
    |       __init__.py
    |
    \---utils
            console.py
            mongo.py
```

## .env

```
GLOBAL_DB_CONNECT=
GAME_DB_CONNECT=
REDIS_PORT=
OAUTH2_CLIENT_ID=
OAUTH2_CLIENT_SECRET=
OAUTH2_REDIRECT_URI=
CONTROLLER_PATH=
```