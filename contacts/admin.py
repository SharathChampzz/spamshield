"""This module contains the admin configuration for the contacts app."""

from django.contrib import admin
from .models import Contact, SpamReport

# Register your models here.

admin.site.register(Contact)
admin.site.register(SpamReport)
