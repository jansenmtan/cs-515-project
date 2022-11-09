from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
        path('', views.IndexView.as_view(), name='index'),
        path('login/', auth_views.LoginView.as_view(template_name='main/login.html')),
        ]
