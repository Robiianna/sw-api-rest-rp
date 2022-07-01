"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

class Starwars:
    all_starwars = []

    def __init__(self, content):
        self.id = len(self.__class__.all_starwars) + 1
        self.content = content
        self.date = datetime.utcnow
        self.__class__.all_starwars.append(self)

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
        }

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def user():
    response_body = {
        "mensaje": "hola usuario"
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def people():
    response_body = {
        "inicio": "hola people"
    }

    return jsonify(response_body), 200

# @app.route('/people/<int:id>', methods=['GET'])
# def people():
#     response_body = {
#         "msg": "Hello, people, "
#     }

#     return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def planets():
    response_body = {
        "mensaje": "hola planetas"
    }

    return jsonify(response_body), 200



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
