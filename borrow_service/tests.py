from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from borrow_service.models import Borrowing
from book_tracker.models import Book


class BorrowingModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com", password="testpass123"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Author",
            inventory=3,
            daily_fee=2.5,
        )
        self.expected_return_date = timezone.now().date() + timedelta(days=7)
        self.borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            expected_return_date=self.expected_return_date,
        )

    def test_borrowing_created_correctly(self):
        self.assertEqual(self.borrowing.user, self.user)
        self.assertEqual(self.borrowing.book, self.book)
        self.assertEqual(self.borrowing.expected_return_date, self.expected_return_date)
        self.assertIsNone(self.borrowing.actual_return_date)
        self.assertEqual(str(self.borrowing), f"Borrowing: {self.book.title} by {self.user} (Expected return: {self.expected_return_date})")

    def test_return_book_sets_actual_return_date_and_updates_inventory(self):
        initial_inventory = self.book.inventory
        self.borrowing.return_book()
        self.borrowing.refresh_from_db()
        self.book.refresh_from_db()

        self.assertIsNotNone(self.borrowing.actual_return_date)
        self.assertEqual(self.book.inventory, initial_inventory + 1)

    def test_return_book_does_not_change_if_already_returned(self):
        self.borrowing.return_book()
        actual_return_date = self.borrowing.actual_return_date
        book_inventory_after_first_return = self.book.inventory

        self.borrowing.return_book()
        self.borrowing.refresh_from_db()
        self.book.refresh_from_db()

        self.assertEqual(self.borrowing.actual_return_date, actual_return_date)
        self.assertEqual(self.book.inventory, book_inventory_after_first_return)
