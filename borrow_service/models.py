from django.db import models

from Books_service import settings
from book_tracker.models import Book

# Add the borrowing model with constraints for borrow_date, expected_return_date, and actual_return_date.
# Implement a read serializer with detailed book info
# Implement the list & detail endpoints


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return (f"Borrowing: {self.book.title} by {self.user} "
                f"(Expected return: {self.expected_return_date})")
