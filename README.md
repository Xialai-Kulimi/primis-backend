# primis-backend

## dev
```
uvicorn backend.main:app --reload
```

## src
```
----backend
    |   dependencies.py
    |   main.py
    |   __init__.py
    |
    +---internal
    |       chat.py
    |       __init__.py
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