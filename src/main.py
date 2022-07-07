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
from models import db, User, Character, Planet, FavoriteCharacter, FavoritePlanet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# class Starwars:
#     all_starwars = []

#     def __init__(self, content):
#         self.id = len(self.__class__.all_starwars) + 1
#         self.content = content
#         self.date = datetime.utcnow
#         self.__class__.all_starwars.append(self)

#     def serialize(self):
#         return {
#             "id": self.id,
#             "content": self.content,
#         }

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def list_user():
    users = User.query.all()
    user_map = list(map(
        lambda user: user.serialize(),
        users
    ))
    return jsonify(user_map), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def user_unique(user_id):
    user = User.query.filter_by(id=character_id).one_or_none()  
    
    return jsonify(user.serialize()), 200

@app.route('/characters', methods=['GET'])
def list_character():
    charracters = Character.query.all()
    charracters_map = list(map(
        lambda character: character.serialize(),
        charracters
    ))
    return jsonify(charracters_map), 200


@app.route('/characters/<int:character_id>', methods=['GET'])
def character_unique(character_id):
    character = Character.query.filter_by(id=character_id).one_or_none()  
    
    return jsonify(character.serialize()), 200


@app.route('/planets', methods=['GET'])
def list_planet():
    planets = Planet.query.all()
    planets_map = list(map(
        lambda planet: planet.serialize(),
        planets
    ))
    return jsonify(planets_map), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def planet_unique(planet_id):
    planet = Planet.query.filter_by(id=planet_id).one_or_none()  
    
    return jsonify(planet.serialize()), 200

@app.route('/favorites', methods=['GET'])
def favorites():
    favorites1 = FavoriteCharacter.query.all()
    favorites2 = FavoritePlanet.query.all()
    favorites2_map = list(map(
        lambda favorite2: favorite2.serialize(),
        favorites2
    ))
    favorites1_map = list(map(
        lambda favorite1: favorite1.serialize(),
        favorites1
    ))
    favorites_map = favorites1_map + favorites2_map

    return jsonify(favorites_map), 200

@app.route('/favorites/planets', methods=['GET'])
def favorite_planet():
    favorites_planet = FavoritePlanet.query.all()
    favorites_panets_map = list(map(
        lambda favorite: favorite.serialize(),
        favorites_planet
    ))

    return jsonify(favorites_panets_map), 200

@app.route('/favorites/characters', methods=['GET'])
def favorite_character():
    favorites_character = FavoriteCharacter.query.all()
    favorites_characters_map = list(map(
        lambda favorite: favorite.serialize(),
        favorites_character
    ))

    return jsonify(favorites_characters_map), 200
    
    

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
