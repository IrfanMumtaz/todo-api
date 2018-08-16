import unittest
import os
import sys, json
absFilePath = os.path.abspath(__file__) 
fileDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(fileDir) 
sys.path.append(parentDir) 
from app import app


class CreateData(unittest.TestCase):


    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
 
        self.assertEquals(app.debug, False)

    def tearDown(self):
        pass

    def test_post_create(self):
        response = self.app.post('/api/v1.0/task',
                        data=json.dumps(dict(task='testing task')),
                       content_type='application/json')
        self.assertEqual(response.status_code,200 )

    def test_create_without_json(self):
        response = self.app.post('/api/v1.0/task')
        self.assertEqual(response.status_code,400 )

    def test_create_with_invalid_json(self):
        response = self.app.post('/api/v1.0/task',
                        data=json.dumps(dict(status='changed')),
                       content_type='application/json')
        self.assertEqual(response.status_code,400 )
 
 
if __name__ == "__main__":
    unittest.main()