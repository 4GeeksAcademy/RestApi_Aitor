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
from models import db, Users, People, Planets, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)




# Obtener Users________________________________________

@app.route('/users', methods=['GET'])
def get_users():
    users = Users.query.all()
    return jsonify([user.serialize() for user in users])

# Agregar favorito________________________________________

@app.route('/favorites', methods=['POST'])
def add_favorite():
    user_id = request.json.get('user_id')
    planet_id = request.json.get('planet_id')
    people_id = request.json.get('people_id')

    new_favorite = Favorites(user_id=user_id, planet_id=planet_id, people_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 201

if __name__ == '__main__':
    app.run(debug=True)

# Obtener favoritos Users________________________________________

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = Users.query.get(user_id)
    if user is None:
        return jsonify({"msg": "Usuario no encontrado"}), 404
    return jsonify([favorite.serialize() for favorite in user.favorites])

# Obtener la lista de personas________________________________________

@app.route('/people', methods=['GET'])
def get_people():
    data = People.query.all()
    people_list = [el.serialize() for el in data]
    return jsonify(people_list), 200


# Obtener una persona específica por su ID______________________

@app.route('/people/<int:id>', methods=['GET'])
def get_person(id):
    data = People.query.get(id)
    if not data:
        return jsonify({"error": "Persona no encontrada"}), 404
    
    return jsonify(data.serialize()), 200



# Añadir una nueva persona_______________________________________

@app.route('/newpeople', methods=['POST'])
def new_person():
    try:
        data = request.json
        
        new_person = People(
            name=data['name'], 
            lastname=data['lastname'],
            side=data['side']
        )
        db.session.add(new_person)
        db.session.commit()
        return jsonify({"message": "Personaje Creado"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400



# Eliminar una persona___________________________________________

@app.route('/deletepeople/<int:id>', methods=['DELETE'])
def delete_person(id):
    try:
        data = People.query.get(id)
        if data is None:
            return jsonify({"error": "No se encontró la persona"}), 404
        
        db.session.delete(data)
        db.session.commit()
        return jsonify({"message": "Persona eliminada"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    

# Obtener lista de planetas___________________________________________

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    return jsonify([planet.serialize() for planet in planets])


# Obtener planeta por id___________________________________________

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({"msg": "Planeta no encontrado"}), 404
    return jsonify(planet.serialize())

# Añadir un nuevo planeta___________________________________________

@app.route('/planets', methods=['POST'])
def add_planet():
    name = request.json.get('name')
    terrain = request.json.get('terrain')
    population = request.json.get('population')
    galaxy = request.json.get('galaxy')

    if not name or not terrain or not population or not galaxy:
        return jsonify({"msg": "Añade todos los campos"}), 400

    new_planet = Planets(name=name, terrain=terrain, population=population, galaxy=galaxy)
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 201

# Eliminar un planeta___________________________________________

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({"msg": "Planeta no encontrado"}), 404

    db.session.delete(planet)
    db.session.commit()
    return jsonify({"msg": "Planeta Eliminado"}), 200

if __name__ == '__main__':
    app.run(debug=True)



@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
