"""buylist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from django.conf.urls import url, include
from django.http import HttpResponse
from social_django.models import UserSocialAuth

def profile_view(request):
    token_info = UserSocialAuth.objects.first()
    return HttpResponse(token_info)


urlpatterns = [
    path('api/token/', views.obtain_auth_token),
    path('', include('mainapp.urls', namespace='mainapp')),
    path('admin/', admin.site.urls),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^accounts/profile/$', profile_view),
]
