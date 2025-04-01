from rest_framework import serializers
from book_tracker.models import Book


class BookSerializer(serializers.ModelSerializer):
    cover = serializers.ChoiceField(choices=Book.CoverType.choices)

    class Meta:
        model = Book
        fields = ("id", "title", "author", "cover", "inventory", "daily_fee")


class BookDetailSerializer(BookSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "cover", "inventory", "daily_fee")


class BookListSerializer(BookSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "inventory",)
