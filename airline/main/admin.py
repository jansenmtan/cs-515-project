from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models, forms


class CustomerUserAdmin(UserAdmin):
    add_form = forms.CustomerCreationForm
    form = forms.CustomerChangeForm

    model = models.Customer

    list_display = ('email', 'cname', 'is_superuser', 'is_active',)
    list_filter  = ('email', 'cname', 'is_superuser', 'is_active',)

    fieldsets = (
            (None,          {'fields': ('email', 'cname', 'password')}),
            ('Permissions', {'fields': ('is_active',)}),
            )
    add_fieldsets = (
            (
                None,
                {
                'classes': ('wide',),
                'fields': ('email', 'cname', 'password1', 'password2', 'is_active',),
                }
                ),
            )

    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(models.Customer, CustomerUserAdmin)
admin.site.register(models.City)
admin.site.register(models.Flight)
admin.site.register(models.Reservation)
