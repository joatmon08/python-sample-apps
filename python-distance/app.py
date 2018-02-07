from flask import Flask, jsonify, request
import os
import logging

app = Flask(__name__)

@app.route('/')
def index():
    return 'From a distance...'

@app.route('/distance', methods=['POST'])
def sum_distance():
    stars = request.json
    if len(stars) == 0:
        return jsonify({'result' : 0})
    distances = [star['distance'] for star in stars]
    sum_distance = sum(distances)
    return jsonify({'result' : sum_distance})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
