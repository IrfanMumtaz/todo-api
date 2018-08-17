import unittest
import os
import sys
absFilePath = os.path.abspath(__file__) 
fileDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(fileDir) 
sys.path.append(parentDir) 
from app import app


class GetData(unittest.TestCase):


    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
 
        self.assertEquals(app.debug, False)

    def tearDown(self):
        pass

    def test_geti_all(self):
        response = self.app.get('/api/v1.0/tasks')
        self.assertEqual(response.status_code,200 )

    def test_get_single_valid(self):
        response = self.app.get('/api/v1.0/task/5b755f8ca71a621d4450b368')
        self.assertEqual(response.status_code,200 )

    def test_get_single_invalid(self):
        response = self.app.get('/api/v1.0/task/5b755f8ca71a621d4450b361')
        self.assertEqual(response.status_code,204 )
 
 
if __name__ == "__main__":
    unittest.main()