import json
import jwt

from datetime import datetime, timedelta
from django.test import TestCase, Client

from products.models import *
from users.models import *
from my_settings import MY_SECRET_KEY


class MenuListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        Category.objects.create(id=1, name="도시락")

        Badge.objects.create(id=1, name="new")

        Tag.objects.create(id=1, name="페스코베지테리언", type="vegetarianism")

        Size.objects.create(id=1, name="미디엄", size="M")

        Menu.objects.create(
            id=1,
            name="plan도시락",
            category_id=1,
            description="똑똑하고 맛있는 식단관리 도시락",
            badge_id=1,
            tag_id=1,
        )

        Item.objects.create(
            menu_id=1,
            size_id=1,
            price=3000,
        )

    def tearDown(self):
        Item.objects.all().delete()
        Menu.objects.all().delete()
        Size.objects.all().delete()
        Tag.objects.all().delete()
        Badge.objects.all().delete()
        Category.objects.all().delete()

    def test_get_menu_list_success(self):
        response = self.client.get("/products/list?offset=0&limit=5")

        menus = Menu.objects.all().order_by("-created_time")[:5]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
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
            },
        )


class MenuDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        Role.objects.create(id=1, name="관리자")
        Role.objects.create(id=2, name="고객")

        User.objects.create(
            id=1,
            email="abc@gmail.com",
            password="abcd1234!@",
            name="songTest",
            role_id=1,
        )

        User.objects.create(
            id=2,
            email="qwerty@gmail.com",
            password="abcd1234!@",
            name="songTest",
            role_id=2,
        )

        self.admin_token = jwt.encode(
            {
                "id": 1,
                "role": 1,
                "exp": datetime.utcnow() + timedelta(hours=6),
            },
            MY_SECRET_KEY,
            algorithm="HS256",
        )

        self.customer_token = jwt.encode(
            {
                "id": 2,
                "role": 2,
                "exp": datetime.utcnow() + timedelta(hours=6),
            },
            MY_SECRET_KEY,
            algorithm="HS256",
        )

        self.invalid_token = jwt.encode(
            {"id": 1, "role": 5, "exp": datetime.utcnow() + timedelta(hours=6)},
            MY_SECRET_KEY,
            algorithm="HS256",
        )

        Category.objects.create(id=1, name="샐러드")

        Badge.objects.create(id=1, name="세일상품")

        Tag.objects.create(id=1, name="간식", type="snack")

        Menu.objects.create(
            id=1,
            name="맛있는 샐러드",
            category_id=1,
            description="맛있는 샐러드입니다.",
            badge_id=1,
            is_sold=False,
            tag_id=1,
        )

        Size.objects.create(id=1, name="미디움", size="M")
        Size.objects.create(id=2, name="라지", size="L")

        Item.objects.create(
            id=1,
            menu_id=1,
            size_id=1,
            price=10000,
            is_sold=False,
        )

    def TearDown(self):
        Item.objects.all().delete()
        Size.objects.all().delete()
        Menu.objects.all().delete()
        Tag.objects.all().delete()
        Badge.objects.all().delete()
        Category.objects.all().delete()

    def test_post_menu_success(self):
        header = {"HTTP_Authorization": self.admin_token}

        data = {
            "name": "맛있는 샐러드",
            "category": "샐러드",
            "description": "맛있는 샐러드입니다.",
            "badge": "세일상품",
            "tag": "간식",
        }

        response = self.client.post(
            "/products", json.dumps(data), content_type="application/json", **header
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(), {"message": "맛있는 샐러드 has successfully posted"}
        )

    def test_post_menu_key_error(self):
        header = {"HTTP_Authorization": self.admin_token}

        data = {
            "category": "샐러드",
            "description": "맛있는 샐러드입니다.",
            "badge": "세일상품",
            "tag": "간식",
        }

        response = self.client.post(
            "/products", json.dumps(data), content_type="application/json", **header
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "KEY_ERROR"})

    def test_post_menu_unauthorized_error(self):
        header = {"HTTP_Authorization": self.customer_token}

        data = {
            "name": "맛있는 샐러드",
            "category": "샐러드",
            "description": "맛있는 샐러드입니다.",
            "badge": "세일상품",
            "tag": "간식",
        }

        response = self.client.post(
            "/products", json.dumps(data), content_type="application/json", **header
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"message": "UNAUTHORIZED"})

    def test_post_menu_not_found_access_token(self):
        data = {
            "name": "맛있는 샐러드",
            "category": "샐러드",
            "description": "맛있는 샐러드입니다.",
            "badge": "세일상품",
            "tag": "간식",
        }

        response = self.client.post(
            "/products", json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"message": "Not Found Access_token"})

    def test_post_menu_invalid_user(self):
        header = {"HTTP_Authorization": self.invalid_token}

        data = {
            "name": "맛있는 샐러드",
            "category": "샐러드",
            "description": "맛있는 샐러드입니다.",
            "badge": "세일상품",
            "tag": "간식",
        }

        response = self.client.post(
            "/products", json.dumps(data), content_type="application/json", **header
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"message": "Invalid User"})

    def test_get_menu_success(self):
        response = self.client.get("/products/1")

        menu = Menu.objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "menus": {
                    "id": menu.id,
                    "category": menu.category.name,
                    "name": menu.name,
                    "description": menu.description,
                    "isSold": menu.is_sold,
                    "badge": menu.badge.name if menu.badge is not None else None,
                    "items": [
                        {
                            "item": item.id,
                            "memuID": item.menu.id,
                            "size": item.size.name,
                            "price": item.price,
                            "isSold": item.is_sold,
                        }
                        for item in menu.item_set.all()
                    ],
                    "tags": [
                        {
                            "id": menu.tag.id,
                            "menuID": menu.id,
                            "type": menu.tag.type,
                            "name": menu.tag.name,
                        }
                    ],
                }
            },
        )

    def test_get_menu_not_found(self):
        response = self.client.get("/products/3")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"message": "POSTING_3_NOT_FOUND"})

    def test_delete_menu_success(self):
        header = {"HTTP_Authorization": self.admin_token}

        response = self.client.delete("/products/1", **header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "message": "맛있는 샐러드 has successfully deleted",
                "result": "2 rows has affected",
            },
        )

    def test_delete_menu_unauthorized(self):
        header = {"HTTP_Authorization": self.customer_token}

        response = self.client.delete("/products/1", **header)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {"message": "UNAUTHORIZED"},
        )

    def test_delete_menu_does_not_exist(self):
        header = {"HTTP_Authorization": self.admin_token}

        response = self.client.delete("/products/3", **header)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {"message": "MENU_3_NOT_FOUND"},
        )

    def test_put_menu_success(self):
        header = {"HTTP_Authorization": self.admin_token}
        menu_data = {"name": "음료", "description": "아주아주 맛있는 음료"}

        response = self.client.put(
            "/products/1",
            json.dumps(menu_data),
            content_type="application/json",
            **header
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"menu name": menu_data["name"], "menu desc": menu_data["description"]},
        )

    def test_put_menu_unauthorized(self):
        header = {"HTTP_Authorization": self.customer_token}
        menu_data = {"name": "음료", "description": "아주아주 맛있는 음료"}

        response = self.client.put(
            "/products/1",
            json.dumps(menu_data),
            content_type="application/json",
            **header
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {"message": "UNAUTHORIZED"},
        )

    def test_put_menu_not_found(self):
        header = {"HTTP_Authorization": self.admin_token}
        menu_data = {"name": "음료", "description": "아주아주 맛있는 음료"}

        response = self.client.put(
            "/products/3",
            json.dumps(menu_data),
            content_type="application/json",
            **header
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {"message": "POSTING_3_NOT_FOUND"},
        )
    
    def test_put_menu_no_input(self):
        header = {"HTTP_Authorization": self.admin_token}
        menu_data = {"name": "", "description": ""}

        response = self.client.put(
            "/products/1",
            json.dumps(menu_data),
            content_type="application/json",
            **header
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {"message": "No input"},
        )
    
    def test_put_menu_item_success(self):
        header = {"HTTP_Authorization": self.admin_token}
        menu_data = {"price": 8000, "size": "L"}

        response = self.client.put(
            "/products/item/1",
            json.dumps(menu_data),
            content_type="application/json",
            **header
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"item price": menu_data["price"], "item size": "라지"},
        )
    
    def test_put_menu_item_unauthorized(self):
        header = {"HTTP_Authorization": self.customer_token}
        menu_data = {"price": 8000, "size": "L"}

        response = self.client.put(
            "/products/item/1",
            json.dumps(menu_data),
            content_type="application/json",
            **header
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {"message": "UNAUTHORIZED"},
        )
    
    def test_put_menu_item_no_input(self):
        header = {"HTTP_Authorization": self.admin_token}
        menu_data = {"price": None, "size": ""}

        response = self.client.put(
            "/products/item/1",
            json.dumps(menu_data),
            content_type="application/json",
            **header
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {"message": "NO_INPUT"},
        )
    
    def test_put_menu_item_value_error(self):
        header = {"HTTP_Authorization": self.admin_token}
        menu_data = {"price": "price", "size": ""}

        response = self.client.put(
            "/products/item/1",
            json.dumps(menu_data),
            content_type="application/json",
            **header
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {"message": "VALUE_ERROR"},
        )

    def test_put_menu_item_does_not_exist(self):
        header = {"HTTP_Authorization": self.admin_token}
        menu_data = {"price": 8000, "size": "L"}

        response = self.client.put(
            "/products/item/3",
            json.dumps(menu_data),
            content_type="application/json",
            **header
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {"message": "ITEMS_NOT_FOUND"},
        )

    def test_put_menu_size_does_not_exist(self):
        header = {"HTTP_Authorization": self.admin_token}
        menu_data = {"price": 8000, "size": "S"}

        response = self.client.put(
            "/products/item/1",
            json.dumps(menu_data),
            content_type="application/json",
            **header
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {"message": "SIZE_NOT_FOUND"},
        )
