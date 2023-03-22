from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib import admin

User = get_user_model()

admin.site.unregister(User)

@register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'is_active', 'username', 'first_name', 'last_name', 'email',
    )
    fields = (
        ('is_active', ),
        ('username', 'email', ),
        ('first_name', 'last_name', ),
    )
    fieldsets = []

    search_fields = (
        'username', 'email',
    )
    list_filter = (
        'is_active', 'first_name', 'email',
    )
    save_on_top = True                    





# from django.contrib import admin
# from django.contrib.auth import get_user_model
# from django.contrib.auth.admin import UserAdmin

# from .models import Subscription

# User = get_user_model()

# class UserAdmin(UserAdmin):
#     list_display = ["username", "first_name", "get_subscription"]

#     def get_subscription(self, obj):
#         subs = obj.subscribed_at.all()
#         result = ''

#         for sub in subs:
#             result += sub.author.username + ', '

#         return result[:-2]
       
#     get_subscription.short_description = 'Your label here'

#     fieldsets = (
#         ('Кто таков:', {
#             'fields': (
#                 'first_name',
#                 'last_name'
#             )
#         }),
#     )

# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)

# admin.site.register(Subscription)