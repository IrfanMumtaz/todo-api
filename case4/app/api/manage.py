import os, sys
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
absFilePath = os.path.abspath(__file__) 
fileDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(fileDir) 
projectDIR = os.path.dirname(parentDir) 
sys.path.append(projectDIR) 
from app import app
from models import db


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()