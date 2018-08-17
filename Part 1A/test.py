import unittest
from app import app
class TestApp(unittest.TestCase):


    def setUp(self):
        app.config['TESTING']=True
        self.app=app.test_client()



    def tearDown(self):
        pass


    def test_api_get(self):
         response =self.app.get('/api/v1.0/todo')
         self.assertEqual(response.status_code, 200)
    def test_api_getsearch(self):
        response=self.app.get('/api/v1.0/todo/5')
    def test_api_post(self):
        response=self.app.post('/api/v1.0/todo', content_type='application/json')
        self.assertEqual(response.status_code , 200)
    def test_api_delete(self):
        response=self.app.delete('/api/v1.0/todo/1')
        self.assertEqual(response.status_code , 200)
    def test_api_update(self):
        response=self.app.put('/api/v1.0/todo/4')
        self.assertEqual(response.status_code , 200)



if __name__=="__main__":
    unittest.main()