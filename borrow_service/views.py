from django.shortcuts import render
from rest_framework import viewsets
from borrow_service.models import Borrowing
from borrow_service.serializers import (
    BorrowingListSerializer,
    BorrowingSerializer,
    BorrowingDetailSerializer,
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    def get_queryset(self):
        is_active = self.request.query_params.get("is_active")
        user_id_str = self.request.query_params.get("user")

        queryset = self.queryset

        if is_active == "true":
            queryset = queryset.filter(actual_return_date__isnull=True)
        elif is_active == "false":
            queryset = queryset.filter(actual_return_date__isnull=False)

        if user_id_str and user_id_str.isdigit():
            queryset = queryset.filter(user_id=int(user_id_str))

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer

        if self.action == "retrieve":
            return BorrowingDetailSerializer

        return BorrowingSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

