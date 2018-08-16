import unittest
import os
import sys
absFilePath = os.path.abspath(__file__) 
fileDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(fileDir) 
sys.path.append(parentDir) 
from app import app


class APITest(unittest.TestCase):


    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
 
        self.assertEquals(app.debug, False)

    def tearDown(self):
        pass

    def test_api_static(self):
        response = self.app.get('/api/v1.0/tasks')
        self.assertEqual(response.status,'200 OK' )
 
 
if __name__ == "__main__":
    unittest.main()