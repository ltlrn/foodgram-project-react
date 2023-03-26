# Generated by Django 4.1.5 on 2023-03-26 19:27

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Ingredient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="название")),
                (
                    "measurement_unit",
                    models.CharField(max_length=200, verbose_name="единицы измерений"),
                ),
            ],
            options={
                "verbose_name": "Ингредиент",
                "verbose_name_plural": "Ингредиенты",
            },
        ),
        migrations.CreateModel(
            name="IngredientAmount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.IntegerField(
                        default=0, null=True, verbose_name="количество"
                    ),
                ),
                (
                    "ingredient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.ingredient",
                        verbose_name="ингредиент",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ингредиенты в рецепте",
                "verbose_name_plural": "Ингредиенты в рецептах",
            },
        ),
        migrations.CreateModel(
            name="Recipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="название")),
                ("text", models.TextField(verbose_name="описание")),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="api/images/",
                        verbose_name="картинка",
                    ),
                ),
                (
                    "cooking_time",
                    models.PositiveIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(
                                1, "Меньше минуты? Это невероятно быстро!"
                            )
                        ],
                        verbose_name="время приготовления",
                    ),
                ),
                (
                    "pub_date",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="дата публикации"
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recipes",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="рецепты пользователя",
                    ),
                ),
                (
                    "ingredients",
                    models.ManyToManyField(
                        through="api.IngredientAmount",
                        to="api.ingredient",
                        verbose_name="ингредиенты",
                    ),
                ),
            ],
            options={
                "verbose_name": "Рецепт",
                "verbose_name_plural": "Рецепты",
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=200, verbose_name="название тега"),
                ),
                (
                    "color",
                    models.CharField(max_length=7, null=True, verbose_name="цвет"),
                ),
                (
                    "slug",
                    models.SlugField(
                        max_length=200, null=True, unique=True, verbose_name="слаг"
                    ),
                ),
            ],
            options={
                "verbose_name": "Тег",
                "verbose_name_plural": "Теги",
            },
        ),
        migrations.CreateModel(
            name="ShoppingCart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shopping_cart_presence",
                        to="api.recipe",
                        verbose_name="рецепт в корзине",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recipe_to_cart",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="добавил рецепт в корзину",
                    ),
                ),
            ],
            options={
                "verbose_name": "Корзина покупок",
                "verbose_name_plural": "Корзина покупок",
            },
        ),
        migrations.AddField(
            model_name="recipe",
            name="tags",
            field=models.ManyToManyField(to="api.tag", verbose_name="теги"),
        ),
        migrations.AddField(
            model_name="ingredientamount",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="api.recipe",
                verbose_name="рецепт",
            ),
        ),
        migrations.CreateModel(
            name="Favorite",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="favorite_presence",
                        to="api.recipe",
                        verbose_name="рецепт в избранном",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recipe_to_favorite",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="добавил рецепт в избранное",
                    ),
                ),
            ],
            options={
                "verbose_name": "Список избранного",
                "verbose_name_plural": "Список избранного",
            },
        ),
        migrations.AddConstraint(
            model_name="shoppingcart",
            constraint=models.UniqueConstraint(
                fields=("recipe", "user"), name="unique_recipe_in_cart"
            ),
        ),
        migrations.AddConstraint(
            model_name="favorite",
            constraint=models.UniqueConstraint(
                fields=("recipe", "user"), name="unique_recipe_in_favorites"
            ),
        ),
    ]
