from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import SignupView, UsersViewSet, CustomTokenObtainView

app_name = 'api'

router = SimpleRouter()
router.register('users', UsersViewSet, basename='users')

v1_urls = [
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/token/', CustomTokenObtainView.as_view(), name='token_obtain'),
    path('', include(router.urls)),
]

urlpatterns = [
    path('v1/', include(v1_urls)),
]
