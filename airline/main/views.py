import urllib

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.urls import reverse, resolve
from django.http import HttpResponseRedirect
from django.utils import dateparse

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
        kwargs = super().get_form_kwargs()

        if self.request.method == "GET":
            if self.request.META['QUERY_STRING'] != "":
                origin_city      = models.City.get_object_from_string(self.request.GET.get('origin_city'))
                destination_city = models.City.get_object_from_string(self.request.GET.get('destination_city'))

                queryset_departure_flights = models.Flight.objects.filter(
                        orig = origin_city,
                        dest = destination_city,
                        fdate = self.request.GET.get('depart_date'),
                        available__gt = 0, # equiv. model method: is_available()
                        )

                kwargs.update({ 'queryset': queryset_departure_flights, 'required': True })

        return kwargs

    def form_valid(self, form):
        # save departure flight onto current session
        self.request.session['departure_flight'] = form.data['flight']

        redirect_url = reverse('returnflight')
        return redirect(f"{redirect_url}?{self.request.META['QUERY_STRING']}")

class SelectReturnFlightView(FormView):
    template_name = "main/returnflights.html"
    form_class = forms.FlightSelectForm

    # if self.request.META['QUERY_STRING'] == "", then there needs to be a redirect to the home page

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if self.request.method == "GET":
            if self.request.META['QUERY_STRING'] != "":
                origin_city      = models.City.get_object_from_string(self.request.GET.get('origin_city'))
                destination_city = models.City.get_object_from_string(self.request.GET.get('destination_city'))
                return_date = dateparse.parse_date(self.request.GET.get('return_date'))

                queryset_return_flights = models.Flight.objects.filter(
                        orig = destination_city,
                        dest = origin_city,
                        fdate__gt = self.request.GET.get('depart_date'),
                        available__gt = 0, # equiv. model method: is_available()
                        )
                if return_date is not None:
                    queryset_return_flights.filter(fdate=return_date)
                else:
                    kwargs.update({ 'empty_label': 'No return flight' })

                kwargs.update({ 'queryset': queryset_return_flights })

        return kwargs
    
    def form_valid(self, form):
        # save return flight onto current session
        self.request.session['return_flight'] = form.data['flight']

        return redirect(reverse("ticketquantity"))


class TicketQuantityView(FormView):
    template_name = "main/ticketqty.html"
    form_class = forms.TicketQuantityForm

    def form_valid(self, form):
        # save ticket quantity onto current session
        self.request.session['ticket_quantity'] = form.data['ticket_quantity']

        return redirect(f"{reverse('login')}?next={reverse('billinginfo')}")


class BillingInformationView(FormView):
    template_name = "main/billinginfo.html"
    form_class = forms.BillingInformationForm

    def form_valid(self, form):
        # save billing information onto current session
        self.request.session['card_number'] = form.data['card_number']
        self.request.session['expiry_date_month'] = form.data['expiry_date_0']
        self.request.session['expiry_date_year']  = form.data['expiry_date_1']

        return redirect(f"{reverse('confirmreservation')}")


class ConfirmReservationDetailView(DetailView): # use FormView instead?
    model = models.Reservation
    template_name = 'main/confirmreservation.html'

    def get_object(self, *args, **kwargs):
        return_flight = self.request.session['return_flight']
        rfid = return_flight if return_flight != "" else None
        rf = None if rfid is None else models.Flight.objects.get(pk=rfid)

        reservation_data = {
                'cid':       models.Customer.objects.get(pk=self.request.user.id),
                'dfid':      models.Flight.objects.get(pk=self.request.session['departure_flight']),
                'rfid':      rf,
                'qty':       self.request.session['ticket_quantity'],
                'cardnum':   self.request.session['card_number'],
                'cardmonth': self.request.session['expiry_date_month'],
                'cardyear':  self.request.session['expiry_date_year'],
                }
        return models.Reservation(**reservation_data)


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

