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
        if origin_city == destination_city:
            raise ValidationError(
                    "Origin city cannot be the same as destination city.",
                    code='invalid',
                    )
        elif return_date < depart_date:
            raise ValidationError(
                    "Depart date must be after return date.",
                    code='invalid',
                    )
        elif return_date < datetime.date.today():
            raise ValidationError(
                    "Return date must be after today.",
                    code='invalid',
                    )
        elif depart_date < datetime.date.today():
            raise ValidationError(
                    "Depart date must be after today.",
                    code='invalid',
                    )



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

