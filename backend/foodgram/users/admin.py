from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
# from sorl.thumbnail.admin import AdminImageMixin

from .models import Subscription

User = get_user_model()

class UserAdmin(UserAdmin):
    # readonly_fields = ('created',) # read about!
    list_display = ["username", "first_name", "get_subscription"]

    def get_subscription(self, obj):
        subs = obj.subscribed_at.all()
        result = ''

        for sub in subs:
            result += sub.author.username + ', '

        return result[:-2]
       
    get_subscription.short_description = 'Your label here'

# read about:
# admin.TabularInline
#     extra = 3?

# inlines = (IngredientRecipeRelationAdminInLine,)

# what are fieldsets?

    fieldsets = (
        ('Кто таков:', {
            'fields': (
                'first_name',
                'last_name'
            )
        }),
    )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Subscription)