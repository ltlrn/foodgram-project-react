# Продуктовый помощник Foodgram

[![foodgram workflow](https://github.com/ltlrn/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/ltlrn/foodgram-project-react/actions/workflows/foodgram_workflow.yml)

   На сервисе Foodgram пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
   
Сервис доступен по адресу:

- http://51.250.109.110

Доступна админка:

- http://51.250.109.110/admin/

Лог-пасс суперпользователя:
- email: so@mail.ru
- password: automata

### Технологии
- Python 3.8+  
- Django 4.1.5 
- Django rest framework 3.12.4
- Postgres
- Docker

### Запуск:

- Склонируйте репозитрий на свой компьютер
- Создайте `.env` файл в директории `infra/`, в котором должны содержаться следующие переменные:
    >DB_ENGINE=django.db.backends.postgresql\
    >DB_NAME= # название БД\ 
    >POSTGRES_USER= # ваше имя пользователя\
    >POSTGRES_PASSWORD= # пароль для доступа к БД\
    >DB_HOST=db\
    >DB_PORT=5432\
- Из папки `infra/` соберите образ при помощи docker-compose
`$ docker-compose up -d --build`
- Примените миграции
`$ docker-compose exec backend python manage.py migrate`
- Соберите статику
`$ docker-compose exec backend python manage.py collectstatic --no-input`
- Создайте суперюзера
`$ docker-compose exec backend python manage.py createsuperuser`

### Автор бэкенда:
Роберт Левченко  
