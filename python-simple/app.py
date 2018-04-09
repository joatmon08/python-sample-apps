from flask import Flask
from flask import request
import os

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/another')
def test():
	user = request.args.get('user')
	return user + ' says Hello!'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv('APP_PORT', 80)), debug=True)
