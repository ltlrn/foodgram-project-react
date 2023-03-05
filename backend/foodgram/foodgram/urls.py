from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include('api.urls')),
    path("api/", include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken'))
]



# from django.contrib import admin
# from django.urls import include, path
# from django.views.generic import TemplateView

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path(
#         'redoc/',
#         TemplateView.as_view(template_name='redoc.html'),
#         name='redoc'
#     ),
#     path('api/', include('api.urls')),
#     path('api/v1/auth/', include('users.urls')),
# ]