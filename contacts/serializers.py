from rest_framework import serializers
from .models import Contact, SpamReport
from accounts.models import User


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ("id", "name", "phone_number")
        read_only_fields = ("id",)


class BulkContactSerializer(serializers.Serializer):
    contacts = ContactSerializer(many=True)

    def create(self, validated_data):
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
    class Meta:
        model = SpamReport
        fields = ("id", "phone_number", "category", "comment", "reported_at")
        read_only_fields = ("id", "reported_at")


class SearchResultSerializer(serializers.ModelSerializer):
    spam_likelihood = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("name", "phone_number", "spam_likelihood", "email")

    def get_spam_likelihood(self, obj):
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
