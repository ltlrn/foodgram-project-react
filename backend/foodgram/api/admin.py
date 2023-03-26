from django.contrib.admin import ModelAdmin, TabularInline, display, register
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)


class IngredientInline(TabularInline):
    model = IngredientAmount
    extra = 2


@register(IngredientAmount)
class LinksAdmin(ModelAdmin):
    pass


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = (
        "name",
        "measurement_unit",
    )
    search_fields = ("name",)
    list_filter = ("name",)

    save_on_top = True


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = (
        "name",
        "author",
        "get_image",
        "count_favorites",
    )
    fields = (
        ("name", "cooking_time"),
        ("author", "tags"),
        ("text",),
        ("image",),
    )
    raw_id_fields = ("author",)
    search_fields = ("name", "author__username", "tags__name")
    list_filter = ("name", "author__username", "tags__name")

    inlines = (IngredientInline,)
    save_on_top = True

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="80" hieght="30"')

    get_image.short_description = "Изображение"

    def count_favorites(self, obj):
        return obj.favorite_presence.count()

    count_favorites.short_description = "В избранном"


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ("name", "slug", "color_code")
    search_fields = ("name", "color")

    save_on_top = True

    @display(description="Colored")
    def color_code(self, obj: Tag):
        return format_html(
            '<span style="color: #{};">{}</span>', obj.color[1:], obj.color
        )

    color_code.short_description = "Цветовой код тэга"


@register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ("user", "recipe")
    search_fields = ("user__username", "recipe__name")

    def has_change_permission(self, request):
        return False

    def has_delete_permission(self, request):
        return False


@register(ShoppingCart)
class CardAdmin(ModelAdmin):
    list_display = ("user", "recipe")
    search_fields = ("user__username", "recipe__name")

    def has_change_permission(self, request):
        return False

    def has_delete_permission(self, request):
        return False
