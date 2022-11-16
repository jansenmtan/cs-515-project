from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from . import managers

class Customer(AbstractBaseUser, PermissionsMixin):
    # fields specified in Design Document
    cname = models.CharField(max_length=80)
    email = models.EmailField(unique=True, max_length=40)
    address = models.CharField(max_length=200, blank=True, null=True)
    #password = models.CharField(max_length=16) # already included in AbstractBaseUser

    # fields specified by Django docs and source
    #   at: https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#substituting-a-custom-user-model
    #   at: https://github.com/django/django/blob/0dd29209091280ccf34e07c9468746c396b7778e/django/contrib/auth/models.py
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['cname']
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # only requred for UserCreationForm and UserChangeForm

    objects = managers.CustomerManager()

    def __str__(self):
        return f"{self.cname}"

    def get_full_name(self):
        return self.cname

    def get_short_name(self):
        # assume cname is "{first_name} {last_name}". only return first_name
        return self.cname.strip().split(" ")[0]

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    class Meta:
        managed = True
        db_table = 'Customer'


class City(models.Model):
    cityid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    state = models.CharField(max_length=2)

    @classmethod
    def get_object_from_string(cls, string):
        (title, state) = string.split(", ")
        return cls.objects.get(title=title, state=state)

    def __str__(self):
        return f"{self.title}, {self.state}"

    class Meta:
        managed = True
        db_table = 'City'


class Flight(models.Model):
    fid = models.AutoField(primary_key=True)
    fnumber = models.IntegerField(blank=True, null=True)
    fdate = models.DateField()
    ftime = models.TimeField()
    price = models.FloatField()
    class_field = models.IntegerField(db_column='class')  # Field renamed because it was a Python reserved word.
    capacity = models.IntegerField()
    available = models.IntegerField()
    orig = models.ForeignKey(City, models.CASCADE, db_column='orig', related_name='cities')
    dest = models.ForeignKey(City, models.CASCADE, db_column='dest')

    def is_available(self):
        return self.available > 0

    def __str__(self):
        return f"{self.fid}: Flight {self.fnumber}: {self.orig} to {self.dest} on {self.fdate} at USD {self.price}"

    class Meta:
        managed = True
        db_table = 'Flight'


class Reservation(models.Model):
    ordernum = models.AutoField(primary_key=True)
    cid = models.ForeignKey(Customer, models.CASCADE, db_column='cid')
    dfid = models.ForeignKey(Flight, models.CASCADE, db_column='dfid', related_name='flights')
    rfid = models.ForeignKey(Flight, models.CASCADE, db_column='rfid', blank=True, null=True)
    qty = models.IntegerField()
    cardnum = models.CharField(max_length=16)
    cardmonth = models.IntegerField()
    cardyear = models.IntegerField()
    order_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.ordernum}"

    class Meta:
        managed = True
        db_table = 'Reservation'
