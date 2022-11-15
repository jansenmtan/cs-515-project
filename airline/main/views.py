import urllib

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse, resolve
from django.http import HttpResponseRedirect

from . import forms

class IndexView(FormView):
    template_name = "main/index.html"
    form_class = forms.FlightSearchForm

    def form_valid(self, form):
        redirect_url = reverse('departureflight')
        get_parameters = urllib.parse.urlencode(form.cleaned_data)
        return redirect(f"{redirect_url}?{get_parameters}")

class SelectDepartureFlightView(TemplateView):
    template_name = "main/departureflights.html"

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

