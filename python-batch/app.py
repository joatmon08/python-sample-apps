from flask import Flask
from flask import request
from flask import jsonify
import json
import logging

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({'Hello': 'World!'})

@app.route('/payload/send', methods=['POST'])
def payload_send():
    return jsonify({'size': len(request.get_data())})

@app.route('/payload/receive', methods=['POST'])
def payload_receive():
    with open('q42.json', 'r') as f:
        data = f.read()
        app.logger.info("Data Length: %d", len(data))
        return jsonify(json.loads(data))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
