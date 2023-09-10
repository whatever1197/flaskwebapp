# Übernommen aus den Beispielen
from app import db, app, login
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import base64
from hashlib import md5

import os


class Users(UserMixin, db.Model):
    ID_User = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(64), index=True, unique=True)
    Password = db.Column(db.String(128))
    API_Token = db.Column(db.String(32), unique=True)
    API_Expiration = db.Column(db.DateTime)
    Models = db.relationship('Models', backref='User', lazy='dynamic')

    @login.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    # Übernommen aus den Beispielen
    def set_password(self, password):
        self.Password = generate_password_hash(password)

    # Übernommen aus den Beispielen
    def check_password(self, password):
        return check_password_hash(self.Password, password)
    
    def get_id(self):
        return (self.ID_User)

    def all_models(self):
        models = Models.query.all()
        return models
   
    def json_one(self):
        returndata = {
            'ID_User': self.ID_User,
            'Username': self.Username,
            'Models': self.Models.count(),
        }

        return(returndata)

    # Übernommen aus den Beispielen
    def json_all():
        users = Users.query.all()
        returndata = {
            'users': [user.json_one() for user in users]
        }

        return(returndata)
    
    # Übernommen aus den Beispielen
    def get_token(self):
        now = datetime.utcnow()
        self.API_Token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.API_Expiration = now + timedelta(days=1)
        db.session.add(self)
        db.session.commit()
        return self.API_Token

    # Übernommen aus den Beispielen
    @staticmethod
    def check_token(token):
        user = Users.query.filter_by(API_Token=token).first()
        if user is None or user.API_Expiration < datetime.utcnow():
            return None
        return user



class Models(db.Model):
    ID_Model = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(64), unique=True)
    Description = db.Column(db.String(1024))
    Status = db.Column(db.String(16))
    Quality = db.Column(db.String(16))
    Timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    User_ID = db.Column(db.Integer, db.ForeignKey(Users.ID_User))

    def json_one(self):
        returndata = {
            'ID_Model': self.ID_Model,
            'Name': self.Name,
            'Description': self.Description,
            'Status': self.Status,
            'Quality': self.Quality,
            'Timestamp': self.Timestamp,
            'User': self.User.Username
        }

        return(returndata)

    def json_all():
        models = Models.query.all()
        returndata = {
            'models': [model.json_one() for model in models]
        }

        return(returndata)