import json

from django.db import migrations

with open("./data/ingredients.json", encoding="utf-8") as file:
    INGREDIENTS = json.load(file)


def add_ingredients(apps, schema_editor):
    Ingredient = apps.get_model("api", "Ingredient")

    for fields in INGREDIENTS:
        new_ingredient = Ingredient(**fields)
        new_ingredient.save()


def remove_ingredients(apps, schema_editor):
    Ingredient = apps.get_model("api", "Ingredient")

    for id in range(1, len(INGREDIENTS)+1):
        Ingredient.objects.get(id=id).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            add_ingredients,
            remove_ingredients
        ),
    ]
    