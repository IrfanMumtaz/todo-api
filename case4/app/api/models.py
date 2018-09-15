import os, sys
absFilePath = os.path.abspath(__file__) 
fileDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(fileDir) 
projectDIR = os.path.dirname(parentDir) 
sys.path.append(projectDIR) 
from app import app
from .routes import db

class ToDo(db.Model):
    __tablename__ = 'todo'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    status = db.Column(db.String())
    created_at = db.Column(db.String())
    updated_at = db.Column(db.String())

    def __init__(self, title, status, created_at, updated_at):
        self.title = title
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<id {}>'.format(self.id)

class UltimateTodo(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String())
    password = db.Column(db.String())
    email = db.Column(db.String())
    age = db.Column(db.String())
    gender = db.Column(db.String())
    joiningdate = db.Column(db.String())

    def __init__(self, userName, password, email, age, gender, joiningdate):
        self.userName = userName
        self.password = password
        self.email = email
        self.age = age
        self.gender = gender
        self.joiningdate = joiningdate

    def __repr__(self):
        return '<id {}>'.format(self.id)