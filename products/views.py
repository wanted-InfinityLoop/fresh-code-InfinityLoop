import json

from rest_framework.views import APIView
from django.http import JsonResponse

from .models import Menu, Category, Badge, Tag


class MenuDetailView(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)

            category = Category.objects.get(name=data["category"])
            badge = Badge.objects.get(name=data["badge"])
            tag = Tag.objects.get(name=data["tag"])

            menu = Menu.objects.create(
                name        = data["name"],
                category    = category,
                description = data['description'],
                badge       = badge,
                tag         = tag
            )
            
            return JsonResponse({"message": f"{menu.name} has successfully posted"}, status=201)
            
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

    def delete(self, request, menu_id):
        try:
            menu = Menu.objects.get(id=menu_id)
            result = menu.delete()

            return JsonResponse(
                {
                    "message": f"{menu.name} has successfully deleted",
                    "result": f"{result[0]} rows has affected",
                },
                status=204,
            )

        except Menu.DoesNotExist:
            return JsonResponse({"message": f"Menu {menu_id} not found"}, status=404)
