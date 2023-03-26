HOST = "http://localhost:8000/api/"
URL_LOGIN = f"{HOST}auth/token/login/"

# данные для создания тестовых записей:

IMAGE = "test-image"
ING_DATA = {"name": "new_ingredient", "measurement_unit": "г"}
TAG_DATA = {"name": "feast", "color": "orange", "slug": "feast"}
REC_DATA = {
    "name": "recipe_2",
    "text": "text_2",
    "cooking_time": 34,
    "tags": [1, 3],
    "ingredients": [
        {"id": 1800, "amount": 7},
        {"id": 6, "amount": 1},
        {"id": 2000, "amount": 4},
    ],
}

# данные для создания тестовых пользователей:

TEST_USERS_DATA = {
    "user_1": {
        "username": "mockuser",
        "email": "mock@mail.ru",
        "first_name": "Ignasio",
        "last_name": "Borgia",
        "password": "unbreakable",
    },
    "user_2": {
        "username": "mockuser_2",
        "email": "mock2@mail.ru",
        "first_name": "John",
        "last_name": "Smith",
        "password": "qwerty123457",
    },
    "admin": {
        "username": "mockadmin",
        "email": "mock3@mail.ru",
        "first_name": "Vasily",
        "last_name": "Kovrov",
        "password": "strong_password",
        "is_staff": True,
    },
}

URL_DATA = [
    {"locator": "users/", "get": "auth", "post": "anon"},
    {"locator": "recipes/", "get": "anon", "post": "auth"},
    {"locator": "recipes/1/", "get": "anon", "patch": "me", "delete": "me"},
    {"locator": "users/me/", "get": "auth"},
    {"locator": "users/2/", "get": "auth"},
    {"locator": "tags/", "get": "anon"},
    {"locator": "tags/3/", "get": "anon", "post": "admin"},
    {"locator": "ingredients/23/", "get": "anon", "post": "admin"},
]


class UrlObject:
    """Создает объект URL-aдреса с возможностью ассоциировать с ним
    доступные методы запросов и уровни прав доступа в контексте API.

    пример: users_url = UrlObject(users/, get='anon', post='auth')
    """

    def __init__(self, locator, host="http://localhost:8000/api/", **kwargs):
        self.locator = host + locator
        self.methods = kwargs

    def level(self, method):
        return self.methods.get(method)

    def __str__(self):
        return self.locator


def url_filter(url_pool, method, level=None):
    """Принимает список объектов класса UrlObject, метод запроса и уровень
    доступа, по которому будет осуществляться фильтрация. Возвращает
    отфильтрованный список URL-адресов.
    """

    filtered_urls = [url for url in url_pool if (method in url.methods)]

    if level:
        filtered_urls = [
            url
            for url in url_pool
            if (method in url.methods) and (url.level(method) == level)
        ]

    return filtered_urls


def login_and_get_token(password, **kwargs):
    """Логин тестового пользователя, получение и закрепление токена
    авторизации.
    """

    client = kwargs.get("client")
    user = kwargs.get("user")
    url = kwargs.get("url")
    token_model = kwargs.get("token_model")

    data_for_login = {"email": user.email, "password": password}

    client.post(url, format="json", data=data_for_login)
    token = token_model.objects.get(user__username=user.username)
    client.credentials(HTTP_AUTHORIZATION="Token " + str(token))


URL_POOL = [UrlObject(**data) for data in URL_DATA]
