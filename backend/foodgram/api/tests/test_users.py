# from rest_framework.reverse import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase, APIClient
# from django.contrib.auth import get_user_model
# from rest_framework.authtoken.models import Token
# from .utils_for_testing import login_and_get_token

# import logging

# User = get_user_model()

# HOST = "http://localhost:8000"
# URL_LOGIN = f"{HOST}/api/auth/token/login/"
# URL_LIST = f"{HOST}{reverse('tags-list')}"
# URL_DETAIL = f"{HOST}/api/tags/2/"
# # URL_DETAIL = f"{HOST}{reverse('tags-detail')}"
# POST_DATA = {"name": "feast", "color": "orange", "slug": "feast"}

# logger = logging.getLogger(__name__)


# class TagViewSetTests(APITestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.user_1 = User.objects.create_user(
#             username="mockuser",
#             email="mock@mail.ru",
#             first_name="Ignasio",
#             last_name="Borgia",
#             password="unbreakable",
#         )

        

#         cls.admin = User.objects.create_user(
#             username="mockuser2",
#             email="mock2@mail.ru",
#             first_name="Ada",
#             last_name="Volkova",
#             password="parol",
#             is_staff=True,
#         )

#     def setUp(self):
        
#         user = TagViewSetTests.user
#         admin = TagViewSetTests.admin
        
#         self.authorized_client = APIClient()
#         self.admin_client = APIClient()

#         login_and_get_token(self.authorized_client, user, URL_LOGIN, Token, "unbreakable")
#         login_and_get_token(self.admin_client, admin, URL_LOGIN, Token, 'parol')


#     def test_tags_get_list(self):
#         """
#         Получение списка тагов.
#         """

#         logger.debug('Sending TEST data to url: %s' % URL_LIST)

#         response = self.client.get(URL_LIST, format='json')

#         logger.debug('Testing status code response: %s, code: %d' % (response.data, response.status_code))

#         self.assertEqual(response.status_code, status.HTTP_200_OK)


#     def test_tags_get_detail(self):
#         """Получение одного тага"""

#         response = self.client.get(URL_LIST, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_tags_post(self):
#         """Попытка добавления нового тага, неавторизованный пользователь."""
        
#         response = self.client.post(URL_LIST, format='json', data=POST_DATA)
        
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_tags_post_authorized(self):
#         """Попытка добавления нового тага, авторизованный пользователь."""

#         response = self.authorized_client.post(URL_LIST, format='json', data=POST_DATA)

#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_tags_post_admin(self):
#         """Попытка добавления нового тага, админ."""

#         response = self.admin_client.post(URL_LIST, format='json', data=POST_DATA)

#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)