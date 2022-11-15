import urllib

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse, resolve
from django.http import HttpResponseRedirect

from . import forms, models

class IndexView(FormView):
    template_name = "main/index.html"
    form_class = forms.FlightSearchForm

    def form_valid(self, form):
        redirect_url = reverse('departureflight')
        get_parameters = urllib.parse.urlencode(form.cleaned_data)
        return redirect(f"{redirect_url}?{get_parameters}")

class SelectDepartureFlightView(FormView):
    template_name = "main/departureflights.html"
    form_class = forms.FlightSelectForm

    def get_form_kwargs(self):
        queryset_departure_flights = models.Flight.objects.all()

        if self.request.method == "GET":
            origin_city      = models.City.get_object_from_string(self.request.GET.get('origin_city'))
            destination_city = models.City.get_object_from_string(self.request.GET.get('destination_city'))
            queryset_departure_flights = models.Flight.objects.filter(
                    orig = origin_city,
                    dest = destination_city,
                    fdate = self.request.GET.get('depart_date'),
                    available__gt = 0, # equiv. model method: is_available()
                    )

        return { 'queryset_departure_flights': queryset_departure_flights }


    def form_valid(self, form):
        redirect_url = reverse('returnflight')
        # need to save the flight into the current reservation
        return redirect(redirect_url)

class SelectReturnFlightView(TemplateView):
    template_name = "main/returnflights.html"

class HelpView(TemplateView):
    template_name = "main/help.html"

class RulesView(TemplateView):
    template_name = "main/rules.html"

class ContactUsView(FormView):
    template_name = "main/contactus.html"
    form_class = forms.ContactForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # Would send the mail if I wanted to set up a mail server.
        #form.send_mail()
        return super().form_valid(form)

class ThanksView(TemplateView):
    template_name = "main/thanks.html"

