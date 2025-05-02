from django.test import TestCase
from book_tracker.models import Book


class BookModelTest(TestCase):
    def setUp(self):
        self.title = "Test Book"
        self.author = "Test Author"
        self.cover = Book.CoverType.HARD
        self.inventory = 2
        self.daily_fee = 0.5

        self.book = Book.objects.create(
            title=self.title,
            author=self.author,
            cover=self.cover,
            inventory=self.inventory,
            daily_fee=self.daily_fee,
        )

    def test_book_creation_with_valid_data(self):
        self.assertEqual(self.book.title, self.title)
        self.assertEqual(self.book.author, self.author)
        self.assertEqual(self.book.cover, self.cover)
        self.assertEqual(self.book.inventory, self.inventory)
        self.assertEqual(self.book.daily_fee, self.daily_fee)
        self.assertEqual(str(self.book), f"{self.title} by {self.author} (ID: {self.book.id})")

    def test_str_method_returns_correct_string(self):
        book = Book.objects.create(
            title="New Book",
            author="New Author",
            cover=Book.CoverType.SOFT,
            inventory=2,
            daily_fee=1.2
        )

        expected_string = f"{book.title} by {book.author} (ID: {book.id})"
        self.assertEqual(str(book), expected_string)

    def test_cover_field_accepts_valid_choices(self):
        book = Book.objects.create(
            title="New Book",
            author="New Author",
            cover=Book.CoverType.SOFT,
            inventory=2,
            daily_fee=1.2
        )

        self.assertEqual(book.cover, Book.CoverType.SOFT)

    def test_inventory_defaults_to_zero(self):
        book = Book.objects.create(
            title="New Book",
            author="New Author",
            cover=Book.CoverType.SOFT,
            daily_fee=1.2
        )

        self.assertEqual(book.inventory, 0)
