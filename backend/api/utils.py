from rest_framework import filters

from .models import Ingredient


class IngredientSearch(filters.SearchFilter):
    """Фильтр для поиска ингредиентов."""
    search_param = 'name'

    class Meta:
        model = Ingredient
        fields = ['=name',]
