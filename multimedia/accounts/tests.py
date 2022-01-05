from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework import status
from .models import Category, Music, Movie
AUTH_URL = reverse("accounts:auth")
MEDIA_URL = reverse("accounts:media")


def create_user(**params):
    return get_user_model().objects.create_user(**params)

def create_test_data():
    category = Category.objects.create(title="Criminal")
    Music.objects.create(title="TEST-music-1", category=category)
    Movie.objects.create(title="TEST-movie-1", category=category)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "test@test.com"
        password = "TestPass123"
        user = get_user_model().objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "TestPass123")

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            "test@test.com",
            "TestPass123"
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_user_with_valid_email(self):
        """Test creating user that already exists fails"""
        payload = {"email": "test@test.com", "password": "testpass"}
        create_user(**payload)
        # creating user with API using same credentials
        res = self.client.post(AUTH_URL, payload, format="json")
        self.assertTrue(res.data["success"])
        self.assertTrue(res.status_code, status.HTTP_200_OK)

    def test_auth_user_with_invalid_email(self):
        """Test that the password must be more than 8 characters. This is default 8 character limit by Django."""
        payload = {"email": "invalid@test.com", "password": "testpass"}
        res = self.client.post(AUTH_URL, {"email": "invalid@test.com"}, format="json")
        self.assertFalse(res.data["success"])
        self.assertTrue(res.status_code, status.HTTP_404_NOT_FOUND)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self, *args, **kwargs):
        if 'user' in kwargs:
            user = kwargs['user']
            token = Token.objects.create(user=user).key
            self.client = APIClient()
            self.client.force_authenticate(user=user)
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
            return user

    def test_auth_successfully(self):
        """Test auth user"""
        payload = {"email": "test@test.com", "password": "testpass"}
        user = create_user(**payload)
        self.setUp(user=user)
        auth_user = Token.objects.get(user=user)
        self.assertEquals(user.email, auth_user.user.email)

    def test_auth_failed(self):
        """Test auth user failed"""
        res = self.client.get(MEDIA_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_data_success(self):
        """Test media info for logged in user"""
        payload = {"email": "test@test.com", "password": "testpass"}
        user = create_user(**payload)
        self.setUp(user=user)
        create_test_data()
        res = self.client.get(MEDIA_URL)
        self.assertTrue(res.data["success"])