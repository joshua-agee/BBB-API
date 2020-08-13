from flask import Flask, g, render_template, jsonify
from flask_cors import CORS
from flask_login import LoginManager

DEBUG = True
PORT = 8000

import models
from resources.recipes import recipe
from resources.users import user
from resources.comments import comment


login_manager = LoginManager()

app = Flask(__name__)

app.secret_key = "9bPX7bEpKpsFvjXQ"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

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

CORS(recipe, origins=["http://localhost:3000"], supports_credentials=True)
CORS(user, origins=["http://localhost:3000"], supports_credentials=True)
CORS(comment, origins=["http://localhost:3000"], supports_credentials=True)

app.register_blueprint(recipe, url_prefix="/recipes")
app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(comment, url_prefix="/comment")

@app.route("/")
def index():
    return jsonify(data={}, status={"code": 200, "message": "Hello World"})


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)