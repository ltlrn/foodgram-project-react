from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CustomUserViewSet, IngredientViewSet, RecipeViewSet,
                    TagViewSet)

router = DefaultRouter()
router.register(r"tags", TagViewSet)
router.register(r"ingredients", IngredientViewSet)
router.register(r"recipes", RecipeViewSet)
router.register(r"users", CustomUserViewSet, "users")

urlpatterns = [
    path("", include(router.urls)),
]
