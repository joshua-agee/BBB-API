from flask import Flask, g, render_template, jsonify
from flask_cors import CORS
from flask_login import LoginManager

DEBUG = True
PORT = 8000

import models
from resources.recipes import recipe

app = Flask(__name__)


@app.before_request
def before_request():
    """connect to the db before each request"""
    g.db = models.db
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the db connection after each request"""
    g.db.close()
    return response

CORS(recipe, origins=['http://localhost:3000'], supports_credentials=True)


app.register_blueprint(recipe, url_prefix='/recipe')


@app.route('/')
def index():
    return 'Hello There'


if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)