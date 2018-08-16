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
    _tasks = mongo.db.tasks.find().sort('created_at', pymongo.DESCENDING)

    tasks = []
    for task in _tasks:
        id = json.loads(dumps(task['_id']))
        tasks.append({
            '_id': id["$oid"],
            'task': task['task'],
            'status': task['status'],
            'created_at': task['created_at'],
            'updated_at': task['updated_at'],
        })
    return jsonify({"result": tasks})

@mod.route('/task/<id>', methods=['POST', 'GET', 'DELETE'])
def task(id):
    #get data from database
    db = mongo.db.tasks
    _task = db.find_one({'_id': ObjectId(id)})

    if(_task is None):
        return jsonify({"result": "oopsss data not found"})

    if request.method == 'POST':
        
        #get data from json request
        task = request.get_json(silent=True)

        if(_task):
            #iterate data and verify give json keys
            for t in task:
                if(t in _task):
                    _task[t] = task[t]
            
            _task['updated_at'] = time.strftime('%d-%m-%Y %H:%M:%S')

            #save updated data
            db.save(_task)
            return redirect(url_for('api.task', id=id))
        else:
            return jsonify({"result": "not found"})


    elif request.method == 'DELETE':
        #remove data
        result = db.remove(_task)
        if(result):
            return jsonify({"result": "Data Successfully Deleted"})
        else:
            return jsonify({"result": "oopss something went wrong!!"})

        
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
        return jsonify({"result": task})
        
@mod.route('/task', methods=["POST"])
def create_taks():
    db = mongo.db.tasks

    _data = request.get_json(silent=True)

    if("task" in _data):
        data = {
            'task': _data['task'],
            'status': "view",
            'created_at': time.strftime('%d-%m-%Y %H:%M:%S'),
            'updated_at': time.strftime('%d-%m-%Y %H:%M:%S'),
        }
        id = db.insert(data)
        if(id):
            return redirect(url_for('api.task', id=id))
        else:
            return jsonify({"result": "oopss something went wrong!!"})
    else:
        return jsonify({"result": "task can not be null"})