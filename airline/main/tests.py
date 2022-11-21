import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

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

def initialize_City_and_Flight():
    City.objects.create(title="Chicago", state="IL")
    City.objects.create(title="Los Angeles", state="CA")
    Flight.objects.create(
            fdate = datetime.date.today(),
            ftime = datetime.datetime.now().time(),
            price = 100.00,
            class_field = 1,
            capacity = 100,
            available = 81,
            orig = City.objects.get(title="Chicago"),
            dest = City.objects.get(title="Los Angeles"),
            )
    Flight.objects.create(
            fdate = datetime.date.today(),
            ftime = datetime.datetime.now().time(),
            price = 200.00,
            class_field = 2,
            capacity = 200,
            available = 91,
            orig = City.objects.get(title="Los Angeles"),
            dest = City.objects.get(title="Chicago"),
            )


class ReservationModelTests(TestCase):
    valid_reservation_data = {}

    @classmethod
    def setUpTestData(cls):
        initialize_City_and_Flight()

        Customer_user_model = get_user_model()
        Customer_user_model.objects.create_user(email='jd@ex.io', cname='John Doe', password='pass')

    def setUp(self):
        self.valid_reservation_data.update({
            'cid':       Customer.objects.get(cname='John Doe'),
            'dfid':      Flight.objects.get(capacity=100),
            'rfid':      Flight.objects.get(capacity=200),
            'qty':       1,
            'cardnum':   "4111111111111111",
            'cardmonth': 12,
            'cardyear':  2022,
            })

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

    def test_place_valid_reservation(self):
        reservation_data = {**self.valid_reservation_data}
        reservation = Reservation(**reservation_data)
        self.assertTrue(Reservation.place(reservation))

    def test_get_price_of_reservation_with_return_flight(self):
        reservation_data = {**self.valid_reservation_data}
        reservation = Reservation(**reservation_data)
        # price should be equal to (100 + 200) * 40% = 120
        self.assertEquals(reservation.get_price(), 120)

    def test_get_price_of_reservation_without_return_flight(self):
        reservation_data = {**self.valid_reservation_data, 'rfid': None,}
        reservation = Reservation(**reservation_data)
        # price should be equal to 100
        self.assertEquals(reservation.get_price(), 100)

    def test_get_price_of_reservation_with_qty(self):
        reservation_data = {**self.valid_reservation_data, 'qty': 3}
        reservation = Reservation(**reservation_data)
        # price should be equal to (100 + 200) * 40% * 3 = 360
        self.assertEquals(reservation.get_price(), 360)

class FlightModelTests(TestCase):

    def test_orig_and_dest_are_not_the_same(self):
        """
        the origin and destination cities should not be the same
        """
        pass

    def test_flight_is_not_available(self):
        """
        flights that have an `available` value of 0 cannot be reserved
        """
        unavailable_flight = create_flight(available = 0)
        self.assertIs(unavailable_flight.is_available(), False)

    def test_flight_is_available(self):
        """
        flights that have an `available` value greater than 0 can be reserved
        """
        available_flight = create_flight(available = 100)
        self.assertIs(available_flight.is_available(), True)


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


class FlightSelectFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        initialize_City_and_Flight()

    def test_one_flight_selected(self):
        form = forms.FlightSelectForm(data={'flight': Flight.objects.get(pk=1).pk})
        self.assertTrue(form.is_valid())

    def test_empty_form(self):
        form = forms.FlightSelectForm()
        self.assertFalse(form.is_valid())

    def test_no_flight_selected_with_required_set_to_false(self):
        form = forms.FlightSelectForm(required=False, data={'flight': ''})
        self.assertTrue(form.is_valid())

    def test_form_field_made_with_no_queryset_has_flight_field_with_all_flights(self):
        form = forms.FlightSelectForm()
        self.assertEquals(form.fields['flight'].queryset.count(), Flight.objects.all().count())

    def test_form_field_made_with_queryset_has_flight_field_with_same_count_as_queryset(self):
        queryset = Flight.objects.filter(orig=City.objects.get(title="Chicago"))
        form = forms.FlightSelectForm(queryset=queryset)
        self.assertEquals(form.fields['flight'].queryset.count(), queryset.count())


class CustomerManagerTest(TestCase):

    def test_create_user(self):
        Customer = get_user_model()
        c = Customer.objects.create_user(email='jd@ex.io', cname='John Doe', password='pass')

        self.assertTrue(c.is_active)
        self.assertFalse(c.is_staff)
        self.assertFalse(c.is_superuser)

        with self.assertRaises(TypeError):
            Customer.objects.create_user()
        with self.assertRaises(TypeError):
            Customer.objects.create_user(email='')
        with self.assertRaises(TypeError):
            Customer.objects.create_user(email='ea@ex.io', password='pwd')

    def test_create_superuser(self):
        Customer = get_user_model()
        c = Customer.objects.create_superuser(email='jd@ex.io', cname='John Doe', password='pass')

        self.assertTrue(c.is_active)
        self.assertTrue(c.is_staff)
        self.assertTrue(c.is_superuser)


class CustomerCreationFormTest(TestCase):

    def test_create_customer(self):
        self.assertEquals(Customer.objects.all().count(), 0)
        form = forms.CustomerCreationForm(data={'email': 'jd@ex.io', 'cname': 'John Doe', 'password1': 'his password.', 'password2': 'his password.',})
        form.save()
        self.assertEquals(Customer.objects.all().count(), 1)

class CreateAccountViewTest(TestCase):

    def test_create_account(self):
        c = Client()

        self.assertEquals(Customer.objects.all().count(), 0)

        next_url = reverse('billinginfo')
        response = c.post(f"{reverse('createaccount')}?next={next_url}", {'email': 'jd@ex.io', 'cname': 'John Doe', 'password1': 'his password.', 'password2': 'his password.',})

        self.assertEquals(Customer.objects.all().count(), 1)
        self.assertIn('_auth_user_id', c.session)


class SubmitReservationViewTest(TestCase):
    valid_reservation_data = {}

    @classmethod
    def setUpTestData(cls):
        initialize_City_and_Flight()

        Customer_user_model = get_user_model()
        Customer_user_model.objects.create_user(email='jd@ex.io', cname='John Doe', password='pass')

    def setUp(self):
        self.valid_reservation_data.update({
            'cid':       Customer.objects.get(cname='John Doe'),
            'dfid':      Flight.objects.get(capacity=100),
            'rfid':      Flight.objects.get(capacity=200),
            'qty':       1,
            'cardnum':   "4111111111111111",
            'cardmonth': 12,
            'cardyear':  2022,
            })

    def test_place_valid_reservation(self):
        c = Client()

        c.login(email='jd@ex.io', password='pass')

        session = c.session
        session.update({
            'departure_flight':  Flight.objects.all()[0].pk,
            'return_flight':     Flight.objects.all()[1].pk,
            'ticket_quantity':   1,
            'card_number':       self.valid_reservation_data['cardnum'],
            'expiry_date_month': self.valid_reservation_data['cardmonth'],
            'expiry_date_year':  self.valid_reservation_data['cardyear'],
            })
        session.save()

        response = c.get(reverse('submitreservation'))

        self.assertTrue(response.context['reservation_placed'])
