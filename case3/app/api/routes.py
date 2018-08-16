from flask import Blueprint, request, jsonify, redirect, url_for
from flask_pymongo import PyMongo, pymongo
from bson.json_util import dumps, ObjectId
import os, sys, json, time
absFilePath = os.path.abspath(__file__) 
fileDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(fileDir) 
sys.path.append(parentDir) 
from app import app

mod = Blueprint('api', __name__)

mongo = PyMongo(app)


@mod.route('/tasks')
def tasks():

    #get all tasks
    _tasks = mongo.db.tasks.find().sort('created_at', pymongo.DESCENDING)

    tasks = []

    #iterate tasks
    for task in _tasks:
        id = json.loads(dumps(task['_id']))

        #append data in list
        tasks.append({
            '_id': id["$oid"],
            'task': task['task'],
            'status': task['status'],
            'created_at': task['created_at'],
            'updated_at': task['updated_at'],
        })
    return jsonify({"result": tasks}), 200

@mod.route('/task/<id>', methods=['POST', 'GET', 'DELETE'])
def task(id):
    #get data from database
    db = mongo.db.tasks
    _task = db.find_one({'_id': ObjectId(id)})

    if(_task is None):
        return jsonify({"result": "oopsss data not found"}), 204

    if request.method == 'POST':
        if (request.data):
        
            #get data from json request
            task = request.get_json(silent=True)

            #iterate data and verify give json keys
            for t in task:
                if(t in _task):
                    _task[t] = task[t]
            
            _task['updated_at'] = time.strftime('%d-%m-%Y %H:%M:%S')

            #save updated data
            db.save(_task)
            if(id):
                _task = db.find_one({'_id': ObjectId(id)})
                id = json.loads(dumps(_task['_id']))

                #iterate data and key
                task = {
                    '_id': id["$oid"],
                    'task': _task['task'],
                    'status': _task['status'],
                    'created_at': _task['created_at'],
                    'updated_at': _task['updated_at'],
                }
                return jsonify({"result": task}), 200
            else:
                return jsonify({"result": "oopss something went wrong!!"}), 102
        else:
            return jsonify({"result": "Bad request, request must contain json data"}), 400


    elif request.method == 'DELETE':
        #remove data
        result = db.remove(_task)
        if(result):
            return jsonify({"result": "Data Successfully Deleted"}), 200
        else:
            return jsonify({"result": "oopss something went wrong!!"}), 102

        
    else:
        #convert json object into dictionary
        id = json.loads(dumps(_task['_id']))

        #iterate data and key
        task = {
            '_id': id["$oid"],
            'task': _task['task'],
            'status': _task['status'],
            'created_at': _task['created_at'],
            'updated_at': _task['updated_at'],
        }
        return jsonify({"result": task}), 200
        
@mod.route('/task', methods=["POST"])
def create_taks():
    db = mongo.db.tasks

    #get data from json request
    _data = request.get_json(silent=True)

    if (request.data):

        #validate task key is avaialable or not
        if "task" in _data :
            #store everything in a dictionary
            data = {
                'task': _data['task'],
                'status': "view",
                'created_at': time.strftime('%d-%m-%Y %H:%M:%S'),
                'updated_at': time.strftime('%d-%m-%Y %H:%M:%S'),
            }

            #insert data and get key
            id = db.insert(data)

            #if key is valid get data
            if(id):
                _task = db.find_one({'_id': ObjectId(id)})
                id = json.loads(dumps(_task['_id']))

                #iterate data and key
                task = {
                    '_id': id["$oid"],
                    'task': _task['task'],
                    'status': _task['status'],
                    'created_at': _task['created_at'],
                    'updated_at': _task['updated_at'],
                }
                return jsonify({"result": task}), 200
            else:
                return jsonify({"result": "oopss something went wrong!!"}), 102
        else:
            return jsonify({"result": "task can not be null"}), 400
    else:
        return jsonify({"result": "Bad request, request must contain json data"}), 400