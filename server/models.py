from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import Schema, fields

from config import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique=True, nullable = False)
    _password_hash = db.Column(db.String)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)

    @hybrid_property
    def password_hash(self):
        raise AttributeError('Passwords may not be viewed')
    
    @password_hash.seeter
    def password_hash(self,password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self,password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))
    
    def __repr__(self):
        return f'<User {self.username}, {self.image_url}, {self.bio}>'
    

class Recipe(db.Model):
    __tablename__ = 'recipes'
    
    pass

class UserSchema(Schema):
    pass

class RecipeSchema(Schema):
    pass