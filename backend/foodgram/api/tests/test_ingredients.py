from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .utils_for_testing import login_and_get_token, TEST_USERS_DATA, ING_DATA

import logging

User = get_user_model()

HOST = "http://localhost:8000"
URL_LOGIN = f"{HOST}/api/auth/token/login/"
URL_LIST = f"{HOST}{reverse('ingredients-list')}"
URL_DETAIL = f"{HOST}/api/ingredients/2/"

logger = logging.getLogger(__name__)


class IngredientViewSetTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(**TEST_USERS_DATA['user_1'])
        cls.admin = User.objects.create_user(**TEST_USERS_DATA['admin'])

    def setUp(self):

        self.authorized_client = APIClient()
        self.admin_client = APIClient()

        authorized = {
            "client": self.authorized_client,
            "url": URL_LOGIN,
            "user": IngredientViewSetTests.user,
            "token_model": Token
        }

        authorized_staff = {
            "client": self.admin_client,
            "url": URL_LOGIN,
            "user": IngredientViewSetTests.admin,
            "token_model": Token
        }

        login_and_get_token(password="unbreakable", **authorized)
        login_and_get_token(password='strong_password', **authorized_staff)
        
        # user = IngredientViewSetTests.user
        # admin = IngredientViewSetTests.admin
        
        # self.authorized_client = APIClient()
        # self.admin_client = APIClient()

        # login_and_get_token(self.authorized_client, user, URL_LOGIN, Token, "unbreakable")
        # login_and_get_token(self.admin_client, admin, URL_LOGIN, Token, 'strong_password')

    def test_ingredients_get_list(self):
        """
        Получение списка ингредиентов.
        """

        logger.debug('Sending TEST data to url: %s' % URL_LIST)

        response = self.client.get(URL_LIST, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_ingredients_get_detail(self):
        """Получение одного ингредиента"""

        response = self.client.get(URL_LIST, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ingredients_post(self):
        """Попытка добавления нового ингредиента, неавторизованный пользователь."""
        
        response = self.client.post(URL_LIST, format='json', data=ING_DATA)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ingredients_post_authorized(self):
        """Попытка добавления нового ингредиента, авторизованный пользователь."""

        response = self.authorized_client.post(URL_LIST, format='json', data=ING_DATA)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tags_ingredients_admin(self):
        """Попытка добавления нового ингредиента, админ."""

        response = self.admin_client.post(URL_LIST, format='json', data=ING_DATA)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)