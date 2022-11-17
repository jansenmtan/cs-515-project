import datetime

from django import forms
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from . import models, fields

class FlightSearchForm(forms.Form):
    origin_city      = forms.ModelChoiceField(queryset=models.City.objects.all())
    destination_city = forms.ModelChoiceField(queryset=models.City.objects.all())
    depart_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    return_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    def clean(self):
        super().clean()
        origin_city      = self.cleaned_data.get('origin_city')
        destination_city = self.cleaned_data.get('destination_city')
        depart_date = self.cleaned_data.get('depart_date')
        return_date = self.cleaned_data.get('return_date')

        errors = []

        if origin_city == destination_city:
            errors.append(ValidationError(
                    "Origin city cannot be the same as destination city.",
                    code='invalid',
                    ))
        if depart_date < datetime.date.today():
            errors.append(ValidationError(
                    "Depart date must be after today.",
                    code='invalid',
                    ))

        if return_date:
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

        if errors:
            raise ValidationError(errors)


class FlightSelectForm(forms.Form):
    flight = forms.ModelChoiceField(
            queryset = models.Flight.objects.all(),
            widget = forms.RadioSelect(),
            required = False,
            )

    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('queryset', models.Flight.objects.all())
        required = kwargs.pop('required', False)
        empty_label = kwargs.pop('empty_label', "No flight")

        super(FlightSelectForm, self).__init__(*args, **kwargs)

        self.fields['flight'].queryset = queryset
        self.fields['flight'].required = required
        self.fields['flight'].empty_label = empty_label
        if required:
            self.fields['flight'].empty_label = None


class TicketQuantityForm(forms.Form):
    ticket_quantity = forms.IntegerField(
            max_value = 10,
            min_value = 1,
            )


class BillingInformationForm(forms.Form):
    card_number = fields.CreditCardField()
    expiry_date = fields.ExpiryDateField()


class CustomerCreationForm(UserCreationForm):

    class Meta:
        model = models.Customer
        fields = ('email', 'cname',)


class CustomerChangeForm(UserChangeForm):

    class Meta:
        model = models.Customer
        fields = ('email', 'cname',)


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

