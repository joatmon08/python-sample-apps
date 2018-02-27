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

class StarError(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv = self.message
        return rv


class StarHealthStatus():
    def __init__(self):
        self.database = 'connected'
    
    def check_database(self):
        try:
            mongo.db.stars.find()
        except Exception as e:
            logging.error(e)
            self.database = 'disconnected'

@app.errorhandler(StarError)
def handle_distance_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/star/health')
def health():
    health_status = StarHealthStatus()
    health_status.check_database()
    if 'disconnected' in health_status.database:
        raise StarError(health_status.__dict__, status_code=500)
    return jsonify(health_status.__dict__)


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
