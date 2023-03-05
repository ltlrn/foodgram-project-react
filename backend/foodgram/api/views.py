from rest_framework import viewsets

from .models import Tag, Ingredient, Recipie
from .serializers import TagSerializer, IngredientSerializer, RecipieGetSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipieViewSet(viewsets.ModelViewSet):
    queryset = Recipie.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']

    serializer_class = RecipieGetSerializer

    # def get_serializer_class(self):
    #     if self.action = 'post':
    #         serializer_class = RecipiePostSerializer
    #     ....