# Technical Test

Docker
- docker-compose up


Endpoints

- [ POST ] /create-user
```javascript
{
    "user_id": "105398891",
    "pin": 2090,
    "balance": 0
}
```
- [ GET ] /list-users

- [ GET ] /detail-users/{id}

- [ PUT ] /update-users/{id}
```javascript
{
    "user_id": "105398891",
    "pin": 2090,
    "balance": 0
}
```
- [ DELETE ] /delete-users/{id}

- [ POST ] /process-file

DATA FILE PATH
- upload/data.json

TEST
- command: python -m unittest test