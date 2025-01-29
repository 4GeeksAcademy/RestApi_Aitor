from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#TABLA USERS ______________________________________________________

class Users (db.Model):
    
   class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    favorites = db.relationship('Favorites', backref='users', lazy=True)

    def __repr__(self):
        return f'<Users {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "favorites": [favorite.serialize() for favorite in self.favorites]
        }


#TABLA PEOPLE ______________________________________________________

class People (db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    lastname = db.Column(db.String(150), nullable=False)
    side = db.Column(db.String(150), nullable=False)
    favorites = db.relationship('Favorites', backref='people', lazy=True)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "side": self.side
        }
    

#TABLA PLANETAS ______________________________________________________

class Planets (db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    terrain = db.Column(db.String(150), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    galaxy = db.Column(db.String(150), nullable=False)
    favorites = db.relationship('Favorites', backref='planets', lazy=True)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            "population": self.population,
            "galaxy": self.galaxy
        }
    
    
# TABLA FAVORITES ______________________________________________________

class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)

    def __repr__(self):
        return f'<Favorites {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "people_id": self.people_id
        }