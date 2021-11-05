from jwt import exceptions, decode

from django.http import JsonResponse

from my_settings import MY_SECRET_KEY
from users.models import User, Role


def authorizer(func):
    def wrapper(self, request, *args, **kwagrs):
        try:
            access_token = request.headers.get("Authorization")
            
            if not access_token:
                return JsonResponse({"message": "Not Found Access_token"}, status = 403)
            
            payload = decode(access_token, MY_SECRET_KEY, algorithm="HS256")
            user_id = payload["id"]
            role_id = payload["role"]

            user = User.objects.get_or_none(id=user_id)

            if not user:
                return JsonResponse({"message": "User Not Found"}, status = 404)

            if user.role_id != role_id:
                return JsonResponse({"message": "Invalid User"}, status = 401)

            request.user = user
            request.role = role_id

        except exceptions.DecodeError:
            return JsonResponse({"message": "Invalid Token"}, status = 403)

        except exceptions.ExpiredSignatureError:
            return JsonResponse({"message": "Token Expired"}, status = 403)

        return func(self, request, *args, **kwagrs)

    return wrapper

        

        

        