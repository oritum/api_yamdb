from django.urls import include, path

app_name = 'api'

v1_urls = []

urlpatterns = [
    path('v1/', include(v1_urls)),
]
