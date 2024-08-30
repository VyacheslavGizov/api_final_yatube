from django.urls import include, path


app_name = 'api'

urls_v1 = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]

urlpatterns = [
    path('v1/', include(urls_v1)),
]
