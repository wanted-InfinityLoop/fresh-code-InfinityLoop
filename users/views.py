import json
import jwt
import requests
import bcrypt
from datetime import datetime, timedelta

from django.http         import JsonResponse

from rest_framework.views import APIView

from users.models    import User, Role
from core.validators import email_validator
from my_settings     import MY_SECRET_KEY

class LogInView(APIView):
    def post(self, request):
        data = json.loads(request.body)

        email    = data.get('email')
        password = data.get('password')

        if not email or not password:
            return JsonResponse({"message": "KEY ERROR"}, status = 400)

        if type(email) != str or  type(password) != str:
            return JsonResponse({"message": "Not Allowed Type"}, status = 400)
        
        if not email_validator(email):
            return JsonResponse({"message": "Email Unvalid"}, status = 400)

        user = User.objects.get_or_none(email = email)

        if not user:
            return JsonResponse({"message": "User Not Found"}, status = 404)

        if user.password != password:
            return JsonResponse({"message": "Log In Failed"}, status = 401)


        access_token = jwt.encode({
            'id' : user.id, 
            'role' : user.role_id, 
            'exp':datetime.utcnow() + timedelta(seconds=120)
            }, MY_SECRET_KEY, algorithm="HS256")

        return JsonResponse({"message": "SUCCESS", "token": access_token}, status = 200)
