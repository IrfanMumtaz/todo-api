from flask import Blueprint


mod = Blueprint('api', __name__)

@mod.route('/tasks')
def tasks():
    return '{"tasks": "this is first task"}'