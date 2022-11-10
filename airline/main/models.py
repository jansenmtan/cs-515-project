# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up: (ALL DONE)
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Customer(models.Model):
    cid = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=80)
    email = models.CharField(unique=True, max_length=40)
    address = models.CharField(max_length=200, blank=True, null=True)
    password = models.CharField(max_length=16)

    class Meta:
        managed = False
        db_table = 'Customer'


class City(models.Model):
    cityid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    state = models.CharField(max_length=2)

    class Meta:
        managed = False
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

    class Meta:
        managed = False
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

    class Meta:
        managed = False
        db_table = 'Reservation'
