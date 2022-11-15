import datetime

from django import forms
from django.core.mail import send_mail
from django.core.exceptions import ValidationError

from . import models

class FlightSearchForm(forms.Form):
    origin_city      = forms.ModelChoiceField(queryset=models.City.objects.all())
    destination_city = forms.ModelChoiceField(queryset=models.City.objects.all())
    depart_date = forms.DateField(widget=forms.DateInput(attrs={ 'type': 'date'}))
    return_date = forms.DateField(widget=forms.DateInput(attrs={ 'type': 'date'}))

    def clean(self):
        super().clean()
        origin_city      = self.cleaned_data.get('origin_city')
        destination_city = self.cleaned_data.get('destination_city')
        return_date = self.cleaned_data.get('return_date')
        depart_date = self.cleaned_data.get('depart_date')

        errors = []
        if origin_city == destination_city:
            errors.append(ValidationError(
                    "Origin city cannot be the same as destination city.",
                    code='invalid',
                    ))
        if return_date < depart_date:
            errors.append(ValidationError(
                    "Depart date must be after return date.",
                    code='invalid',
                    ))
        if return_date < datetime.date.today():
            errors.append(ValidationError(
                    "Return date must be after today.",
                    code='invalid',
                    ))
        if depart_date < datetime.date.today():
            errors.append(ValidationError(
                    "Depart date must be after today.",
                    code='invalid',
                    ))
        if errors:
            raise ValidationError(errors)


class FlightSelectForm(forms.Form):
    flight = forms.ModelChoiceField(
            queryset = models.Flight.objects.none(),
            widget = forms.RadioSelect(),
            )

    def __init__(self, *args, **kwargs):
        queryset_departure_flights = kwargs.pop('queryset_departure_flights', models.Flight.objects.none())
        super(FlightSelectForm, self).__init__(*args, **kwargs)

        self.fields['flight'].queryset = queryset_departure_flights

class CustomerLoginForm(forms.Form):
    email = forms.EmailField(label='Email address')

class ContactForm(forms.Form):
    name = forms.CharField(max_length=40)
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)

    def send_mail(self):
        send_mail(
                self.cleaned_data['subject'],
                self.cleaned_data['message'],
                self.cleaned_data['email'],
                ['jansenmtan@gmail.com'],
                )

