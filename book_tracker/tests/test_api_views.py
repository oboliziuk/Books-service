from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from book_tracker.models import Book


class BaseBookTest(APITestCase):
    def create_book(self, **kwargs):
        defaults = {
            "title": "Some Title",
            "author": "Some Author",
            "cover": Book.CoverType.SOFT,
            "inventory": 1,
            "daily_fee": 1.0
        }
        defaults.update(kwargs)
        return Book.objects.create(**defaults)


class UnauthenticatedBookViewTest(BaseBookTest, APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.book1 = Book.objects.create(
            title="The first Book",
            author="First Author",
            cover=Book.CoverType.HARD,
            inventory=2,
            daily_fee=1.5
        )

        self.book2 = Book.objects.create(
            title="The second Book",
            author="Second Author",
            cover=Book.CoverType.SOFT,
            inventory=1,
            daily_fee=1.7
        )

    def test_list_books_with_title_filter(self):
        url = reverse("book_tracker:book-list") + "?title=First"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "The first Book")

    def test_retrieve_book_allowed_for_any_user(self):
        url = reverse("book_tracker:book-detail", args=[self.book1.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book1.title)


class AuthenticatedBookViewTest(BaseBookTest, APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@test.com", password="userpass"
        )
        self.client.force_authenticate(user=self.user)

    def test_non_admin_cannot_create_book(self):
        payload = {
            "title": "Unauthorized Book",
            "author": "No Admin",
            "cover": "HARD",
            "inventory": 1,
            "daily_fee": 1.0
        }
        url = reverse("book_tracker:book-list")
        response = self.client.post(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_admin_cannot_delete_book(self):
        book = self.create_book(title="Book to delete")
        url = reverse("book_tracker:book-detail", args=[book.pk])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Book.objects.filter(id=book.id).exists())


class AdminBookApiTest(BaseBookTest, APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@test.com", password="adminpass"
        )
        self.client.force_authenticate(user=self.admin_user)

    def test_create_book_requires_admin_permission(self):
        payload = {
            "title": "Test Book",
            "author": "Test Author",
            "cover": "HARD",
            "inventory": 1,
            "daily_fee": 1.5
        }

        res = self.client.post(reverse("book_tracker:book-list"), data=payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        book = Book.objects.get(pk=res.data["id"])
        self.assertEqual(book.title, payload["title"])

    def test_update_book_requires_admin_permission(self):
        book = self.create_book(title="Old book")

        url = reverse("book_tracker:book-detail", args=[book.pk])
        payload = {"title": "Updated Title"}

        response = self.client.patch(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book.refresh_from_db()
        self.assertEqual(book.title, "Updated Title")
