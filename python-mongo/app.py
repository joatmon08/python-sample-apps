from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import os
import logging

app = Flask(__name__)
try:
    app.config['MONGO_DBNAME'] = os.environ['DB_NAME']
    app.config['MONGO_URI'] = os.environ['DB_URI']
    app.config['APP_PORT'] = int(os.getenv('APP_PORT', 80))
except Exception as e:
    logging.error(e)

mongo = PyMongo(app)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/star', methods=['GET'])
def get_all_stars():
  star = mongo.db.stars
  output = []
  for s in star.find():
      output.append({'name' : s['name'], 'distance' : s['distance']})
  return jsonify({'result' : output})

@app.route('/star', methods=['POST'])
def add_star():
    star = mongo.db.stars
    name = request.json['name']
    distance = request.json['distance']
    star_id = star.insert({'name': name, 'distance': distance})
    new_star = star.find_one({'_id': star_id })
    output = {'name' : new_star['name'], 'distance' : new_star['distance']}
    return jsonify({'result' : output})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=app.config['APP_PORT'], debug=True)
