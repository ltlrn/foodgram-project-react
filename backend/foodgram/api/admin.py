from django.contrib import admin

from .models import Tag, Ingredient, Recipie, Favorite, IngredientAmount


class TagAdmin(admin.ModelAdmin):
    pass

class RecipieAdmin(admin.ModelAdmin):
    # readonly_fields = ('created',) # read about!
    list_display = [
        "name",
        "author"
    ]               

    # def get_subscription(self, obj):
    #     subs = obj.subscribed_at.all()
    #     result = ''

    #     for sub in subs:
    #         result += sub.author.username + ', '

    #     return result[:-2]
       
    # get_subscription.short_description = 'Your label here'


admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipie, RecipieAdmin)
admin.site.register(Favorite)
admin.site.register(IngredientAmount)