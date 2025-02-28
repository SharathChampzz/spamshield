"""Tests for the views of the contacts app."""

from django.urls import reverse
from rest_framework import status
from tests.factories.factories import UserFactory, ContactFactory, SpamReportFactory
import pytest


@pytest.mark.django_db
class TestSearchViews:
    """Tests for the search views."""

    def test_search_by_name(self, authenticated_client):
        """Test searching for contacts or users by name."""
        client, user = authenticated_client
        contact = ContactFactory(added_by=user, name="John Doe")
        other_user = UserFactory(name="John Smith")

        url = reverse("search-by-name")
        response = client.get(f"{url}?query=John")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        names = [item["name"] for item in response.data]
        assert "John Doe" in names
        assert "John Smith" in names

    def test_search_by_phone(self, authenticated_client):
        """Test searching for contacts or users by phone number."""
        client, user = authenticated_client
        contact = ContactFactory(added_by=user)

        url = reverse("search-by-phone")
        response = client.get(f"{url}?query={contact.phone_number}")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["phone_number"] == contact.phone_number


@pytest.mark.django_db
class TestSpamReporting:
    """Tests for the spam reporting views."""

    def test_mark_as_spam(self, authenticated_client):
        """Test marking a phone number as spam."""
        client, user = authenticated_client
        url = reverse("spam-report")
        data = {
            "phone_number": "+1234567890",
            "category": "fraud",
            "comment": "Suspicious activity",
        }
        response = client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_unmark_spam(self, authenticated_client):
        """Test unmarking a phone number as spam."""
        client, user = authenticated_client
        spam_report = SpamReportFactory(reporter=user)
        url = reverse("unmark-spam", kwargs={"phone_number": spam_report.phone_number})
        response = client.put(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestContactSync:
    """Tests for the contact sync view."""

    def test_sync_contacts(self, authenticated_client):
        """Test syncing contacts from the user's device."""
        client, user = authenticated_client
        url = reverse("contact-sync")
        data = {
            "contacts": [
                {"name": "Contact 1", "phone_number": "+1234567890"},
                {"name": "Contact 2", "phone_number": "+0987654321"},
            ]
        }
        response = client.post(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert user.contacts.count() == 2

    def test_update_existing_contact(self, authenticated_client):
        """Test updating an existing contact."""
        client, user = authenticated_client
        contact = ContactFactory(added_by=user, name="Old Name")
        url = reverse("contact-sync")
        data = {
            "contacts": [{"name": "New Name", "phone_number": contact.phone_number}]
        }
        response = client.post(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        contact.refresh_from_db()
        assert contact.name == "New Name"


@pytest.mark.django_db
class TestPhoneDetails:
    """Tests for the phone details view."""

    def test_get_phone_details(self, authenticated_client):
        """Test getting details of a phone number."""
        client, user = authenticated_client
        contact = ContactFactory(added_by=user)
        spam_report = SpamReportFactory(phone_number=contact.phone_number)

        url = reverse("phone-details", kwargs={"phone_number": contact.phone_number})
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["phone_number"] == contact.phone_number
        assert response.data["name"] == contact.name
        assert response.data["spam_status"] in ["NotSPAM", "LikelySPAM", "SPAM"]
        assert response.data["added_by_user"] is True
