from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from users.models import Subscription

from .utils_for_testing import (
    HOST,
    TEST_USERS_DATA,
    URL_LOGIN,
    login_and_get_token
)

User = get_user_model()


class SubscriptionTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(**TEST_USERS_DATA["user_1"])
        cls.user_2 = User.objects.create_user(**TEST_USERS_DATA["user_2"])
        cls.admin = User.objects.create_user(**TEST_USERS_DATA["admin"])

    def setUp(self):
        self.authorized_client = APIClient()
        self.authorized_client_2 = APIClient()
        self.admin_client = APIClient()

        authorized = {
            "client": self.authorized_client,
            "url": URL_LOGIN,
            "user": SubscriptionTests.user,
            "token_model": Token,
        }

        authorized_2 = {
            "client": self.authorized_client_2,
            "url": URL_LOGIN,
            "user": SubscriptionTests.user_2,
            "token_model": Token,
        }

        authorized_staff = {
            "client": self.admin_client,
            "url": URL_LOGIN,
            "user": SubscriptionTests.admin,
            "token_model": Token,
        }

        login_and_get_token(password="unbreakable", **authorized)
        login_and_get_token(password="qwerty123457", **authorized_2)
        login_and_get_token(password="strong_password", **authorized_staff)

    def test_subscribe_action(self):
        """Подписка на пользователя, попытка повторной подписки. Отписка."""

        url = f"{HOST}users/2/subscribe/"
        records = Subscription.objects.all().count()
        response = self.authorized_client.post(url, format="json")

        records += 1

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.all().count(), records)

        response_exist = self.authorized_client.post(url, format="json")

        self.assertEqual(
            response_exist.status_code, status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(Subscription.objects.all().count(), records)

        response_remove = self.authorized_client.delete(url, format="json")
        records -= 1

        self.assertEqual(
            response_remove.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(Subscription.objects.all().count(), records)

    def test_get_subscriptions(self):
        """Получение списка подписок авторизованным/анонимным
        пользователем.
        """

        url = f"{HOST}users/2/subscribe/"
        url_2 = f"{HOST}users/subscriptions/"

        self.authorized_client.post(url, format="json")

        response_auth = self.authorized_client.get(url_2, format="json")
        response_anon = self.client.get(url_2, format="json")

        self.assertEqual(response_auth.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_anon.status_code, status.HTTP_401_UNAUTHORIZED
        )

    def test_try_to_subscribe_on_yourself(self):
        """Попытка подписаться на самого себя."""

        url = f"{HOST}users/1/subscribe/"

        response = self.authorized_client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
