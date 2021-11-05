import json

from rest_framework.views import APIView
from django.http          import JsonResponse

from .models import Menu, Category, Badge, Tag, Item, Size
from users.models import Role
from core.decorators import authorizer


class MenuDetailView(APIView):
    @authorizer
    def post(self, request):
        try:
            if request.user.role_id != Role.Type.ADMIN.value:
                return JsonResponse({"message": "UNAUTHORIZED"}, status = 401)
            
            data = json.loads(request.body)

            category = Category.objects.get(name=data["category"])
            badge    = Badge.objects.get(name=data["badge"])
            tag      = Tag.objects.get(name=data["tag"])

            menu = Menu.objects.create(
                name       =data["name"],
                category   =category,
                description=data["description"],
                badge      =badge,
                tag        =tag,
            )

            return JsonResponse(
                {"message": f"{menu.name} has successfully posted"}, status=201
            )

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


    def get(self, request, menu_id):
        if not Menu.objects.filter(id=menu_id).exists():
            return JsonResponse({"message": f"POSTING_{menu_id}_NOT_FOUND"}, status=404)
        
        menu = Menu.objects.get(id=menu_id)
        
        menus = {
            "id"          : menu.id,
            "category"    : menu.category.name,
            "name"        : menu.name,
            "description" : menu.description,
            "isSold"      : menu.is_sold,
            "badge"       : menu.badge.name if menu.badge is not None else None,
            "items" : [
                {
                    "item"   : item.id,
                    "memuID" : item.menu.id,
                    "size"   : item.size.name,
                    "price"  : item.price,
                    "isSold" : item.is_sold,
                    } for item in menu.item_set.all()],
            "tags" : [
                {
                    "id"     : menu.tag.id,
                    "menuID" : menu.id,
                    "type"   : menu.tag.type,
                    "name"   : menu.tag.name
                }
            ]
        }
        
        return JsonResponse({"menus": menus}, status=200)

    @authorizer
    def delete(self, request, menu_id):
        try:
            if request.user.role_id != Role.Type.ADMIN.value:
                return JsonResponse({"message": "UNAUTHORIZED"}, status = 401)

            menu   = Menu.objects.get(id=menu_id)
            result = menu.delete()

            return JsonResponse(
                {
                    "message": f"{menu.name} has successfully deleted",
                    "result": f"{result[0]} rows has affected",
                },
                status=200,
            )

        except Menu.DoesNotExist:
            return JsonResponse({"message": f"MENU_{menu_id}_NOT_FOUND"}, status=404)

    @authorizer
    def put(self, request, menu_id):
        try:
            if request.user.role_id != Role.Type.ADMIN.value:
                return JsonResponse({"message": "UNAUTHORIZED"}, status = 401)

            if not Menu.objects.filter(id=menu_id).exists():
                return JsonResponse({"message": f"POSTING_{menu_id}_NOT_FOUND"}, status=404)
            
            data = json.loads(request.body)

            if not (data["name"] or data["description"]):
                return JsonResponse({"message": "No input"}, status=404)
            
            menu = Menu.objects.get(id=menu_id)
            
            if data["name"]:
                menu.name = data["name"]
            
            if data["description"]:
                menu.description = data["description"]

            menu.save()

            return JsonResponse({"menu name": menu.name, "menu desc": menu.description}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class MenuListView(APIView):
    def get(self, request):
        OFFSET = int(request.GET.get("offset", 0))
        LIMIT  = int(request.GET.get("limit", 10))

        menus  = (
            Menu.objects.prefetch_related("item_set")
            .all()
            .order_by("-created_time")[OFFSET : OFFSET + LIMIT]
        )

        menus  = {
            "menus": [
                {
                    "id": menu.id,
                    "category": menu.category.name,
                    "name": menu.name,
                    "description": menu.description,
                    "is_sold": menu.is_sold,
                    "badge": menu.badge.name,
                    "items": [
                        {
                            "id": item.id,
                            "menu_id": menu.id,
                            "name": item.size.name,
                            "size": item.size.size,
                            "price": item.price,
                            "is_sold": item.is_sold,
                        }
                        for item in menu.item_set.all()
                    ],
                    "tags": [
                        {
                            "id": menu.tag.id,
                            "menu_id": menu.id,
                            "type": menu.tag.type,
                            "name": menu.tag.name,
                        }
                    ],
                }
                for menu in menus
            ],
        }

        return JsonResponse(menus, status=200)


class MenuItemsView(APIView):
    @authorizer
    def put(self, request, item_id):
        try:
            if request.user.role_id != Role.Type.ADMIN.value:
                return JsonResponse({"message": "UNAUTHORIZED"}, status = 401)

            data = json.loads(request.body)
            
            item = Item.objects.get(id=item_id)

            if not (data["price"] or data["size"]):
                return JsonResponse({"message": "NO_INPUT"}, status=404)

            if data["price"]:
                item.price = data["price"]

            if data["size"]:
                item.size_id = Size.objects.get(size=data["size"]).id

            item.save()

            return JsonResponse({"item price": item.price, "item size": item.size.name}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"message": "VALUE_ERROR"}, status=404)

        except Item.DoesNotExist:
            return JsonResponse({"message": "ITEMS_NOT_FOUND"}, status=404)

        except Size.DoesNotExist:
            return JsonResponse({"message": "SIZE_NOT_FOUND"}, status=404)
