"""Serializers for the contacts app."""

from rest_framework import serializers
from accounts.models import User
from .models import Contact, SpamReport


class ContactSerializer(serializers.ModelSerializer):
    """Serializer for the contact model."""

    class Meta:
        """Meta options."""

        model = Contact
        fields = ("id", "name", "phone_number")
        read_only_fields = ("id",)


class BulkContactSerializer(serializers.Serializer):
    """Serializer for creating multiple contacts."""

    contacts = ContactSerializer(many=True)

    def create(self, validated_data):
        """Create and return a list of contacts."""
        user = self.context["request"].user
        contacts_data = validated_data.get("contacts", [])
        contacts = []

        for contact_data in contacts_data:
            contact, _ = Contact.objects.update_or_create(
                phone_number=contact_data["phone_number"],
                added_by=user,
                defaults={"name": contact_data["name"]},
            )
            contacts.append(contact)

        return contacts


class SpamReportSerializer(serializers.ModelSerializer):
    """Serializer for the spam report model."""

    class Meta:
        """Meta options."""

        model = SpamReport
        fields = ("id", "phone_number", "category", "comment", "reported_at")
        read_only_fields = ("id", "reported_at")


class SearchResultSerializer(serializers.ModelSerializer):
    """Serializer for search results."""

    spam_likelihood = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        """Meta options."""

        model = User
        fields = ("name", "phone_number", "spam_likelihood", "email")

    def get_spam_likelihood(self, obj):
        """Return the spam likelihood of the phone number."""
        if isinstance(obj, User):
            phone_number = obj.phone_number
        else:
            phone_number = obj.phone_number

        spam_count = SpamReport.objects.filter(phone_number=phone_number).count()
        if spam_count == 0:
            return "NotSPAM"
        elif spam_count < 3:
            return "LikelySPAM"
        return "SPAM"

    def get_email(self, obj):
        """Return the email of the user if in contacts."""
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return None

        if isinstance(obj, User):
            # Only show email if the requesting user is in the user's contacts
            has_contact = Contact.objects.filter(
                added_by=obj, phone_number=request.user.phone_number
            ).exists()
            return obj.email if has_contact else None
        return None


class PhoneDetailsSerializer(serializers.Serializer):
    """Serializer for phone details."""

    phone_number = serializers.CharField()
    name = serializers.CharField()
    spam_status = serializers.CharField()
    category = serializers.CharField(
        source="spam_report.category", default="unclassified"
    )
    comment = serializers.CharField(source="spam_report.comment", allow_null=True)
    added_by_user = serializers.BooleanField(default=False)
    reported_at = serializers.DateTimeField(
        source="spam_report.reported_at", allow_null=True
    )
