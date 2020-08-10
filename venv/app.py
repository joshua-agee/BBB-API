from flask import Flask, g

DEBUG = True
PORT = 8000

import models


app = Flask(__name__)


@app.before_request
def before_request();
    """connect to the db before each request"""
    g.db = models.db
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the db connection after each request"""
    g.db.close()
    return response

@app.route('/')
def index():
    return 'Hello There'


if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)