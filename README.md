# feedbook
feedbook is a RSS feed aggregator. <br />

## Features
- Authentication & Authorization user
- Support following multiple feeds & rss links
- Bookmark feeds


##  Technologies
- [FastAPI](https://fastapi.tiangolo.com/)
- [sqlalchemy](sqlalchemy.org)
- [pydantic](https://docs.pydantic.dev/latest/)
- [postgresql](https://www.postgresql.org/)
- pytest
- [docker](https://www.docker.com/)


## APIs

Register user
```
POST /auth/login
```

Login user
```
POST /auth/register
```

Get User feeds
```
GET /users/{user_id}/feeds
```

Get User sources
```
GET /users/{user_id}/sources
```

Add User source
```
POST /users/{user_id}/sources
```

Get User bookmarks
```
GET /users/{user_id}/bookmarks
```

Add User bookmark
```
POST /users/{user_id}/bookmark
```

# Run
Just run a simple docker compose.
```
git clone https://github.com/mo1ein/feedbook.git
cd feedbook
docker compose build
docker compose up -d
```
Then, enjoy the app! [http://127.0.0.1:8500/docs#/](http://127.0.0.1:8500/docs#/)
