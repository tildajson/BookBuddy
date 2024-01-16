from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError

from bookapp.models import Book, AllBooks


class BookModelTest(TestCase):
    """Test book model"""

    def test_default_book_details(self):
        """Test default book details work."""
        book = Book()
        self.assertEqual([book.title, book.current_page, book.total_pages],
                         ['', None, None])

    def test_book_is_related_to_list_of_books(self):
        """Test book is in list of all books."""
        all_books = AllBooks.objects.create()
        book = Book(all_books=all_books,
                    title='Some title',
                    current_page=1,
                    total_pages=255,)
        book.save()
        self.assertIn(book, all_books.book_set.all())

    def test_duplicate_books_are_invalid(self):
        """Test duplicate book titles returns error."""
        all_books = AllBooks.objects.create()
        Book.objects.create(all_books=all_books,
                            title='Duplicate',
                            current_page=10,
                            total_pages=25,)

        with self.assertRaises(ValidationError):
            book = Book(all_books=all_books,
                        title='Duplicate',
                        current_page=10,
                        total_pages=25,)
            book.full_clean()

    def test_can_save_the_same_book_to_different_list(self):
        """Test same book can be saved to multiple lists."""
        all_books_first = AllBooks.objects.create()
        all_books_second = AllBooks.objects.create()
        Book.objects.create(all_books=all_books_first,
                            title='Duplicate',
                            current_page=10,
                            total_pages=25,)
        book = Book(all_books=all_books_second,
                    title='Duplicate',
                    current_page=10,
                    total_pages=25,)
        book.full_clean()


class AllBooksModelTest(TestCase):
    """Test all books model."""

    def test_get_absolute_url(self):
        """Test get absolute url works."""
        all_books = AllBooks.objects.create()
        self.assertEqual(all_books.get_absolute_url(), '/')
