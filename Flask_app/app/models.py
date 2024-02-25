from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def save(self):
        db.session.add(self)
        db.session.commit()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    base_exp = db.Column(db.String, nullable=False)
    base_hp = db.Column(db.String, nullable=False)
    base_attack = db.Column(db.String, nullable=False)
    base_defense = db.Column(db.String, nullable=False)
    ability = db.Column(db.String, nullable=False)
    sprite_url = db.Column(db.String, nullable=False)
    

    def __init__(self, name, ability, base_exp, base_hp, base_attack, base_defense, sprite_url):
        self.name = name 
        self.ability = ability
        self.base_exp = base_exp
        self.base_hp = base_hp
        self.base_attack = base_attack
        self.base_defense = base_defense
        self.sprite_url = sprite_url
        

    def save(self):
        db.session.add(self)
        db.session.commit()