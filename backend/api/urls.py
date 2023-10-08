from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CustomUserViewSet, IngredientViewSet, RecipeViewSet,
                    TagViewSet, index)

router = DefaultRouter()
router.register(r"tags", TagViewSet, "tags")
router.register(r"ingredients", IngredientViewSet, "ingredients")
router.register(r"recipes", RecipeViewSet, "recipes")
router.register(r"users", CustomUserViewSet, "users")

urlpatterns = [
    path("", include(router.urls)),
    path("index", index)
]
