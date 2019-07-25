from django.urls import path, include
import socializer.views as socializer

app_name = 'socializer'

urlpatterns = [
    path('login/google-oauth2/', socializer.google_login, name='google_login'),
    path('test_login/', socializer.test_login, name='test_login'),
    path('login/', socializer.login, name='login'),
    path('logout/', socializer.logout, name='logout'),
]
