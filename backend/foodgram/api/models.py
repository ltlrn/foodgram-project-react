from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Tag(models.Model):
    """Some tag, I guess."""

    name = models.CharField("название тега", max_length=200)

    color = models.CharField("цвет", max_length=7, null=True)

    slug = models.SlugField(
        "слаг",
        max_length=200,
        null=True,
        unique=True,
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингридиентов."""

    name = models.CharField(
        "название",
        max_length=200,
    )

    measurement_unit = models.CharField("единицы измерений", max_length=200)

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""

    name = models.CharField("название", max_length=200)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="рецепты пользователя",
    )

    tags = models.ManyToManyField(Tag, verbose_name="теги")

    text = models.TextField("описание")

    image = models.ImageField(
        "картинка", upload_to="api/images/", null=True, blank=True
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientAmount",
        through_fields=["recipe", "ingredient"],
        verbose_name="ингридиенты",
    )

    cooking_time = models.PositiveIntegerField(
        "время приготовления",
        # validators=[MinValueValidator(1)]
    )

    pub_date = models.DateTimeField("дата публикации", auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


# class RecipeTag(models.Model):
#     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
#     tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class IngredientAmount(models.Model):
    """Количество ингридиентов."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )

    amount = models.IntegerField(null=True, default=0)


class ShoppingCart(models.Model):
    "Модель корзины покупок."

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="shopping_cart_presence",
        verbose_name="Рецепт в корзине",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipe_to_cart",
        verbose_name="добавил рецепт в корзину",
    )


class Favorite(models.Model):
    "Модель избранного."

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorite_presence",
        verbose_name="Рецепт в избранном",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipe_to_favorite",
        verbose_name="добавил рецепт в избранное",
    )
