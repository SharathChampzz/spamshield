"""
Module for pytest fixtures.
"""

import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


@pytest.fixture
def authenticated_client():
    """
    Fixture to provide an authenticated client.
    """
    user = User.objects.create_user(phone_number="4321876509", password="testpassword")
    client = APIClient()

    response = client.post(
        reverse("login"),
        {"phone_number": "4321876509", "password": "testpassword"},
    )
    token = response.data["access"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client, user
