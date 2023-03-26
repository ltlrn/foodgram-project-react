from django.db import migrations

TAGS_TO_DB = [
    {"name": "завтрак", "color": "#00696b", "slug": "breakfast"},
    {"name": "обед", "color": "#749e35", "slug": "lunch"},
    {"name": "ужин", "color": "#fa9a50", "slug": "dinner"},
    {"name": "закуска", "color": "#d11200", "slug": "snack"}
]


def add_tags(apps, schema_editor):
    Tag = apps.get_model('api', 'Tag')
    for fields in TAGS_TO_DB:
        tag_to_add = Tag(**fields)
        tag_to_add.save()


def remove_tags(apps, schema_editor):
    Tag = apps.get_model('api', 'Tag')
    for fields in TAGS_TO_DB:
        Tag.objects.get(slug=fields['slug']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_add_ingredients"),
    ]

    operations = [
        migrations.RunPython(
            add_tags,
            remove_tags
        )
    ]
    