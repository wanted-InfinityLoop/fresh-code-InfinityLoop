import json

from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.http import JsonResponse
from django.views import View
from django.db.models import Q

from users.models import User
from .models import *
# from core.utils import login_decorator
from .serializer import *

class PostingProductView(APIView):
    '''
    # 게시글 작성
    '''

    # parameter_token = openapi.Parameter(
    #     "Authorization",
    #     openapi.IN_HEADER,
    #     description = "access_token",
    #     type = openapi.TYPE_STRING
    # )
    # @swagger_auto_schema(request_body = PostingSerializer, manual_parameters = [parameter_token])
    # @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            menu = Menu.objects.create(
                name        = data["name"],
                category    = Category.objects.get(id=data["category"]),
                description = data['description'],
                badge       = Badge.objects.get(id=data["badge"]),
                is_sold     = data['is_sold'],
                tag         = Tag.objects.get(id=data["tag"])
            )
            
            return JsonResponse({"message": f"{menu.name} has successfully posted"}, status=201)
            
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)