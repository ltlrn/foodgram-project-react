from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

User = settings.AUTH_USER_MODEL


class Tag(models.Model):
    """Модель тегов."""

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
    """Модель ингредиентов."""

    name = models.CharField(
        "название",
        max_length=200,
    )

    measurement_unit = models.CharField("единицы измерений", max_length=200)

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

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
        verbose_name="ингредиенты",
    )

    cooking_time = models.PositiveIntegerField(
        "время приготовления",
        validators=[MinValueValidator(1, "Меньше минуты? Это невероятно быстро!")],
    )

    pub_date = models.DateTimeField("дата публикации", auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    """Модель связи ингредиентов и рецептов."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="рецепт",
    )

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="ингредиент",
    )

    amount = models.IntegerField(
        null=True,
        default=0,
        verbose_name="количество",
    )

    class Meta:
        verbose_name = "Ингредиенты в рецепте"
        verbose_name_plural = "Ингредиенты в рецептах"

    def __str__(self):
        return f"Ингредиенты блюда {self.recipe.name}"


class ShoppingCart(models.Model):
    "Модель корзины покупок."

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="shopping_cart_presence",
        verbose_name="рецепт в корзине",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipe_to_cart",
        verbose_name="добавил рецепт в корзину",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "user"], name="unique_recipe_in_cart"
            ),
        ]

        verbose_name = "Корзина покупок"
        verbose_name_plural = "Корзина покупок"

    def __str__(self):
        return f"{self.user.username}, {self.recipe.name}"


class Favorite(models.Model):
    "Модель избранного."

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorite_presence",
        verbose_name="рецепт в избранном",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipe_to_favorite",
        verbose_name="добавил рецепт в избранное",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "user"], name="unique_recipe_in_favorites"
            ),
        ]

        verbose_name = "Список избранного"
        verbose_name_plural = "Список избранного"

    def __str__(self):
        return f"{self.user.username}, {self.recipe.name}"
