import json

from rest_framework.views import APIView
from django.http import JsonResponse

from .models import Menu


class MenuDetailView(APIView):
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
