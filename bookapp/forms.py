from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from bookapp.models import Book

ERROR_NO_INPUT = "This field is required."
ERROR_DUPLICATE_BOOKS = "This book already exists on your list."
ERROR_DUPLICATE_USERS = "A user with that username already exists."


class BookForm(ModelForm):
    """Form for creating books."""
    class Meta:
        model = Book
        fields = ["title", "current_page", "total_pages", "user", "all_books"]
        widgets = {
            "title": forms.fields.TextInput(attrs={
                "placeholder": "Book Title",
                "class": "form-control input-lg",
            }),
            "current_page": forms.fields.NumberInput(attrs={
                "placeholder": "Current page",
                "class": "form-control input-lg",
            }),
            "total_pages": forms.fields.NumberInput(attrs={
                "placeholder": "Total pages",
                "class": "form-control input-lg",
            }),
        }
        error_messages = {
            "title": {"required": ERROR_NO_INPUT,
                      "unique_together": ERROR_DUPLICATE_BOOKS},
            "current_page": {"required": ERROR_NO_INPUT},
            "total_pages": {"required": ERROR_NO_INPUT},
        }

    def save(self, for_list):
        self.instance.all_books = for_list
        return super().save()


class BooksInList(BookForm):
    """Return existing books in list."""

    def __init__(self, for_list, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.all_books = for_list
        self.user = user

    def validate_unique(self):
        """Check for duplicate book titles in list."""
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {"title": [ERROR_DUPLICATE_BOOKS]}
            self._update_errors(e)

    def save(self):
        return ModelForm.save(self)


class UserForm(UserCreationForm):
    """Form for creating new users."""
    first_name = forms.CharField(
        label="First name", required=True, widget=forms.TextInput)
    email = forms.EmailField(label="Email", widget=forms.EmailInput)

    class Meta:
        model = User
        fields = ("username", "first_name", "email", "password1", "password2")
        help_texts = {
            "username": None,
            "password": None,
        }

    def validate_unique(self):
        """Check for duplicate usernames."""
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {"username": [ERROR_DUPLICATE_USERS]}
            self._update_errors(e)
