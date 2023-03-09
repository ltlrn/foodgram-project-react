from rest_framework import serializers

from .models import Tag, Ingredient, Recipe, IngredientAmount, RecipeTag


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


class RecipeGetSerializer(serializers.ModelSerializer):
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
        model = Recipe
        fields = ('id', 'name', 'ingredients', 'image', 'author', 'cooking_time', 'tags')


class RecipePostPatchSerializer(serializers.ModelSerializer):
    # ingredients =
    tags = TagSerializer(read_only=True, many=True)


    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image', 'name', 'text', 'cooking_time')



    def create(self, validated_data):
        
        print(self.initial_data)
        print(validated_data)
        ingredients = self.initial_data.pop('ingredients')

        tags = self.initial_data.pop('tags')

        recipe = Recipe.objects.create(**validated_data)

        for ingredient in ingredients:
            
            current_ingredient = Ingredient.objects.get(id=ingredient["id"])
            IngredientAmount.objects.create(
                recipe=recipe,
                ingredient=current_ingredient,
                amount=ingredient['amount']
            )

        for id in tags:
            current_tag = Tag.objects.get(id=id)
            RecipeTag.objects.create(
                recipe=recipe,
                tag=current_tag
            )
        
        return recipe