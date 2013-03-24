from flask import Flask, request, render_template
from bson.json_util import dumps
import pymongo
import datetime

config = {
    'app': {
        'title': 'Chat',
        'description': 'Simple chat using Flask and MongoDB'
    },
    'mongodb': {
        'host': '127.0.0.1', 
        'port': 27017, 
        'db': 'chat'
    }
}

con = pymongo.Connection(config['mongodb']['host'], config['mongodb']['port'])
db = con[config['mongodb']['db']]
messages = db['messages']

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', data = config['app'])

@app.route('/messages.json')
def all():
    total = messages.count()
    limit = 50
    if (total > limit):
        skip = total - limit;
        all = messages.find().limit(limit).skip(skip)
    else:
        all = messages.find()

    return dumps(all)

@app.route('/messages/add', methods=['POST'])
def add():
    username = request.form['username']
    message = request.form['message']

    if (username and message):
        obj = messages.insert({'username': username, 'message': message, 'timestamp': datetime.datetime.now()})
        return dumps({'status': 'ok', 'obj': obj})

    return dumps({'status': 'error'})

if __name__ == '__main__':
    app.run(debug=True)
