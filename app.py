import os
from flask import Flask, request, jsonify, Response, wrappers
from flask_pymongo import PyMongo
from bson import json_util, ObjectId
import json
from utils import trm
import time

UPLOAD_FOLDER = '/app/uploads'

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongodb:27017/test_db"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mongo = PyMongo(app)

def validate_account(func):
    """
    Decorator for validate user account
    """
    def wrapper(*args, **kwargs):
        user = mongo.db.users.find_one({'user_id': args[0].user_id, 'pin': args[0].pin})
        if user:
            return func(*args, **kwargs)
        else:
            raise Exception('User invalid')
    return wrapper

@app.route('/')
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/create-user', methods=['POST'])
def create_user():
    user_id = request.json['user_id']
    pin = request.json['pin']
    balance = request.json['balance']

    id = mongo.db.users.insert(
        {'user_id': user_id,
         'pin': pin,
         'balance': balance
        }
    )
    return jsonify({
        'id': str(id),
        'user_id': user_id, 
        'pin': pin,
        'balance': balance
        })

@app.route('/list-users', methods=['GET'])
def users():
    users = mongo.db.users.find()
    return Response(json_util.dumps(users), mimetype='application/json')

@app.route('/detail-users/<id>', methods=['GET'])
def detail_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    return Response(json_util.dumps(user), mimetype='application/json')

@app.route('/update-users/<id>', methods=['PUT'])
def update_user(id):
    user_id = request.json['user_id']
    pin = request.json['pin']
    balance = request.json['balance']
    mongo.db.users.update_one({'_id': ObjectId(id)}, 
        {'$set': {
        'user_id': user_id, 
        'pin': pin,
        'balance': balance
        }}
        )
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    return Response(json_util.dumps(user), mimetype='application/json')

@app.route('/delete-users/<id>', methods=['DELETE'])
def delete_user(id):
    user = mongo.db.users.delete_one({'_id': ObjectId(id)})
    return jsonify({'message': 'User was deleted successfully'})


# endpoint that allows you to upload a JSON file.

@app.route('/process-file', methods=['POST'])
def process_file():
    
    file = request.files['file']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    
    with open(os.path.join(app.config['UPLOAD_FOLDER'], file.filename), 'r') as f:
        data = json.load(f)

    if data:
        
        result = {}

        user_id = data['trigger']['params']['user_id']
        pin = data['trigger']['params']['pin']

        t = Transaction(user_id, pin)

        # validate_account = t.validate_account()
        get_account_balance = 0
        trm_today = float(json.dumps(trm(date=time.strftime('%Y-%m-%d'))))

        for step in data['steps']:
            deposit_money = 0
            withdraw_money = 0
            money = 0

            # if validate_account:

            if step['action'] == 'get_account_balance':
                get_account_balance = t.get_account_balance()

            elif step['action'] == 'deposit_money':
                money = step['params']['money']['value']
                deposit_money = t.deposit_money(money)

            elif step['action'] == 'withdraw_in_pesos':
                money = step['params']['money']['value']
                withdraw_money = t.withdraw_money_in_pesos(money)

            elif step['action'] == 'withdraw_in_dollars':
                money = step['params']['money']['value']
                withdraw_money = t.withdraw_money_in_dollars(money)

            result[step['id']] = {
                'action': step['action'],
                'trm': trm_today,
                # 'validate_account': validate_account,
                'balance': get_account_balance,
                'money' : money,
                'deposit_money': deposit_money,
                'withdraw_money': withdraw_money
                }

            print(result[step['id']])

            # else:
            #     raise Exception('User invalid')


        return jsonify({'message': 'File was received successfully', 
                        'filename': file.filename,
                        # 'data': json.loads(json.dumps(data)),
                        'result': result
                        })
    else:
        return jsonify({'message': 'File was not received'})


@app.errorhandler(404)
def not_found():
    return jsonify({'message': 'Resource Not Found' + request.url, 'status': 404})

class Transaction:
    TRM = float(trm(date=time.strftime('%Y-%m-%d')))

    def __init__(self, user_id, pin):
        self.user_id = user_id
        self.pin = pin
        self.balance = self.get_account_balance()

    # def validate_account(self):
    #     user = mongo.db.users.find_one({'user_id': self.user_id, 'pin': self.pin})
    #     return True if user else False

    @validate_account
    def get_account_balance(self):
        user = mongo.db.users.find_one({'user_id': self.user_id, 'pin': self.pin})
        return float(user['balance'])

    @validate_account
    def deposit_money(self, money):
        balance = self.balance
        result = balance + float(money)
        mongo.db.users.update_one({'user_id': self.user_id, 'pin': self.pin}, 
        {'$set': {
        'balance': result
        }}
        )
        return result

    @validate_account
    def withdraw_money_in_pesos(self, money):
        balance = self.balance
        if balance and balance >= money:
            result = balance - float(money)
            mongo.db.users.update_one({'user_id': self.user_id, 'pin': self.pin}, 
            {'$set': {
            'balance': result
            }}
            )
        else:
            result = f'insufficient funds: {balance}'
        return result

    @validate_account
    def withdraw_money_in_dollars(self, money):
        balance = self.balance
        if balance and balance >= float(money * self.TRM):
            result = balance - float(money * self.TRM)
            mongo.db.users.update_one({'user_id': self.user_id, 'pin': self.pin}, 
            {'$set': {
            'balance': result
            }}
            )
        else:
            result = f'insufficient funds: {balance}'
        return result

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)