INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
]

MIDDLEWARE = [
    ...
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Flutter web dev server (adjust if needed)
    "http://127.0.0.1:3000",
    "http://localhost:8000",  # If you are testing backend directly
]


