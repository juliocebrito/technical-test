# Technical Test

docker-compose up


endpoints

/create-user       (POST)
{
    "balance": "0",
    "id": "610787399f0f4b54371059b4",
    "pin": 2090,
    "user_id": "105398891"
}
/list-users        (GET)
/detail-users/<id> (GET)
/update-users/<id> (PUT)
{
        "user_id": "105398891",
        "pin": 2090,
        "balance": 0
}
/delete-users/<id> (DELETE)
/process-file      (POST)

FILE PATH
upload/data.json


TEST
command: python -m unittest test