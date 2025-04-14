from django.utils import timezone

from django.db import models
from Books_service import settings
from book_tracker.models import Book


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

    def return_book(self):
        if self.actual_return_date is None:
            self.actual_return_date = timezone.now().date()
            self.book.inventory += 1
            self.book.save()
            self.save(update_fields=["actual_return_date"])
