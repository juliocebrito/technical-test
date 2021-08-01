from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongodb:27017/test_db"
mongo = PyMongo(app)

@app.route('/')
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/create-user', methods=['POST'])
def create_user():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    id = mongo.db.testuser.insert(
        {'username':'username', 'password':'password', 'email':'email'}
    )
    return {'id': str(id), 'username':username, 'password':password, 'email':email}

@app.route('/list-users', methods=['GET'])
def users():
    users = mongo.db.testuser.find()
    return Response(json_util.dumps(users), mimetype='application/json')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)