from rest_framework.test import APITestCase

from book_tracker.models import Book
from book_tracker.serializers import (
    BookSerializer,
    BookDetailSerializer,
    BookListSerializer,
)


class BookSerializerTest(APITestCase):
    def setUp(self):
        self.book_data = {
            "title": "Test Book",
            "author": "Author",
            "cover": Book.CoverType.SOFT,
            "inventory": 5,
            "daily_fee": 0.2
        }
        self.book = Book.objects.create(**self.book_data)

    def test_book_serializer_returns_expected_fields(self):
        serializer = BookSerializer(self.book)

        expected_keys = {"id", "title", "author", "cover", "inventory", "daily_fee"}
        self.assertEqual(expected_keys, set(serializer.data.keys()))

    def test_book_serializer_validates_valid_data(self):
        serializer = BookSerializer(data=self.book_data)

        self.assertTrue(serializer.is_valid())

    def test_book_serializer_validates_invalid_data(self):
        invalid_data = self.book_data.copy()
        invalid_data.pop("title")

        serializer = BookSerializer(data=invalid_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors, {"title": ["This field is required."]})

    def test_book_detail_serializer_includes_all_fields(self):
        serializer = BookDetailSerializer(self.book)

        expected_keys = {"id", "title", "author", "cover", "inventory", "daily_fee"}
        self.assertEqual(expected_keys, set(serializer.data.keys()))

    def test_book_list_serializer_includes_subset_of_fields(self):
        serializer = BookListSerializer(self.book)

        expected_keys = {"id", "title", "author", "inventory"}
        self.assertEqual(expected_keys, set(serializer.data.keys()))

    def test_book_serializer_rejects_invalid_cover(self):
        invalid_data = {
            "title": "Bad Book",
            "author": "Bad Author",
            "cover": "PAPER",
            "inventory": 1,
            "daily_fee": 0.5
        }
        serializer = BookSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("cover", serializer.errors)
