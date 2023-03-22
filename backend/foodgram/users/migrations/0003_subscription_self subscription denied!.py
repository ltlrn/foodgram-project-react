# Generated by Django 4.1.5 on 2023-03-17 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_rename_subscriptions_subscription"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="subscription",
            constraint=models.CheckConstraint(
                check=models.Q(("author", models.F("user")), _negated=True),
                name="self subscription denied!",
            ),
        ),
    ]