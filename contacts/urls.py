"""This module contains the URL configuration for the contacts app."""

from django.urls import path
from .views import (
    SearchByNameView,
    SearchByPhoneNumberView,
    SearchByNameAndPhoneView,
    ReportSpamView,
    UnmarkSpamView,
    ContactSyncView,
    PhoneDetailsView,
)

urlpatterns = [
    path("search-by-name/", SearchByNameView.as_view(), name="search-by-name"),
    path("search-by-phone/", SearchByPhoneNumberView.as_view(), name="search-by-phone"),
    path("search/", SearchByNameAndPhoneView.as_view(), name="search"),
    path("spam/", ReportSpamView.as_view(), name="spam-report"),
    path(
        "spam/unmark/<str:phone_number>/", UnmarkSpamView.as_view(), name="unmark-spam"
    ),
    path("sync/", ContactSyncView.as_view(), name="contact-sync"),
    path(
        "details/<str:phone_number>/", PhoneDetailsView.as_view(), name="phone-details"
    ),
]
