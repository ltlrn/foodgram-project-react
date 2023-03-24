from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .utils_for_testing import login_and_get_token, TEST_USERS_DATA, TAG_DATA

import logging

User = get_user_model()

HOST = "http://localhost:8000"
URL_LOGIN = f"{HOST}/api/auth/token/login/"
URL_LIST = f"{HOST}{reverse('tags-list')}"
URL_DETAIL = f"{HOST}/api/tags/2/"

logger = logging.getLogger(__name__)


class TagViewSetTests(APITestCase):
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
            "user": TagViewSetTests.user,
            "token_model": Token
        }

        authorized_staff = {
            "client": self.admin_client,
            "url": URL_LOGIN,
            "user": TagViewSetTests.admin,
            "token_model": Token
        }

        login_and_get_token(password="unbreakable", **authorized)
        login_and_get_token(password='strong_password', **authorized_staff)


    def test_tags_get_list(self):
        """
        Получение списка тагов.
        """

        logger.debug('Sending TEST data to url: %s' % URL_LIST)
        response = self.client.get(URL_LIST, format='json')
        logger.debug('Testing status code response: %s, code: %d' % (response.data, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_tags_get_detail(self):
        """Получение одного тага"""

        response = self.client.get(URL_LIST, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tags_post(self):
        """Попытка добавления нового тага, неавторизованный пользователь."""
        
        response = self.client.post(URL_LIST, format='json', data=TAG_DATA)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_tags_post_authorized(self):
        """Попытка добавления нового тага, авторизованный пользователь."""

        response = self.authorized_client.post(URL_LIST, format='json', data=TAG_DATA)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tags_post_admin(self):
        """Попытка добавления нового тага, админ."""

        response = self.admin_client.post(URL_LIST, format='json', data=TAG_DATA)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)