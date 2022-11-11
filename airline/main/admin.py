from django.contrib import admin

from .models import Customer, City, Flight, Reservation

admin.site.register(Customer)
admin.site.register(City)
admin.site.register(Flight)
admin.site.register(Reservation)
