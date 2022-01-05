## User and Media APIs

* Authentication

POST > http://127.0.0.1:8000/user/auth

#### Request body

```json
{
    "email": "admin@gmail.com"
}
```

#### Response body

```json
{
    "success": true,
    "email": "admin@gmail.com",
    "token": "e36bec45b6c9facdf2d8319a4354698a0c4a7fb7"
}
```

#### Exception

```json
{
    "success": false
}
```

* Media


GET > http://127.0.0.1:8000/user/media

#### Response body

```json
{
    "success": true,
    "music": [
        {
            "id": 2,
            "category": "Criminal",
            "title": "Test-music-1"
        }
    ],
    "movie": [
        {
            "id": 2,
            "category": "Criminal",
            "title": "Test-movie-1"
        }
    ]
}
```

#### Exception

```json
{
    "success": false,
    "music": [],
    "movie": []
}
```

