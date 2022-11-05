# primis-backend

## dev
```
uvicorn backend.__main__:app --reload
```

## src
```
----backend
    |   dependencies.py
    |   __main__.py
    |   __init__.py
    |
    +---routers
    |       entity.py
    |       ws.py
    |       __init__.py
    |
    \---utils
            console.py
            mongo.py
```
