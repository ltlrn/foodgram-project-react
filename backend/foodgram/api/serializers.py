from rest_framework import serializers

from .models import Tag, Ingredient, Recipie, IngredientAmount


class IngredientAmountSerializer(serializers.ModelSerializer):
    
    r_name = serializers.CharField(source='recipie.name')

    class Meta:
        model = IngredientAmount
        fields = ['id', 'amount', 'r_name']
    
    # def to_representation(self, instance):
    #     representation = dict()
    #     representation()

    #     return representation

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipieGetSerializer(serializers.ModelSerializer):
    # ingredients = IngredientAmountSerializer(many=True, required=False, read_only=True)
    ingredients = serializers.SerializerMethodField()
    
    def get_ingredients(self, obj):
        amount_may_be = obj.ingredientamount_set.all()
        return [{
            'id': ing.ingredient.id,
            'ingredient': ing.ingredient.name,
            'measurement_unit': ing.ingredient.measurement_unit,
            'amount': ing.amount 
            } 
            for ing in amount_may_be]


    class Meta:
        model = Recipie
        fields = ('id', 'name', 'ingredients', 'image', 'cooking_time', 'author', 'tags')