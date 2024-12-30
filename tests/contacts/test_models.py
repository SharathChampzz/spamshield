import pytest
from tests.factories.factories import UserFactory, ContactFactory, SpamReportFactory

@pytest.mark.django_db
class TestUserModel:
    def test_user_creation(self):
        user = UserFactory()
        assert user.pk is not None
        assert user.is_active is True

    def test_user_str_representation(self):
        user = UserFactory(name="Test User", phone_number="+1234567890")
        assert str(user) == "Test User (+1234567890)"

@pytest.mark.django_db
class TestContactModel:
    def test_contact_creation(self):
        contact = ContactFactory()
        assert contact.pk is not None

    def test_contact_str_representation(self):
        contact = ContactFactory(name="Test Contact", phone_number="+1234567890")
        assert str(contact) == "Test Contact (+1234567890)"

    def test_unique_contact_per_user(self):
        user = UserFactory()
        contact1 = ContactFactory(added_by=user, phone_number="+1234567890")
        
        with pytest.raises(Exception):
            ContactFactory(added_by=user, phone_number="+1234567890")

@pytest.mark.django_db
class TestSpamReportModel:
    def test_spam_report_creation(self):
        spam_report = SpamReportFactory()
        assert spam_report.pk is not None
        assert spam_report.category == 'unclassified'

    def test_spam_report_with_custom_category(self):
        spam_report = SpamReportFactory(category='fraud')
        assert spam_report.category == 'fraud'