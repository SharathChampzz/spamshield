import factory
from factory.django import DjangoModelFactory
from accounts.models import User
from contacts.models import Contact, SpamReport
from faker import Faker

fake = Faker()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    name = factory.Faker('name')
    phone_number = factory.LazyFunction(lambda: fake.unique.phone_number()[:15])
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')
    status = User.Status.ENABLED

class ContactFactory(DjangoModelFactory):
    class Meta:
        model = Contact

    name = factory.Faker('name')
    phone_number = factory.LazyFunction(lambda: fake.unique.phone_number()[:15])
    added_by = factory.SubFactory(UserFactory)

class SpamReportFactory(DjangoModelFactory):
    class Meta:
        model = SpamReport

    reporter = factory.SubFactory(UserFactory)
    phone_number = factory.LazyFunction(lambda: fake.unique.phone_number()[:15])
    category = SpamReport.Category.UNCLASSIFIED
    comment = factory.Faker('sentence')