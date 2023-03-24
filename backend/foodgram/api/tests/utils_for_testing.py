# TEST_USER_DATA = {
#     "username": "",
#     "email": ,
#     "first_name": ,
#     "last_name": ,
#     "password": ,
# }

# {key}


ING_DATA = {"name": "new_ingredient", "measurement_unit": "г"}
TAG_DATA = {"name": "feast", "color": "orange", "slug": "feast"}

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

def login_and_get_token(password, **kwargs):
#(client, user, url, token_model, passw):  
#   
    client = kwargs.get('client')
    user = kwargs.get('user')
    url = kwargs.get('url')
    token_model = kwargs.get('token_model')

    data_for_login = {
        "email": user.email,
        "password": password
    }

    client.post(url, format='json', data=data_for_login)
    token = token_model.objects.get(user__username=user.username)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))
