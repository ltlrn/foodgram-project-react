from api.models import Ingredient, IngredientAmount, Recipe
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from .utils_for_testing import (
    IMAGE,
    ING_DATA,
    TAG_DATA,
    TEST_USERS_DATA,
    URL_LOGIN,
    URL_POOL,
    login_and_get_token,
    url_filter,
)

"""
Эндпоинты, доступные анонимным пользователям:

/api/users/                            GET POST
/api/auth/token/login/                 POST
/api/recipes/                          GET
/api/recipes/<id>/                     GET

+ для авторизованных пользователей:

/api/users/me/                         GET
/api/users/{id}/                       GET
/api/users/subscriptions/              GET
/api/users/{id}/subscribe/             POST DELETE
/api/users/set_password/               POST
/api/auth/token/logout/                POST

/api/recipes/                          POST
/api/recipes/download_shopping_cart/   GET
/api/recipes/{id}/shopping_cart/       POST DELETE
/api/recipes/{id}/favorite/            POST DELETE

+ только для авторов рецепта:

/api/recipes/{id}/                     PATCH DELETE

+ для администраторов:

/api/tags/                             POST
/api/ingredients/                      POST

"""

User = get_user_model()


class ApiAccessTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(**TEST_USERS_DATA["user_1"])
        cls.admin = User.objects.create_user(**TEST_USERS_DATA["admin"])

        cls.recipe = Recipe.objects.create(
            name="recipe_1",
            text="text_1",
            author=cls.user,
            image=IMAGE,
            cooking_time=48,
        )

        cls.recipe.tags.set([1, 3])
        ingredients = [
            {"id": 25, "amount": 3},
            {"id": 325, "amount": 32},
            {"id": 8, "amount": 2},
        ]

        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.get(id=ingredient["id"])
            IngredientAmount.objects.create(
                recipe=cls.recipe,
                ingredient=current_ingredient,
                amount=ingredient["amount"],
            )

    def setUp(self):
        self.authorized_client = APIClient()
        self.admin_client = APIClient()

        authorized = {
            "client": self.authorized_client,
            "url": URL_LOGIN,
            "user": ApiAccessTests.user,
            "token_model": Token,
        }

        authorized_staff = {
            "client": self.admin_client,
            "url": URL_LOGIN,
            "user": ApiAccessTests.admin,
            "token_model": Token,
        }

        login_and_get_token(password="unbreakable", **authorized)
        login_and_get_token(password="strong_password", **authorized_staff)

    def test_access_get_200(self):
        """GET запрос к эндпоинтам приложения в соответствии с
        необходимыми правами доступа.
        """

        urls = url_filter(URL_POOL, method="get")

        for url in urls:
            with self.subTest(url=url.locator):
                client = self.client
                if url.level("get") == "admin":
                    client = self.admin_client
                elif url.level("get") == "auth":
                    client = self.authorized_client

                response = client.get(url.locator, format="json")
                self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_get_try_anon_401(self):
        """попытка GET запроса к эндпоинтам приложения без
        необходимых прав доступа.
        """

        urls = url_filter(URL_POOL, method="get", level="auth")

        for url in urls:
            with self.subTest(url=url.locator):
                response = self.client.get(url.locator, format="json")
                self.assertEqual(
                    response.status_code, status.HTTP_401_UNAUTHORIZED
                )

    def test_add_tags_ingredients_401_403(self):
        """Попытка добавить таг и ингредиент без прав администратора."""

        urls = url_filter(URL_POOL, method="post", level="admin")

        for url in urls:
            with self.subTest(url=url.locator):
                response_tag = self.client.post(
                    url.locator, format="json", data=TAG_DATA
                )
                response_ing = self.client.post(
                    url.locator, format="json", data=ING_DATA
                )
                self.assertEqual(
                    response_tag.status_code, status.HTTP_401_UNAUTHORIZED
                )
                self.assertEqual(
                    response_ing.status_code, status.HTTP_401_UNAUTHORIZED
                )

                response_tag = self.authorized_client.post(
                    url.locator, format="json", data=TAG_DATA
                )
                response_ing = self.authorized_client.post(
                    url.locator, format="json", data=ING_DATA
                )

                self.assertEqual(
                    response_tag.status_code, status.HTTP_403_FORBIDDEN
                )
                self.assertEqual(
                    response_ing.status_code, status.HTTP_403_FORBIDDEN
                )
