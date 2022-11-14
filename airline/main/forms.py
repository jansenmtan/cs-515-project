from django import forms
from django.core.mail import send_mail

from . import models

class FlightSearchForm(forms.Form):
    origin_city      = forms.ModelChoiceField(queryset=models.City.objects.all())
    destination_city = forms.ModelChoiceField(queryset=models.City.objects.all())
    depart_date = forms.DateField(widget=forms.DateInput(attrs={ 'type': 'date'}))
    return_date = forms.DateField(widget=forms.DateInput(attrs={ 'type': 'date'}))

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

