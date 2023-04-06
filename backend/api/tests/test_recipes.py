from api.models import (
    Favorite,
    Ingredient,
    IngredientAmount,
    Recipe,
    ShoppingCart
)
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from .utils_for_testing import (
    HOST,
    IMAGE,
    REC_DATA,
    TEST_USERS_DATA,
    URL_LOGIN,
    login_and_get_token,
)

User = get_user_model()


class RecipeTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(**TEST_USERS_DATA["user_1"])
        cls.user_2 = User.objects.create_user(**TEST_USERS_DATA["user_2"])
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
        self.authorized_client_2 = APIClient()
        self.admin_client = APIClient()

        authorized = {
            "client": self.authorized_client,
            "url": URL_LOGIN,
            "user": RecipeTests.user,
            "token_model": Token,
        }

        authorized_2 = {
            "client": self.authorized_client_2,
            "url": URL_LOGIN,
            "user": RecipeTests.user_2,
            "token_model": Token,
        }

        authorized_staff = {
            "client": self.admin_client,
            "url": URL_LOGIN,
            "user": RecipeTests.admin,
            "token_model": Token,
        }

        login_and_get_token(password="unbreakable", **authorized)
        login_and_get_token(password="qwerty123457", **authorized_2)
        login_and_get_token(password="strong_password", **authorized_staff)

    def test_create_new_recipe(self):
        """Создание нового рецепта."""

        url = f"{HOST}recipes/"
        response = self.authorized_client.post(
            url, format="json", data=REC_DATA
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Recipe.objects.all().count(), 2)

    def test_update_existing_recipe(self):
        """Обновление рецепта автором. Попытка обновления другим
        пользователем.
        """

        url = f"{HOST}recipes/1/"
        patch_data = {
            "name": "pelmenii",
            "text": "some",
            "cooking_time": 7,
            "ingredients": [
                {"id": 605, "amount": 1},
                {"id": 209, "amount": 4}
            ],
            "tags": [2],
        }
        response_author = self.authorized_client.patch(
            url, format="json", data=patch_data
        )
        response_user = self.authorized_client_2.patch(
            url, format="json", data=patch_data
        )

        self.assertEqual(response_author.status_code, status.HTTP_200_OK)
        self.assertEqual(response_author.data.get("name"), "pelmenii")

        self.assertEqual(response_user.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_to_shopping_cart(self):
        """Добавление рецепта в корзину покупок. Удаление из корзины."""

        records = ShoppingCart.objects.all().count()

        url = f"{HOST}recipes/1/shopping_cart/"

        response = self.authorized_client_2.post(url, format="json")
        records += 1

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ShoppingCart.objects.all().count(), records)

        response_remove = self.authorized_client_2.delete(url, format="json")
        records -= 1

        self.assertEqual(
            response_remove.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(ShoppingCart.objects.all().count(), records)

    def test_add_to_favorite(self):
        """Добавление рецепта в избранное. Удаление из избранного."""

        records = ShoppingCart.objects.all().count()

        url = f"{HOST}recipes/1/favorite/"

        response = self.authorized_client_2.post(url, format="json")
        records += 1

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Favorite.objects.all().count(), records)

        response_remove = self.authorized_client_2.delete(url, format="json")
        records -= 1

        self.assertEqual(
            response_remove.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(Favorite.objects.all().count(), records)

    def test_download_shopping_cart(self):
        """Скачивание списка покупок."""

        url_1 = f"{HOST}recipes/1/shopping_cart/"
        url_2 = f"{HOST}recipes/download_shopping_cart/"

        self.authorized_client_2.post(url_1, format="json")
        response_download = self.authorized_client_2.get(url_2, format="json")

        self.assertEqual(response_download.status_code, status.HTTP_200_OK)
