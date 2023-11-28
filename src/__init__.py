import os
from flask import Flask,jsonify
from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

#set config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

# instantiate the db
db = SQLAlchemy(app)

app.config.from_object('src.config.DevelopmentConfig')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128),nullable=False)
    email = db.Column(db.String(128),nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

class Ping(Resource):
    def get(self):
        return{
            'status': 'success',
            'message': 'pong!'
        }
        
api.add_resource(Ping,'/ping')
        