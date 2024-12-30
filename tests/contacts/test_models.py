"""Tests for the models of the contacts app."""

import pytest
from tests.factories.factories import UserFactory, ContactFactory, SpamReportFactory


@pytest.mark.django_db
class TestUserModel:
    """Tests for the User model."""

    def test_user_creation(self):
        """Test creation of a User instance."""
        user = UserFactory()
        assert user.pk is not None
        assert user.is_active is True

    def test_user_str_representation(self):
        """Test string representation of a User instance."""
        user = UserFactory(name="Test User", phone_number="+1234567890")
        assert str(user) == "Test User (+1234567890)"


@pytest.mark.django_db
class TestContactModel:
    """Tests for the Contact model."""

    def test_contact_creation(self):
        """Test creation of a Contact instance."""
        contact = ContactFactory()
        assert contact.pk is not None

    def test_contact_str_representation(self):
        """Test string representation of a Contact instance."""
        contact = ContactFactory(name="Test Contact", phone_number="+1234567890")
        assert str(contact) == "Test Contact (+1234567890)"

    def test_unique_contact_per_user(self):
        """Test that a user cannot have multiple contacts with the same phone number."""
        user = UserFactory()
        contact1 = ContactFactory(added_by=user, phone_number="+1234567890")

        with pytest.raises(Exception):
            ContactFactory(added_by=user, phone_number="+1234567890")


@pytest.mark.django_db
class TestSpamReportModel:
    """Tests for the SpamReport model."""

    def test_spam_report_creation(self):
        """Test creation of a SpamReport instance."""
        spam_report = SpamReportFactory()
        assert spam_report.pk is not None
        assert spam_report.category == "unclassified"

    def test_spam_report_with_custom_category(self):
        """Test creation of a SpamReport instance with a custom category"""
        spam_report = SpamReportFactory(category="fraud")
        assert spam_report.category == "fraud"
