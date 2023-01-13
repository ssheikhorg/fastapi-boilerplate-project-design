# fastapi-boilerplate-project-design

## 1. Project Structure

```bash
├── LICENSE
├── main.py
├── README.md
├── requirements.txt
└── src
    ├── apps
    │   └── __init__.py
    ├── app.py
    ├── auth
    │   ├── auth_bearer.py
    │   └── __init__.py
    └── core
        ├── cache
        │   ├── backend.py
        │   ├── base.py
        │   ├── __init__.py
        │   ├── redis.py
        │   └── utils.py
        ├── cipher.py
        ├── config.py
        ├── database
        │   ├── __init__.py
        │   └── mongo_client.py
        ├── error
        │   ├── http_error.py
        │   ├── __init__.py
        │   └── validation_error.py
        ├── __init__.py
        ├── middlewares
        │   ├── __init__.py
        │   └── throttler.py
        └── utils
            ├── base_response.py
            ├── events.py
            ├── helpers.py
            ├── __init__.py
            └── serializers.py
```

## Can be used as a template for Python, FastAPI, MongoDB, Redis
