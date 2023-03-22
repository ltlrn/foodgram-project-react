from django.conf import settings
from django.db import models


class Subscription(models.Model):
    """Модель подписок."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscribed_at",
        verbose_name="Подписчик",
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscribing",
        verbose_name="Подписка",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "author"], name="unique_followers"),
            models.CheckConstraint(
                check=~models.Q(author=models.F("user")),
                name="self subscription denied!",
            ),
        ]

        verbose_name = "Список избранного"

    def __str__(self):
        return f"{self.user.username} => {self.author.username}"
