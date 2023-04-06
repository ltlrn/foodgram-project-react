import base64

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from .models import Ingredient, IngredientAmount, Recipe, Tag

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    """Кастомное поле сериализатора для работы с Base64."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            extension = format.split("/")[-1]

            data = ContentFile(
                base64.b64decode(imgstr), name="temp." + extension
            )

        return super().to_internal_value(data)


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания нового пользователя, наследуется от
    сериализатора из библиотеки djoser."""

    class Meta(UserCreateSerializer.Meta):
        fields = [
            "email",
            "id",
            "first_name",
            "last_name",
            "username",
            "password"
        ]


class CustomUserSerializer(UserSerializer):
    """Сериализатор для пользователя, наследуется от сериализатора из
    библиотеки djoser."""
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        current_user = self.context.get("view").request.user
        if current_user.is_anonymous or (current_user == obj):
            return False
        return current_user.subscribed_at.filter(author=obj).exists()

    class Meta(UserSerializer.Meta):
        fields = [
            "email",
            "id",
            "first_name",
            "last_name",
            "username",
            "is_subscribed"
        ]


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Сериализатор модели IngredientAmountSerializer."""

    r_name = serializers.CharField(source="recipie.name")

    class Meta:
        model = IngredientAmount
        fields = ["id", "amount", "r_name"]


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели Tag."""

    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор модели Ingredient."""
    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class RecipeGetSerializer(serializers.ModelSerializer):
    """Сериализатор для получения рецептов."""

    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(required=False, allow_null=True)
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)

    def get_ingredients(self, obj):
        amount_may_be = obj.ingredientamount_set.all()
        return [
            {
                "id": ing.ingredient.id,
                "name": ing.ingredient.name,
                "measurement_unit": ing.ingredient.measurement_unit,
                "amount": ing.amount,
            }
            for ing in amount_may_be
        ]

    def get_is_favorited(self, obj):
        current_user = self.context.get("view").request.user

        if current_user.is_anonymous:
            return False

        return current_user.recipe_to_favorite.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        current_user = self.context.get("view").request.user

        if current_user.is_anonymous:
            return False

        return current_user.recipe_to_cart.filter(recipe=obj).exists()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "ingredients",
            "image",
            "author",
            "cooking_time",
            "tags",
            "is_favorited",
            "is_in_shopping_cart",
        )


class RecipePostPatchSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления рецепта."""

    image = Base64ImageField(required=False, allow_null=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Recipe
        fields = [
            "id",
            "ingredients",
            "tags",
            "image",
            "name",
            "text",
            "cooking_time"
        ]
        read_only_fields = ["id"]

    def validate(self, data):
        tags = self.initial_data.get("tags")
        ingredients = self.initial_data.get("ingredients")

        if not tags or not ingredients:
            raise ValidationError("Недостаточно данных.")

        data.update({"tags": tags, "ingredients": ingredients})

        return data

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients", [])
        tags_data = validated_data.pop("tags", [])
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags_data)

        for ingredient in ingredients:

            current_ingredient = Ingredient.objects.get(id=ingredient["id"])
            IngredientAmount.objects.create(
                recipe=recipe,
                ingredient=current_ingredient,
                amount=ingredient["amount"],
            )

        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop("ingredients", [])
        tags_data = validated_data.pop("tags", [])

        instance.tags.set(tags_data)
        instance.ingredients.clear()

        for ingredient in ingredients_data:
            current_ingredient = Ingredient.objects.get(id=ingredient["id"])
            IngredientAmount.objects.create(
                recipe=instance,
                ingredient=current_ingredient,
                amount=ingredient["amount"],
            )

        instance.name = validated_data.get("name", instance.name)
        instance.text = validated_data.get("text", instance.text)
        instance.cooking_time = validated_data.get(
            "cooking_time", instance.cooking_time
        )
        instance.image = validated_data.get("image", instance.image)
        instance.save()

        return instance


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода некоторых полей рецепта."""

    class Meta:
        model = Recipe
        fields = "id", "name", "image", "cooking_time"
        read_only_fields = [
            "__all__",
        ]


class UserSubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор для механизма подписок."""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    def get_recipes(self, obj):
        request = self.context.get('request')
        queryset = Recipe.objects.filter(author=obj.id)

        if request.GET.get('recipes_limit'):
            limit = int(request.GET.get('recipes_limit'))
            queryset = queryset[:limit]

        serializer = RecipeShortSerializer(
            queryset, many=True, read_only=True
        )

        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_is_subscribed(self, obj):
        return True

    class Meta:
        model = User
        fields = [
            "email",
            "id",
            "first_name",
            "last_name",
            "username",
            "is_subscribed",
            "recipes",
            "recipes_count",
        ]
