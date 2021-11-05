import json

from rest_framework.views import APIView
from django.http          import JsonResponse

from .models import Menu, Category, Badge, Tag, Item


class MenuDetailView(APIView):
    def post(self, request):
        try:
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
        
        product = Menu.objects.get(id=menu_id)
        
        menus = {
            "id"          : product.id,
            "category"    : product.category.name,
            "name"        : product.name,
            "description" : product.description,
            "isSold"      : product.is_sold,
            "badge"       : product.badge.name if product.badge is not None else None,
            "items" : [
                {
                    "item"   : item.id,
                    "memuID" : item.menu.id,
                    "size"   : item.size.name,
                    "price"  : item.price,
                    "isSold" : item.is_sold,
                    } for item in product.item_set.all()],
            "tags" : [
                {
                    "id"     : product.tag.id,
                    "menuID" : product.id,
                    "type"   : product.tag.type,
                    "name"   : product.tag.name
                }
            ]
        }
        
        return JsonResponse({"menus": menus}, status=200)

    def delete(self, request, menu_id):
        try:
            menu   = Menu.objects.get(id=menu_id)
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

    def put(self, request, menu_id):
        try:
            if not Menu.objects.filter(id=menu_id).exists():
                return JsonResponse({"message": f"POSTING_{menu_id}_NOT_FOUND"}, status=404)
            
            data = json.loads(request.body)

            if not (data["name"] or data["description"]):
                return JsonResponse({"message": "Fill_In_All_Values"}, status=404)
            
            menu = Menu.objects.get(id=menu_id)
            
            if data["name"]:
                menu.name = data["name"]
            
            if data["description"]:
                menu.description = data["description"]

            menu.save()

            return JsonResponse({"menu name": menu.name, "menu_desc": menu.description}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except Category.DoesNotExist:
            return JsonResponse({"message": "Category Does not Exist"}, status=404)


class MenuListView(APIView):
    def get(self, request):
        OFFSET = int(request.GET.get("offset", 0))
        LIMIT  = int(request.GET.get("limit", 10))

        menus = (
            Menu.objects.prefetch_related("item_set")
            .all()
            .order_by("-created_time")[OFFSET : OFFSET + LIMIT]
        )

        menus = {
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
    def put(self, request):
        try:
            data = json.loads(request.body)
            
            if not Menu.objects.filter(id=data["menu_id"]).exists():
                return JsonResponse({"message": "MENU_NOT_FOUND"}, status=404)

            if not Item.objects.filter(id=data["id"]).exists():
                return JsonResponse({"message": "ITEMS_NOT_FOUND"}, status=404)

            if not (data["id"] or data["name"] or data["price"] or data["menu_id"]):
                return JsonResponse({"message": "Fill_In_All_Values"}, status=404)
            
            item = Item.objects.get(menu__id=data["menu_id"], id=data["id"])
            
            if data["size"]:
                if not Item.objects.filter(size__name=data["size"]).first():
                    return JsonResponse({"message": "SIZE_NOT_FOUND"}, status=404)

                item.size.name = data["size"]

            if data["price"]:
                item.price = data["price"]

            item.save()

            return JsonResponse({"item size": item.size.name, "item price": item.price}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"message": "Value Error"}, status=404)
