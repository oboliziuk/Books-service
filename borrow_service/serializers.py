from rest_framework import serializers

from book_tracker.serializers import BookDetailSerializer
from borrow_service.models import Borrowing
from django.contrib.auth import get_user_model

from user.serializers import UserSerializer

User = get_user_model()


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )


class BorrowingListSerializer(BorrowingSerializer):
    book_title = serializers.CharField(source="book.title", read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_title",
            "user_email",
            "is_active",
        )

    def get_is_active(self, obj):
        return obj.actual_return_date is None


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookDetailSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )

    def get_book(self, obj):
        return {
            "id": obj.book.id,
            "title": obj.book.title,
            "author": obj.book.author,
            "daily_fee": obj.book.daily_fee,
        }

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "email": obj.user.email,
        }


class BorrowingReturnSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = ["actual_return_date"]

    def validate_actual_return_date(self, value):
        instance = self.instance
        if value < instance.borrow_date:
            raise serializers.ValidationError("The return date cannot be earlier than the borrowing date.")
        return value
