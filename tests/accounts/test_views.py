import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from tests.factories.factories import UserFactory
from accounts.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client):
    user = UserFactory()
    api_client.force_authenticate(user=user)
    return api_client, user


@pytest.mark.django_db
class TestUserRegistration:
    def test_successful_registration(self, api_client):
        url = reverse("register")
        data = {
            "name": "Test User",
            "phone_number": "+1234567890",
            "password": "testpass123",
            "email": "test@example.com",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(phone_number=data["phone_number"]).exists()

    def test_duplicate_phone_number(self, api_client):
        existing_user = UserFactory()
        url = reverse("register")
        data = {
            "name": "Another User",
            "phone_number": existing_user.phone_number,
            "password": "testpass123",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_invalid_phone_number(self, api_client):
        url = reverse("register")
        data = {
            "name": "Test User",
            "phone_number": "invalid",
            "password": "testpass123",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserLogin:
    def test_successful_login(self, api_client):
        password = "testpass123"
        user = UserFactory(password=password)
        url = reverse("login")
        data = {"phone_number": user.phone_number, "password": password}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_invalid_credentials(self, api_client):
        password = "testpass123"
        user = UserFactory(password=password)
        url = reverse("login")
        data = {"phone_number": user.phone_number, "password": "wrongpass"}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUserProfile:
    def test_get_profile(self, authenticated_client):
        client, user = authenticated_client
        url = reverse("profile")
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["phone_number"] == user.phone_number
        assert response.data["name"] == user.name

    def test_update_profile(self, authenticated_client):
        client, user = authenticated_client
        url = reverse("profile")
        data = {"name": "Updated Name", "email": "updated@example.com"}
        response = client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.name == data["name"]
        assert user.email == data["email"]

    def test_unauthorized_access(self, api_client):
        url = reverse("profile")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
