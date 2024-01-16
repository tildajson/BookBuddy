from django.test import TestCase, Client
from django.urls import resolve, reverse
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.utils.html import escape

from unittest import skip

from bookapp.models import Book, AllBooks
from bookapp.forms import (BooksInList, ERROR_NO_INPUT,
                           ERROR_DUPLICATE_BOOKS, ERROR_DUPLICATE_USERS,
                           UserForm)


class RegisterTest(TestCase):
    """Test registration view."""

    def test_uses_register_template(self):
        """Test correct template is used."""
        response = self.client.get('/register/')
        self.assertTemplateUsed(response, 'register.html')

    def test_register_uses_UserRegistrationForm(self):
        """Test registration uses correct form."""
        response = self.client.get('/register/')
        self.assertIsInstance(response.context['form'], UserForm)

    def test_saving_POST_request(self):
        """Test saving user with post request."""
        self.client.post(reverse('register'), data={
            'username': 'usertest',
            'first_name': 'Tilda',
            'email': 'test@example.com',
            'password1': 'password123P()',
            'password2': 'password123P()',
        })

        self.assertEqual(User.objects.count(), 1)
        new_user = User.objects.first()
        self.assertEqual(new_user.username, 'usertest')
        self.assertEqual(new_user.first_name, 'Tilda')
        self.assertEqual(new_user.email, 'test@example.com')
        check_password(new_user.password, 'password123P()')

    def test_invalid_registration_inputs_arent_saved(self):
        """Test invalid data is not saved to database."""
        # invalid email
        self.client.post(reverse('register'), data={
            'username': 'usertest',
            'first_name': 'test',
            'email': 'test.com',
            'password1': 'password123P()',
            'password2': 'password123P()',
        })

        self.assertEqual(User.objects.count(), 0)

        # invalid username
        self.client.post(reverse('register'), data={
            'username': '',
            'first_name': 'test',
            'email': 'test@example.com',
            'password1': 'password123P()',
            'password2': 'password123P()',
        })

        self.assertEqual(User.objects.count(), 0)

        # invalid first_name
        self.client.post(reverse('register'), data={
            'username': 'usertest',
            'first_name': '',
            'email': 'test@example.com',
            'password': 'password123P()',
            'password2': 'password123P()',
        })

        self.assertEqual(User.objects.count(), 0)

        # invalid password1 (too short)
        self.client.post(reverse('register'), data={
            'username': 'usertest',
            'first_name': 'Tilda',
            'email': 'test@example.com',
            'password1': '123',
            'password2': '123',
        })

        self.assertEqual(User.objects.count(), 0)

        # not matching passwords
        self.client.post(reverse('register'), data={
            'username': 'usertest',
            'first_name': 'Tilda',
            'email': 'test@example.com',
            'password1': 'password123P()',
            'password2': 'password123p()',
        })

        self.assertEqual(User.objects.count(), 0)

    def test_displays_UserForm(self):
        """Test user creation form is displayed."""
        response = self.client.get(reverse('register'))

        self.assertIsInstance(response.context['form'], UserForm)
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="password1"')
        self.assertContains(response, 'name="password2"')
