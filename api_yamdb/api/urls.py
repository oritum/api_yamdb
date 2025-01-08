from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (
    CustomTokenObtainView,
    SignupView,
    UsersManagementViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet,
)

app_name = 'api'

router = SimpleRouter()
router.register('users', UsersManagementViewSet, basename='users')
router.register('titles', TitleViewSet, basename='titles')

reviews_router = SimpleRouter()
reviews_router.register(
    r'reviews',
    ReviewViewSet,
    basename='reviews'
)

comments_router = SimpleRouter()
comments_router.register(
    r'comments',
    CommentViewSet,
    basename='comments'
)

v1_urls = [
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/token/', CustomTokenObtainView.as_view(), name='token_obtain'),
    path('', include(router.urls)),
    path('titles/<int:title_id>/', include(reviews_router.urls)),
    path('reviews/<int:review_id>/', include(comments_router.urls)),
]

urlpatterns = [
    path('v1/', include(v1_urls)),
]
