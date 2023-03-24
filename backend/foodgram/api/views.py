from django.contrib.auth import get_user_model
from django.db.models import F, Q, Sum
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import Subscription

from api.permissions import AdminOrReadOnly, AuthorStaffOrReadOnly

from .models import (Favorite, Ingredient, Recipe,
                     ShoppingCart, Tag)
from .serializers import (CustomUserSerializer, IngredientSerializer,
                          RecipeGetSerializer, RecipePostPatchSerializer,
                          RecipeShortSerializer, TagSerializer,
                          UserSubscribeSerializer)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Вьюсет для пользователей, который наследуется от вьюсета
    по умолчанию из библиотеки djoser."""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    paginaton_class = PageNumberPagination
    add_serializer = UserSubscribeSerializer
    http_method_names = ["get", "post", "patch", "delete"]

    @action(
        methods=["get"],
        detail=False,
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def subscriptions(self, request):
        """Возвращает все подписки текущего пользователя, если такие
        есть."""
        if self.request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        users = User.objects.filter(subscribing__user=request.user)

        serializer = UserSubscribeSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["POST", "DELETE"],
        detail=True,
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def subscribe(self, request, id):
        """Механизм подписки на автора рецепта и отписки
        от него."""
        author = get_object_or_404(self.queryset, id=id)
        serializer = self.add_serializer(author)
        subscription = Subscription.objects.filter(
            Q(author=author) & Q(user=request.user)
        )

        if (request.method == "POST") and not subscription:
            Subscription.objects.create(author=author, user=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if (request.method == "DELETE") and subscription:
            subscription[0].delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            status=status.HTTP_400_BAD_REQUEST
        )


class TagViewSet(viewsets.ModelViewSet):
    """Вьюсет для тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [
        AdminOrReadOnly,
    ]


class IngredientViewSet(viewsets.ModelViewSet):
    """Вьюсет для ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [
        AdminOrReadOnly,
    ]
    filter_backends = [
        filters.SearchFilter,
    ]
    search_fields = [
        "name",
    ]


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов."""
    queryset = Recipe.objects.all()
    http_method_names = ["get", "post", "patch", "delete"]
    permission_classes = (AuthorStaffOrReadOnly,)
    paginaton_class = PageNumberPagination
    filter_backends = [
        filters.OrderingFilter,
    ]
    ordering_fields = ["pub_date"]
    ordering = ("-pub_date",)

    serializer_class = RecipeGetSerializer
    add_serializer = RecipeShortSerializer

    def get_queryset(self):
        """Фильтрация в соответствии с параметрами запроса."""
        queryset = self.queryset

        user = self.request.user

        tags = self.request.query_params.getlist("tags")

        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()

        author = self.request.query_params.get("author")

        if author:
            queryset = queryset.filter(author=author)

        if user.is_anonymous:
            return queryset

        in_shopping_cart = self.request.query_params.get(
            "is_in_shopping_cart"
        )

        if in_shopping_cart in ["true", "1"]:
            queryset = queryset.filter(shopping_cart_presence__user=user)
        elif in_shopping_cart in ["false", "0"]:
            queryset = queryset.exclude(shopping_cart_presence__user=user)

        in_favorite = self.request.query_params.get("is_favorited")

        if in_favorite in ["true", "1"]:
            queryset = queryset.filter(favorite_presence__user=user)
        if in_favorite in ["false", "0"]:
            queryset = queryset.exclude(favorite_presence__user=user)

        return queryset

    @action(
        methods=["GET", "POST", "DELETE"],
        detail=True,
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def shopping_cart(self, request, pk):
        """Добавляет/удалет рецепт в `список покупок`."""

        recipe = get_object_or_404(self.queryset, id=pk)
        serializer = self.add_serializer(recipe)
        in_cart = ShoppingCart.objects.filter(
            Q(recipe__id=pk) & Q(user=request.user)
        )

        if (request.method == "POST") and not in_cart:
            ShoppingCart.objects.create(recipe=recipe, user=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if (request.method == "DELETE") and in_cart:
            in_cart[0].delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=["POST", "DELETE"],
        detail=True,
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def favorite(self, request, pk):
        """Добавляет/удалет рецепт в `избранное`."""

        recipe = get_object_or_404(self.queryset, id=pk)
        serializer = self.add_serializer(recipe)
        in_favorite = Favorite.objects.filter(
            Q(recipe__id=pk) & Q(user=request.user)
        )

        if (request.method == "POST") and not in_favorite:
            Favorite.objects.create(recipe=recipe, user=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if (request.method == "DELETE") and in_favorite:
            in_favorite[0].delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def download_shopping_cart(self, request):
        """Формирует и возвращает файл со списком ингредиентов и их
        количеством, необходимым для рецептов в корзине."""
        user = request.user
        if not user.recipe_to_cart.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        filename = f"{user.username}_shopping_list.txt"
        shopping_list = [f"Список покупок пользователя: {user.first_name}\n"]

        ingredients = (
            Ingredient.objects.filter(
                recipe__shopping_cart_presence__user=user
            ).values(
                "name", measurement=F("measurement_unit")
            ).annotate(
                amount=Sum("ingredientamount__amount")
            )
        )

        for ing in ingredients:
            shopping_list.append(
                f'{ing["name"]}: {ing["amount"]} {ing["measurement"]}'
            )

        shopping_list = "\n".join(shopping_list)

        response = HttpResponse(
            shopping_list,
            content_type="text.txt; charset=utf-8")
        response["Content-Disposition"] = f"attachment; filename={filename}"

        return response

    def create(self, request):
        serializer = RecipePostPatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data)

    def update(self, request, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RecipeGetSerializer
        elif self.request.method == "POST" or "PATCH":
            return RecipePostPatchSerializer