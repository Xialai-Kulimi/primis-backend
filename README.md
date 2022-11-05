# primis-backend

## dev
```
uvicorn backend.main:app --reload
```

## src
```
----backend
    |   dependencies.py
    |   __main__.py
    |   __init__.py
    |
    |
    +---routers
    |       auth.py
    |       entity.py
    |       ws.py
    |       __init__.py
    |
    \---utils
            console.py
            mongo.py
```