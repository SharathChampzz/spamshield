"""This module contains the URL configuration for the contacts app."""

from django.urls import path
from .views import (
    SearchView,
    PhoneSearchView,
    SpamReportView,
    UnmarkSpamView,
    ContactSyncView,
    PhoneDetailsView,
)

urlpatterns = [
    path("search/", SearchView.as_view(), name="search"),
    path("search-by-name/", SearchView.as_view(), name="search-by-name"),
    path("search-by-phone/", PhoneSearchView.as_view(), name="search-by-phone"),
    path("spam/", SpamReportView.as_view(), name="spam-report"),
    path(
        "spam/unmark/<str:phone_number>/", UnmarkSpamView.as_view(), name="unmark-spam"
    ),
    path("sync/", ContactSyncView.as_view(), name="contact-sync"),
    path(
        "details/<str:phone_number>/", PhoneDetailsView.as_view(), name="phone-details"
    ),
]
