"""Factories for generating test data."""

from faker import Faker
import factory
from factory.django import DjangoModelFactory
from accounts.models import User
from contacts.models import Contact, SpamReport

fake = Faker()


class UserFactory(DjangoModelFactory):
    """Factory for generating User instances."""

    class Meta:
        """Meta class for the UserFactory."""

        model = User

    name = factory.Faker("name")
    phone_number = factory.LazyFunction(lambda: fake.unique.phone_number()[:15])
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "testpass123")
    status = User.Status.ENABLED


class ContactFactory(DjangoModelFactory):
    """Factory for generating Contact instances."""

    class Meta:
        """Meta class for the ContactFactory."""

        model = Contact

    name = factory.Faker("name")
    phone_number = factory.LazyFunction(lambda: fake.unique.phone_number()[:15])
    added_by = factory.SubFactory(UserFactory)


class SpamReportFactory(DjangoModelFactory):
    """Factory for generating SpamReport instances."""

    class Meta:
        """Meta class for the SpamReportFactory."""

        model = SpamReport

    reporter = factory.SubFactory(UserFactory)
    phone_number = factory.LazyFunction(lambda: fake.unique.phone_number()[:15])
    category = SpamReport.Category.UNCLASSIFIED
    comment = factory.Faker("sentence")
