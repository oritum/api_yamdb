from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (
    CategoryViewSet,
    CommentViewSet,
    CustomTokenObtainView,
    GenreViewSet,
    ReviewViewSet,
    SignupView,
    TitleViewSet,
    UsersManagementViewSet,
)

app_name = 'api'

v1_router = SimpleRouter()
v1_router.register('users', UsersManagementViewSet, basename='users')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)

v1_urls = [
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/token/', CustomTokenObtainView.as_view(), name='token_obtain'),
    path('', include(v1_router.urls)),
]

urlpatterns = [
    path('v1/', include(v1_urls)),
]
