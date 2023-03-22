from django.contrib.admin import (ModelAdmin, TabularInline, display, register,
                                  site)
from django.core.handlers.wsgi import WSGIRequest
from django.utils.html import format_html
from django.utils.safestring import SafeString, mark_safe

# from recipes.forms import TagForm
from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)

site.site_header = "Администрирование Foodgram"
EMPTY_VALUE_DISPLAY = "Значение не указано"


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
    empty_value_display = EMPTY_VALUE_DISPLAY


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = (
        "name",
        "author",
        "get_image",
        "count_favorites",
    )
    fields = (
        (
            "name",
            "cooking_time",
        ),
        (
            "author",
            "tags",
        ),
        ("text",),
        ("image",),
    )
    raw_id_fields = ("author",)
    search_fields = (
        "name",
        "author__username",
        "tags__name",
    )
    list_filter = ("name", "author__username", "tags__name")

    inlines = (IngredientInline,)
    save_on_top = True
    empty_value_display = EMPTY_VALUE_DISPLAY

    def get_image(self, obj: Recipe) -> SafeString:
        return mark_safe(f'<img src={obj.image.url} width="80" hieght="30"')

    get_image.short_description = "Изображение"

    def count_favorites(self, obj: Recipe) -> int:
        return obj.favorite_presence.count()

    count_favorites.short_description = "В избранном"


@register(Tag)
class TagAdmin(ModelAdmin):
    # form = TagForm
    list_display = (
        "name",
        "slug",
        "color_code",
    )
    search_fields = ("name", "color")

    save_on_top = True
    empty_value_display = EMPTY_VALUE_DISPLAY

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

    def has_change_permission(
        self,
        request,
    ) -> bool:
        return False

    def has_delete_permission(
        self,
        request,
    ) -> bool:
        return False


@register(ShoppingCart)
class CardAdmin(ModelAdmin):
    list_display = ("user", "recipe")
    search_fields = ("user__username", "recipe__name")

    def has_change_permission(self, request: WSGIRequest) -> bool:
        return False

    def has_delete_permission(
        self,
        request: WSGIRequest,
    ) -> bool:
        return False


# from django.contrib import admin

# from .models import Favorite, Ingredient, IngredientAmount, Recipe, Tag


# class TagAdmin(admin.ModelAdmin):
#     pass


# class RecipeAdmin(admin.ModelAdmin):
#     # readonly_fields = ('created',) # read about!
#     list_display = ["name", "author"]

#     # def get_subscription(self, obj):
#     #     subs = obj.subscribed_at.all()
#     #     result = ''

#     #     for sub in subs:
#     #         result += sub.author.username + ', '

#     #     return result[:-2]

#     # get_subscription.short_description = 'Your label here'


# admin.site.register(Tag)
# admin.site.register(Ingredient)
# admin.site.register(Recipe, RecipeAdmin)
# admin.site.register(Favorite)
# admin.site.register(IngredientAmount)
