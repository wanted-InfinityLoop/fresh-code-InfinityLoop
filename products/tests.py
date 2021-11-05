import json

from django.test import TestCase, Client

from .models import *
from users.models import *


class MenuListTest(TestCase):

    def setUp(self):
        category = Category.objects.create(
            name = "도시락"
        )

        badge    = Badge.objects.create(
            name = "new"
        )

        tag      = Tag.objects.create(
            name = "페스코베지테리언",
            type = "vegetarianism"
        )

        size     = Size.objects.create(
            name = "미디엄",
            size = "M"
        )

        menu            = Menu.objects.create(
            name        = "plan도시락",
            category    = category,
            description = "똑똑하고 맛있는 식단관리 도시락",
            badge       = badge,
            tag         = tag,
        )

        Item.objects.create(
            menu = menu,
            size = size,
            price = 3000,
        )

    def tearDown(self):
        Item.objects.all().delete()
        Size.objects.all().delete()
        Menu.objects.all().delete()
        Tag.objects.all().delete()
        Badge.objects.all().delete()
        Category.objects.all().delete()

    def test_get_menu_success(self):
        client = Client()
        response = client.get('/products/list?offset=0&limit=5')
        menus = Menu.objects.all().order_by("-created_time")[:5]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
              "menus"             : [
                {
                    "id"          : menu.id,
                    "category"    : menu.category.name,
                    "name"        : menu.name,
                    "description" : menu.description,
                    "is_sold"     : menu.is_sold,
                    "badge"       : menu.badge.name,
                    "items" : [
                        {
                            "id"      : item.id,
                            "menu_id" : menu.id,
                            "name"    : item.size.name,
                            "size"    : item.size.size,
                            "price"   : item.price,
                            "is_sold" : item.is_sold,
                           } for item in menu.item_set.all()
                    ],
                    "tags" : [
                        {
                            "id"      : menu.tag.id,
                            "menu_id" : menu.id,
                            "type"    : menu.tag.type,
                            "name"    : menu.tag.name,
                            }
                        ],
                    }
                for menu in menus
                ],
            }
        )
