from django.urls import path
from . import views


urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('auth/login', views.login, name='login'),
    path('auth/logout', views.logout, name='logout'),
]
