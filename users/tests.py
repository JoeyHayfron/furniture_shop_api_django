from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
import json
from .models import User
from rest_framework_simplejwt.tokens import AccessToken


# Create your tests here.
class UserViewTestCase(TestCase):

    def setUp(self):
        self.test_user = User.objects.create(
            first_name="Test",
            last_name="User1",
            email="testuser1@gmail.com",
            username="testuser1",
            password="testuser1",
        )
        self.admin_user = User.objects.create(
            first_name="Admin",
            last_name="User",
            email="adminuser@gmail.com",
            password="admin_user",
            is_staff=True,
            is_superuser=True,
        )
        self.register_url = reverse("register-user")
        self.users_url = reverse("get-all-users")
        self.get_user_url = reverse("get-or-update-user", args=[self.test_user.id])
        self.client = APIClient()

    def tearDown(self):
        User.objects.all().delete()

    def test_user_registration_successful(self):
        response = self.client.post(
            self.register_url,
            json.dumps(
                {
                    "first_name": "Test",
                    "last_name": "User",
                    "email": "testuser@gmail.com",
                    "username": "testuser",
                    "password": "testuser",
                    "provider": "password",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        # Test to see if the user is authenticated(token was generated and included in the response)
        self.assertIsNotNone(response.data.get("access_token"))

    def test_user_registration_failed(self):
        user_details = {
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@gmail.com",
            "username": "testuser",
            "password": "testuser",
        }
        response = self.client.post(
            self.register_url,
            json.dumps(user_details),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data.get("message"), "provider is required to register a user"
        )
        user_details["provider"] = "password"
        first_user = self.client.post(
            self.register_url,
            json.dumps(user_details),
            content_type="application/json",
        )
        second_user = self.client.post(
            self.register_url,
            json.dumps(user_details),
            content_type="application/json",
        )
        self.assertEqual(second_user.status_code, 400)
        self.assertEqual(
            second_user.data.get("message"),
            "User with this email or username already exists",
        )

    def test_fetching_all_users(self):
        token = AccessToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token)}")
        response = self.client.get(self.users_url, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get("results")), 2)

    def test_fetching_a_user(self):
        token = AccessToken.for_user(self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token)}")
        response = self.client.get(self.get_user_url, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("email"), self.test_user.email)

    def test_updating_user_details(self):
        update_data = {"phone_number": 201513130}
        token = AccessToken.for_user(self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token)}")
        response = self.client.patch(
            self.get_user_url,
            data=json.dumps(update_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("phone_number"), 201513130)
