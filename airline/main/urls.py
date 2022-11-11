from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
        path('', views.IndexView.as_view(), name='index'),
        path('deals/', views.IndexView.as_view(), name='deals'),
        path('rules/', views.IndexView.as_view(), name='rules'),
        path('help/', views.HelpView.as_view(), name='help'),
        path('contactus/', views.ContactUsView.as_view(), name='contactus'),
        path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
        ]
