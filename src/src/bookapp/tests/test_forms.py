from django.test import TestCase, Client
from django.contrib.auth.models import User
from bookapp.forms import (BookForm, BooksInList, UserForm,
                           ERROR_NO_INPUT, ERROR_DUPLICATE_BOOKS)
from bookapp.models import AllBooks, Book


class BookFormTest(TestCase):
    """Test book form."""

    def test_validation_for_blank_book_details_input(self):
        """Test leaving empty fields gives error."""
        form = BookForm(
            data={'title': '', 'current_page': 45, 'total_pages': 500, })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['title'], [ERROR_NO_INPUT])

        form = BookForm(data={'title': 'Some title',
                        'current_page': '', 'total_pages': '', })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['current_page'], [ERROR_NO_INPUT])

        form = BookForm(data={'title': 'Some title',
                        'current_page': 20, 'total_pages': '', })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['total_pages'], [ERROR_NO_INPUT])

    def test_BookForm_handles_saving_to_a_ListOfBooks(self):
        """Test new books are added to list of all books."""
        all_books = AllBooks.objects.create()
        form = BookForm(data={'title': 'Some title',
                        'current_page': 11, 'total_pages': 56, })
        new_book = form.save(for_list=all_books)

        self.assertEqual(new_book, Book.objects.first())
        self.assertEqual(new_book.title, 'Some title')
        self.assertEqual(new_book.all_books, all_books)


class BooksInListTest(TestCase):
    """Test list for existing books."""

    if not User.objects.filter(username='exampleuser').exists():
        user = User.objects.create(username='exampleuser')
        user.set_password('12345test')
        user.save()
    else:
        user = User(username='exampleuser', password='12345test')

    Client().login(username='exampleuser', password='12345test')
