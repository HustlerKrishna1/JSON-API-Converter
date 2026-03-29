# JSON → API Converter

Paste any JSON file → get a full REST API instantly.

## Setup

```bash
cd json-api
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

## Usage

### 1. Edit `data/db.json` directly
The default db.json contains `users` and `products`. On startup, the API auto-generates:

```
GET    /users          → list all users
GET    /users/{id}     → get one user
POST   /users          → create user
PUT    /users/{id}     → replace user
DELETE /users/{id}     → delete user

GET    /products       → list all products
...and so on for every collection
```

### 2. Upload a new JSON file via API

```bash
curl -X POST http://127.0.0.1:8000/upload \
  -F "file=@your_data.json"
```

The API hot-reloads with the new structure.

### 3. Interactive docs
Visit: http://127.0.0.1:8000/docs

## JSON Format

Root must be an object where array values become resources:

```json
{
  "users":    [{"name": "Krishn", "age": 20}],
  "products": [{"title": "Laptop", "price": 999}]
}
```

Each item gets a UUID `id` automatically on first access.
