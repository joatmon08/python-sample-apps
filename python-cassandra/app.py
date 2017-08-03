from flask import Flask, jsonify, request
from cassandra.cluster import Cluster
import os
import logging

STAR_ROUTE = '/stars'
GALAXY_ROUTE = '/galaxies'

app = Flask(__name__)
cluster = None
session = None
try:
    cluster = Cluster([os.environ['CLUSTER_ADDRESS']], port=9042)
    session = cluster.connect(os.getenv('CLUSTER_KEYSPACE', 'mycluster'))
except Exception as e:
    logging.error(e)


@app.route(STAR_ROUTE, methods=['GET'])
def get_all_stars():
    rows = session.execute('SELECT name, distance FROM stars')
    output = []
    for row in rows:
        output.append({'name': row.name, 'distance': row.distance})
    return jsonify({'result': output})


@app.route(STAR_ROUTE, methods=['POST'])
def add_star():
    session.execute(
        """
        INSERT INTO stars (name, distance)
        VALUES (%s, %s)
        IF NOT EXISTS
        """,
        (request.json['name'], request.json['distance'])
    )
    return jsonify({'result': request.json})


@app.route(GALAXY_ROUTE, methods=['GET'])
def get_all_galaxies():
    rows = session.execute('SELECT name, data FROM galaxies')
    output = []
    for row in rows:
        output.append({'name': row.name, 'data': row.data})
    return jsonify({'result': output})


@app.route(GALAXY_ROUTE, methods=['POST'])
def add_galaxy():
    with open(request.json['data'], 'r') as f:
        data_blob = bytearray(f.read())
    session.execute(
        """
        INSERT INTO galaxies (name, data)
        VALUES (%s, %s)
        """,
        (request.json['name'], data_blob)
    )
    rows = session.execute('SELECT * FROM galaxies WHERE name=%s', [request.json['name']])
    return jsonify({'name': rows[0][0]})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
