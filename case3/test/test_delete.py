import unittest
import os
import sys, json
absFilePath = os.path.abspath(__file__) 
fileDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(fileDir) 
sys.path.append(parentDir) 
from app import app


class DeleteData(unittest.TestCase):


    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
 
        self.assertEquals(app.debug, False)

    def tearDown(self):
        pass

    def test_post_delete(self):
        response = self.app.delete('/api/v1.0/task/5b755f8ca71a621d4450b368')
        self.assertEqual(response.status_code,200 )

    def test_post_delete_invalid(self):
        response = self.app.post('/api/v1.0/task/5b755f8ca71a621d4450b368')
        self.assertEqual(response.status_code,204 )

 
 
if __name__ == "__main__":
    unittest.main()