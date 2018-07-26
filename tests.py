import unittest
import json
from api import create_app
from api.models import db


class UserTestCase(unittest.TestCase):
    """This class represents the user test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user = {'name': 'Test user', 'email': 'test2@test.com',
                     'password': '123', 'gender': 'male'}

        self.userweight = {'weight': 80.0}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_user_creation(self):
        res = self.client().post('/user/signup/', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('User created successfully!', str(res.data))

    def test_api_can_get_all_users(self):
        res = self.client().post('/user/signup/', data=self.user)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/user/')
        self.assertEqual(res.status_code, 200)

    def test_api_can_get_user_by_id(self):
        res = self.client().post('/user/signup/', data=self.user)
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        result = self.client().post('/user/', data={'user_id': int(result_in_json['user_id'])})
        self.assertEqual(result.status_code, 200)

    def test_user_can_be_edited(self):
        res = self.client().post(
            '/user/signup/',
            data=self.user)
        self.assertEqual(res.status_code, 201)
        res = self.client().put(
            '/user/1',
            data={
                "name": "John"
            })
        self.assertEqual(res.status_code, 200)

    def test_user_deletion(self):
        res = self.client().post(
            '/user/signup/',
            data=self.user)
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/user/1')
        self.assertEqual(res.status_code, 200)

    def test_create_weight(self):
        res = self.client().post('/user/signup/', data=self.user)
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        result = self.client().post('/userweight/', data={'weight': 89, 'user_id':int(result_in_json['user_id'])})
        self.assertEqual(result.status_code, 201)

    def test_get_user_weight(self):
        res = self.client().post('/user/signup/', data=self.user)
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        result = self.client().post('/userweight/', data={'weight': 89, 'user_id':int(result_in_json['user_id'])})
        self.assertEqual(result.status_code, 201)
        weights = self.client().get('/user/{}/weight'.format(int(result_in_json['user_id'])))
        self.assertEqual(weights.status_code, 200)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()