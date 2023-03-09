from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TagViewSet, IngredientViewSet, RecipeViewSet

# from users.views import UserViewSet
# from .views import CategoryViewSet, GenreViewSet, TitleDetail, TitleList
# from .views import CommentsViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)

# router_1.register('v1/genres', GenreViewSet)
# router_1.register("v1/users", UserViewSet)
# router_1.register(r'v1/titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
#                   basename='reviews')
# router_1.register(
#     r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     CommentsViewSet,
#     basename='comments')

urlpatterns = [
    path('', include(router.urls)),
]