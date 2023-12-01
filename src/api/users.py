from flask import Blueprint, request
from flask_restx import Resource, Api, fields

from src import db
from src.api.models import User

users_blueprint = Blueprint('users', __name__) 
api = Api(users_blueprint) 

user = api.model('User', { 
    'id': fields.Integer(readOnly=True),
    'username': fields.String(required=True),
    'email': fields.String(required=True), 
    'created_date': fields.DateTime, 
})

class Users(Resource): 
    @api.marshal_with(user) 
    def get(self, user_id): 
        user = User.query.filter_by(id=user_id).first()
        if not user:
            api.abort(404, f"User {user_id} does not exist")
        return user, 200
    
    #delete CRUD
    #Delete user using id
    @api.expect(user)
    def delete(self,user_id):
        user = User.query.filter_by(id=user_id).first()
        email = user.email
        response_object = {} 
        if not user:
            api.abort(404, f"user {user_id} does not exist")
        db.session.delete(user)
        db.session.commit()
        
        response_object['message'] = f'{email} was deleted'
        return response_object, 200
    
    
    #update CRUD 
    #This function updates the username
    @api.expect(user)
    def put(self,user_id):
        update_data = request.get_json()
        user = User.query.filter_by(id=user_id).first()
        email = user.email
        response_object = {}
        username = update_data.get('username')
        if not user:
            api.abort(404, f"user {user_id} does not exist")
        if  not update_data:
            api.abort(400, f"Input payload validation failed")
            
        user.username = username
        print(user.username)
        db.session.commit()
        
        response_object['message'] = f'{email} info was updated'
        return response_object, 200
        
    
class UsersList(Resource):
    
    @api.expect(user, validate=True)   
    def post(self): 
        post_data = request.get_json() 
        username = post_data.get('username') 
        email = post_data.get('email')     
        response_object = {} 
        user = User.query.filter_by(email=email).first()
        if user:
            response_object['message'] = 'Sorry. That email already exists.'
            return response_object, 400
        
        db.session.add(User(username=username, email=email)) 
        db.session.commit() 
        
        response_object['message'] = f'{email} was added!'
        
        return response_object, 201 
    
    @api.marshal_with(user, as_list=True)
    def get(self):
        return User.query.all(), 200

  
    
    
    
    
api.add_resource(UsersList, '/users')
api.add_resource(Users, '/users/<int:user_id>')