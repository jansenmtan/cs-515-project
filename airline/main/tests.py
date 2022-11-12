import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Customer, City, Flight, Reservation

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

