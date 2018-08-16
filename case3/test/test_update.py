import unittest
import os
import sys, json
absFilePath = os.path.abspath(__file__) 
fileDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(fileDir) 
sys.path.append(parentDir) 
from app import app


class UpdateData(unittest.TestCase):


    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
 
        self.assertEquals(app.debug, False)

    def tearDown(self):
        pass

    def test_post_update(self):
        response = self.app.post('/api/v1.0/task/5b755f8ca71a621d4450b368',
                        data=json.dumps(dict(status='changed')),
                       content_type='application/json')
        self.assertEqual(response.status_code,200 )

    def test_post_without_json(self):
        response = self.app.post('/api/v1.0/task/5b755f8ca71a621d4450b368')
        self.assertEqual(response.status_code,400 )

    def test_post_invalid_key(self):
        response = self.app.post('/api/v1.0/task/5b755f8ca71a621d4450b361',
                        data=json.dumps(dict(status='changed')),
                       content_type='application/json')
        self.assertEqual(response.status_code,204 )
 
 
if __name__ == "__main__":
    unittest.main()