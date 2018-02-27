from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import os
import logging
import requests

headers = {'Content-Type': 'application/json'}

app = Flask(__name__)
try:
    app.config['STARS_ENDPOINT'] = os.environ['STARS_ENDPOINT']
    app.config['MONGO_URI'] = os.environ['DB_URI']
    app.config['MONGO_DBNAME'] = os.environ['DB_NAME']
except Exception as e:
    logging.error(e)

mongo = PyMongo(app)


class DistanceError(Exception):
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

class DistanceHealthStatus():
    def __init__(self):
        self.database = 'connected'
        self.stars = 'connected'

    def check_stars(self):
        try: 
            r = requests.get(app.config['STARS_ENDPOINT']) 
        except requests.exceptions.ConnectionError as e:
            logging.error(e)
            self.stars = 'disconnected'
    
    def check_database(self):
        try:
            mongo.db.stars.find()
        except Exception as e:
            logging.error(e)
            self.database = 'disconnected'


@app.errorhandler(DistanceError)
def handle_distance_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/')
def index():
    return 'Get sum of all distances with /distance.'

@app.route('/distance/health')
def health():
    health_status = DistanceHealthStatus()
    health_status.check_database()
    health_status.check_stars()
    if 'disconnected' in health_status.stars:
        raise DistanceError(health_status.__dict__, status_code=500)
    return jsonify(health_status.__dict__)

@app.route('/distance')
def sum_distance():
    r = requests.get(app.config['STARS_ENDPOINT'] + '/star')
    data = r.json()
    stars = data['result']
    print(stars)
    r.raise_for_status()
    if len(stars) == 0:
        return jsonify({'result' : 0})
    distances = [star['distance'] for star in stars]
    sum_distance = sum(distances)
    return jsonify({'result' : sum_distance})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.getenv('APP_PORT', 80)), debug=True)
