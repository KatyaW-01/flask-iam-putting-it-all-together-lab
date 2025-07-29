#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe, UserSchema, RecipeSchema

class Signup(Resource):
    def post(self):
        user_request = request.get_json()
        username = user_request.get('username')
        password = user_request.get('password')
        image_url = user_request.get('image_url')
        bio = user_request.get('bio')

        user = User(username = username, image_url = image_url, bio = bio)
        user.password_hash = password
        try:
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            return UserSchema().dump(user), 201
        except IntegrityError:
           return {'error': '422 Unprocessable Entity'}, 422 

class CheckSession(Resource):
    pass

class Login(Resource):
    pass

class Logout(Resource):
    pass

class RecipeIndex(Resource):
    pass

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)