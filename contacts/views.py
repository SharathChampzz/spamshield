from django.db.models import Q, Count, Value, CharField
from django.db.models.functions import Concat
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Contact, SpamReport
from accounts.models import User
from .serializers import (
    ContactSerializer,
    SpamReportSerializer,
    SearchResultSerializer,
    PhoneDetailsSerializer,
    BulkContactSerializer,
)


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class SearchView(generics.ListAPIView):
    """
    View to search for contacts or users based on a query string.
    """

    serializer_class = SearchResultSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "query",
                openapi.IN_QUERY,
                description="Search query string",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="Page number",
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
            openapi.Parameter(
                "size",
                openapi.IN_QUERY,
                description="Number of items per page",
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        query = self.request.query_params.get("query", "")
        print(f"Query ==>: {query}")

        # Search in User table
        user_results = User.objects.filter(
            Q(name__icontains=query) | Q(phone_number__icontains=query)
        )

        # Search in Contact table
        contact_results = Contact.objects.filter(
            Q(name__icontains=query) | Q(phone_number__icontains=query)
        )

        # Combine the results, with User results first
        combined_results = list(user_results) + list(contact_results)

        # Pagination
        page = self.request.query_params.get("page", 1)
        size = self.request.query_params.get("size", 10)
        start = (int(page) - 1) * int(size)
        end = start + int(size)
        return combined_results[start:end]


class PhoneSearchView(generics.ListAPIView):
    serializer_class = SearchResultSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "query",
                openapi.IN_QUERY,
                description="Search query string",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="Page number",
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
            openapi.Parameter(
                "size",
                openapi.IN_QUERY,
                description="Number of items per page",
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        phone_number = self.request.query_params.get("query", "")
        if not phone_number:
            return User.objects.none()

        # Search in User table
        user_results = User.objects.filter(phone_number__icontains=phone_number)

        # Search in Contact table
        contact_results = Contact.objects.filter(phone_number__icontains=phone_number)

        # Combine the results, with User results first
        combined_results = list(user_results) + list(contact_results)

        # Pagination
        page = self.request.query_params.get("page", 1)
        size = self.request.query_params.get("size", 10)
        start = (int(page) - 1) * int(size)
        end = start + int(size)
        return combined_results[start:end]


class SpamReportView(generics.CreateAPIView):
    serializer_class = SpamReportSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)


class UnmarkSpamView(generics.UpdateAPIView):
    """
    View to unmark a phone number as spam.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = SpamReportSerializer

    def update(self, request, *args, **kwargs):
        phone_number = kwargs.get("phone_number")
        SpamReport.objects.filter(
            reporter=request.user, phone_number=phone_number
        ).delete()
        return Response(status=status.HTTP_200_OK)


class ContactSyncView(generics.CreateAPIView):
    serializer_class = BulkContactSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"message": "Contacts synced successfully"}, status=status.HTTP_200_OK
        )


class PhoneDetailsView(generics.RetrieveAPIView):
    serializer_class = PhoneDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        phone_number = self.kwargs.get("phone_number")
        user = User.objects.filter(phone_number=phone_number).first()
        contact = Contact.objects.filter(phone_number=phone_number).first()
        spam_report = SpamReport.objects.filter(phone_number=phone_number).first()

        # Determine name from user or contact
        name = user.name if user else (contact.name if contact else "Unknown")

        # Calculate spam status
        spam_count = SpamReport.objects.filter(phone_number=phone_number).count()
        if spam_count == 0:
            spam_status = "NotSPAM"
        elif spam_count < 3:
            spam_status = "LikelySPAM"
        else:
            spam_status = "SPAM"

        return {
            "phone_number": phone_number,
            "name": name,
            "spam_status": spam_status,
            "spam_report": spam_report,
            "added_by_user": bool(user or contact),
        }
