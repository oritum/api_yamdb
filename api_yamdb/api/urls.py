from django.urls import include, path

from api.views import SignupViewSet

app_name = 'api'

v1_urls = [
    path('auth/signup/', SignupViewSet.as_view(), name='signup'),
]

urlpatterns = [
    path('v1/', include(v1_urls)),
]
