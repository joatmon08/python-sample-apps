from flask import Flask, jsonify, request
import os
import logging
import requests

headers = {'Content-Type': 'application/json'}

app = Flask(__name__)
try:
    app.config['STARS_ENDPOINT'] = os.environ['STARS_ENDPOINT']
    app.config['APP_PORT'] = int(os.getenv('APP_PORT', 80))
except Exception as e:
    logging.error(e)

@app.route('/')
def index():
    return 'From a distance...'

@app.route('/health')
def health():
    r = requests.get(app.config['STARS_ENDPOINT'])
    if r.status_code > 499:
        return jsonify({'stars': 'unhealthy'})
    return jsonify({'stars': 'healthy'})

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
    app.run(host="0.0.0.0", port=app.config['APP_PORT'], debug=True)
