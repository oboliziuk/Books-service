from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from borrow_service.models import Borrowing
from borrow_service.serializers import (
    BorrowingListSerializer,
    BorrowingSerializer,
    BorrowingDetailSerializer,
    CreateBorrowingSerializer,
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_id_str = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")

        if user.is_staff:
            queryset = Borrowing.objects.all()
        else:
            queryset = Borrowing.objects.filter(user=user)

        if user.is_staff and user_id_str and user_id_str.isdigit():
            queryset = queryset.filter(user_id=int(user_id_str))

        if is_active == "true":
            queryset = queryset.filter(actual_return_date__isnull=True)
        elif is_active == "false":
            queryset = queryset.filter(actual_return_date__isnull=False)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        if self.action == "create":
            return CreateBorrowingSerializer

        return BorrowingSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="is_active",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="Filter by active borrowings (true - active, false - returned)",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
