from typing import cast

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.test import APITestCase

from accounts.models import User


class AuthenticationAPITestCase(APITestCase):
    def setUp(self):
        self.username = 'foo'
        self.password = 'bar'
        self.email = 'foo@bar.com'

        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            email=self.email,
        )

    def test_signup_with_non_matching_password_fields(self):
        data = {
            'username': 'test',
            'email': 'test@todoapi.com',
            'password': 'string',
            'password2': 'different_string',
        }
        response = self.client.post(reverse('signup'), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup(self):
        data = {
            'username': 'test',
            'email': 'test@todoapi.com',
            'password': 'string',
            'password2': 'string',
        }
        response = cast(
            Response, self.client.post(reverse('signup'), data=data)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.data is not None
        self.assertTrue(
            User.objects.filter(id=response.data['user_id']).exists()
        )

    def test_login_with_incorrect_credentials(self):
        data = {
            'username': 'foo',
            'password': 'not_bar',
        }
        response = self.client.post(reverse('login'), data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login(self):
        data = {
            'username': 'foo',
            'password': 'bar',
        }
        response = cast(Response, self.client.post(reverse('login'), data=data))

        assert response.data is not None
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user_id'], self.user.pk)
        self.assertTrue(Token.objects.exists())

    def test_unauthorized_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)  # type: ignore

        response = self.client.get(reverse('logout'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(pk=token.pk).exists())
