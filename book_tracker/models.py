from django.db import models


class Book(models.Model):
    # COVER_CHOICES = models.TextChoices("HARD", "SOFT")
    class CoverType(models.TextChoices):
        HARD = "HARD", "Hardcover"
        SOFT = "SOFT", "Softcover"

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    cover = models.CharField(max_length=10, choices=CoverType.choices, blank=True)
    inventory = models.PositiveIntegerField(default=0)
    daily_fee = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name_plural = "books"

    def __str__(self):
        return f"{self.title} by {self.author} (ID: {self.id})"
