from django.urls import path, include

from mainapp import router

app_name = 'mainapp'

urlpatterns = [
    path('api/v1/', include(router.router.urls)),
]
