from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
        path('', views.IndexView.as_view(), name='index'),
        path('departureflight/', views.SelectDepartureFlightView.as_view(), name='departureflight'),
        path('returnflight/', views.SelectReturnFlightView.as_view(), name='returnflight'),
        path('ticketquantity/', views.TicketQuantityView.as_view(), name='ticketquantity'),
        path('billinginfo/', views.BillingInformationView.as_view(), name='billinginfo'),
        path('deals/', views.IndexView.as_view(), name='deals'),
        path('rules/', views.RulesView.as_view(), name='rules'),
        path('help/', views.HelpView.as_view(), name='help'),
        path('contactus/', views.ContactUsView.as_view(), name='contactus'),
        path('thanks/', views.ThanksView.as_view(), name='thanks'),
        path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
        ]
