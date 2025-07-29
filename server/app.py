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
    def get(self):
        if session.get('user_id'):
            user = User.query.filter(User.id == session['user_id']).first()
            return UserSchema().dump(user), 200
        else:
            return {"error": "User is not logged in"}, 401

class Login(Resource):
    def post(self):
        username = request.get_json()['username']
        password = request.get_json()['password']

        user = User.query.filter(User.username == username).first()

        if user and user.authenticate(password):
            session['user_id'] = user.id
            return UserSchema().dump(user), 200
        
        return {'error': '401 Unauthorized'}, 401
        

class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session['user_id'] = None
            return {}, 204
        return {"error": "User is already logged out" }, 401

class RecipeIndex(Resource):
    def get(self):
        if session.get('user_id'):
            recipes = [RecipeSchema().dump(recipe) for recipe in Recipe.query.all()]
            return recipes, 200
        else:
            return {"error": "User not logged in"}, 401
        
    def post(self):
        if session.get('user_id'):
            request_json = request.get_json()
            recipe = Recipe(
                title = request_json.get('title'),
                instructions = request_json.get('instructions'),
                minutes_to_complete = request_json.get('minutes_to_complete'),
                user_id = session['user_id']
            )
            
            try:
                db.session.add(recipe)
                db.session.commit()
                return RecipeSchema().dump(recipe),201
            except IntegrityError:
                return {'error': '422 Unprocessable Entity'}, 422
        else:
            return {"error": "User not logged in"}, 401

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)