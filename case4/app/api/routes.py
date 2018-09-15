from flask import Blueprint, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from bson.json_util import dumps, ObjectId
import os, sys, json, time
absFilePath = os.path.abspath(__file__) 
fileDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(fileDir) 
sys.path.append(parentDir) 
from app import app

mod = Blueprint('api', __name__)

db = SQLAlchemy(app)

from .models import ToDo, UltimateTodo



@mod.route('/tasks')
def tasks():

    #get all tasks
    _tasks = ToDo.query.all()
    #return _tasks.title
    # return dumps(_tasks[0].title)

    tasks = []

    #iterate tasks
    for task in _tasks:

        #append data in list
        tasks.append({
            'id': task.id,
            'task': task.title,
            'status': task.status,
            'created_at': task.created_at,
            'updated_at': task.updated_at,
        })
    return jsonify({"result": tasks}), 200



@mod.route('/task/<id>', methods=['POST', 'GET', 'DELETE'])
def task(id):
    #get data from database
    _task = ToDo.query.filter_by(id=id).first()


    if(_task is None):
        return jsonify({"result": "oopsss data not found"}), 204

    if request.method == 'POST':
        if (request.data):
        
            #get data from json request
            task = request.get_json(silent=True)

            #iterate data and verify give json keys
            if 'title' in task:
                _task.title=task['title']
            if 'status' in task:
                _task.status=task['status']
            
            _task.updated_at = time.strftime('%d-%m-%Y %H:%M:%S')

            #save updated data
            db.session.commit()
            
            return jsonify({"result": "Success"}), 200
            
        else:
            return jsonify({"result": "Bad request, request must contain json data"}), 400


    elif request.method == 'DELETE':
        #remove data
        db.session.delete(_task)
        db.session.commit()
        
        return jsonify({"result": "Data Successfully Deleted"}), 200

        
    else:
        #iterate data and key
        task = {
            'id': _task.id,
            'task': _task.title,
            'status': _task.status,
            'created_at': _task.created_at,
            'updated_at': _task.updated_at,
        }
        return jsonify({"result": task}), 200
        



@mod.route('/task', methods=["POST"])
def create_taks():

    #get data from json request
    _data = request.get_json(silent=True)

    if (request.data):

        #validate task key is avaialable or not
        if "title" in _data :
            #store everything in a dictionary
            todo = ToDo(
                _data['title'],
                "view",
                time.strftime('%d-%m-%Y %H:%M:%S'),
                time.strftime('%d-%m-%Y %H:%M:%S')
            )
            db.session.add(todo)
            db.session.commit()

            #if key is valid get data
            return jsonify({"result": "success"}), 200
        else:
            return jsonify({"result": "task can not be null"}), 400
    else:
        return jsonify({"result": "Bad request, request must contain json data"}), 400

@mod.route('/ultimate', methods=["POST"])
def ultimate_taks():

    #get data from json request
    _data = request.get_json(silent=True)

    if (request.data):

        #validate task key is avaialable or not
        if "username" in _data :
            #store everything in a dictionary
            todo = UltimateTodo(
                _data['username'],
                _data['password'],
                _data['email'],
                _data['age'],
                _data['gender'],
                time.strftime('%d-%m-%Y %H:%M:%S')
            )
            db.session.add(todo)
            db.session.commit()

            #if key is valid get data
            return jsonify({"result": "success"}), 200
        else:
            return jsonify({"result": "task can not be null"}), 400
    else:
        return jsonify({"result": "Bad request, request must contain json data"}), 400