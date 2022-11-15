import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Customer, City, Flight, Reservation
from . import forms

def create_flight(**kwargs):
    default_kwargs = {
            "fdate" :  datetime.date.today(),
            "ftime" :  datetime.datetime.now().time(),
            "price" :  100.00,
            "class_field" :  1,
            "capacity" :  100,
            "available" :  0,
            "orig" :  City(title="Chicago", state="IL"),
            "dest" :  City(title="Los Angeles", state="CA"),
            }
    flight_kwargs = default_kwargs

    for k, v in kwargs.items():
        flight_kwargs[k] = v

    return Flight(**flight_kwargs)


class ReservationModelTests(TestCase):

    def test_cardnum_with_only_numeric_values(self):
        """
        a `cardnum` value with only numeric values is okay.
        """
        pass

    def test_cardnum_with_non_numeric_values(self):
        """
        a `cardnum` value with non-numeric values is not okay.
        """
        pass

    def test_reserve_flight_that_is_not_available(self):
        """
        flights that have an `available` value of 0 cannot be reserved
        """
        unavailable_flight = create_flight(available = 0)
        self.assertIs(unavailable_flight.is_available(), False)

    def test_reserve_flight_that_is_available(self):
        """
        flights that have an `available` value greater than 0 can be reserved
        """
        available_flight = create_flight(available = 100)
        self.assertIs(available_flight.is_available(), True)


class FlightModelTests(TestCase):

    def test_orig_and_dest_are_not_the_same(self):
        """
        the origin and destination cities should not be the same
        """
        pass


class FlightSearchFormTest(TestCase):
    valid_form_data = {}

    @classmethod
    def setUpTestData(cls):
        City.objects.create(title="Chicago", state="IL")
        City.objects.create(title="Los Angeles", state="CA")

    def setUp(self):
        self.valid_form_data.update({
            'origin_city':      City.objects.get(pk=1).pk,
            'destination_city': City.objects.get(pk=2).pk,
            'depart_date': datetime.date.today(), 
            'return_date': datetime.date.today() + datetime.timedelta(days=10),
            })

    def test_origin_city_is_same_as_destination_city(self):
        form_data = {
            **self.valid_form_data,
            'origin_city':      City.objects.get(pk=1).pk,
            'destination_city': City.objects.get(pk=1).pk,
            }
        form = forms.FlightSearchForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_origin_city_is_not_same_as_destination_city(self):
        form_data = {
            **self.valid_form_data,
            'origin_city':      City.objects.get(pk=1).pk,
            'destination_city': City.objects.get(pk=2).pk,
            }
        form = forms.FlightSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_return_date_is_before_depart_date(self):
        form_data = {
            **self.valid_form_data,
            'depart_date': datetime.date.today() + datetime.timedelta(days=10), 
            'return_date': datetime.date.today() + datetime.timedelta(days=5),
            }
        form = forms.FlightSearchForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_return_date_is_after_depart_date(self):
        form_data = {
            **self.valid_form_data,
            'depart_date': datetime.date.today(), 
            'return_date': datetime.date.today() + datetime.timedelta(days=10),
            }
        form = forms.FlightSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_return_date_is_before_today(self):
        form_data = {
            **self.valid_form_data,
            'depart_date': datetime.date.today() - datetime.timedelta(days=10),
            'return_date': datetime.date.today(),
            }
        form = forms.FlightSearchForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_depart_date_is_before_today(self):
        form_data = {
            **self.valid_form_data,
            'depart_date': datetime.date.today() - datetime.timedelta(days=10),
            }
        form = forms.FlightSearchForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_return_date_is_none(self):
        """
        set a null return date. should be valid
        """
        form_data = {
            **self.valid_form_data,
            'return_date': None,
            }
        form = forms.FlightSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
