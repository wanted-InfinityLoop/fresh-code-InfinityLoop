import json
import jwt
from datetime import datetime, timedelta

from django.test import TestCase, Client

from users.models import User, Role
from my_settings  import MY_SECRET_KEY

class LogInTest(TestCase):
    def setUp(self):
        admin    = Role.objects.create(name="ADMIN")
        customer = Role.objects.create(name="CUSTOMER")

        user_1 = User.objects.create(
            email    = "abc@gmail.com",
            password = "abcd1234!@",
            name     = "songTest",
            role     = customer
        )

        user_2 = User.objects.create(
            email    = "qwerty@gmail.com",
            password = "abcd1234!@",
            name     = "songTest",
            role     = admin
        )

        self.access_token_1 = jwt.encode({
            "id"   : user_1.id,
            "role" : user_1.role.id,
            "exp"  : datetime.utcnow() + timedelta(seconds=120)
        }, MY_SECRET_KEY, algorithm="HS256")

        self.access_token_2 = jwt.encode({
            "id"   : user_2.id,
            "role" : user_2.role.id,
            "exp"  : datetime.utcnow() + timedelta(seconds=120)
        }, MY_SECRET_KEY, algorithm="HS256")

        self.invalid_token = jwt.encode({
            "id"   : user_1.id,
            "role" : 5,
            "exp"  : datetime.utcnow() + timedelta(seconds=120)
        }, MY_SECRET_KEY, algorithm="HS256")

    def tearDown(self):
        User.objects.all().delete()
        Role.objects.all().delete()

    def test_loginview_success(self):
        client     = Client()
        login_data = {
            "email"    : "abc@gmail.com",
            "password" : "abcd1234!@"
        }
        response = client.post('/users/sign-in', json.dumps(login_data), content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{
            "message": "SUCCESS", "token": self.access_token_1
        })

    def test_loginview_key_error(self):
        client     = Client()
        login_data = {
            "emai"     : "abc@gmail.com",
            "password" : "abcd1234!@"
        }
        response = client.post('/users/sign-in', json.dumps(login_data), content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{
            "message": "KEY ERROR"
        })

    def test_loginview_type_error(self):
        client     = Client()
        login_data = {
            "email"    : 1,
            "password" : "abcd1234!@"
        }
        response = client.post('/users/sign-in', json.dumps(login_data), content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{
            "message": "Not Allowed Type"
        })

    def test_loginview_validate_email(self):
        client     = Client()
        login_data = {
            "email"    : "dfdfl",
            "password" : "abcd1234!@"
        }
        response = client.post('/users/sign-in', json.dumps(login_data), content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{
            "message": "Email Unvalid"
        })

    def test_loginview_user_not_exist(self):
        client     = Client()
        login_data = {
            "email"    : "abcde123@gmail.com",
            "password" : "abcd1234!@"
        }
        response = client.post('/users/sign-in', json.dumps(login_data), content_type = 'application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),{
            "message": "User Not Found"
        })

    def test_loginview_password_not_equal(self):
        client     = Client()
        login_data = {
            "email"    : "abc@gmail.com",
            "password" : "a!@bcd1234"
        }
        response = client.post('/users/sign-in', json.dumps(login_data), content_type = 'application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),{
            "message": "Log In Failed"
        })

    def test_loginview_password_not_equal(self):
        client     = Client()
        login_data = {
            "email"    : "abc@gmail.com",
            "password" : "a!@bcd1234"
        }
        response = client.post('/users/sign-in', json.dumps(login_data), content_type = 'application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),{
            "message": "Log In Failed"
        })