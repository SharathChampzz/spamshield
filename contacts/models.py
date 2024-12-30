from django.db import models
import uuid
from accounts.models import User


class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, db_index=True)
    phone_number = models.CharField(max_length=15, db_index=True)
    added_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="contacts"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        db_table = "contacts"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["phone_number"]),
        ]
        unique_together = ["phone_number", "added_by"]

    def __str__(self):
        return f"{self.name} ({self.phone_number})"


class SpamReport(models.Model):
    class Category(models.TextChoices):
        UNCLASSIFIED = "unclassified", "Unclassified"
        FRAUD = "fraud", "Fraud"
        TELEMARKETER = "telemarketer", "Telemarketer"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reporter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="spam_reports"
    )
    phone_number = models.CharField(max_length=15, db_index=True)
    category = models.CharField(
        max_length=20, choices=Category.choices, default=Category.UNCLASSIFIED
    )
    comment = models.TextField(blank=True, null=True)
    reported_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        db_table = "spam_reports"
        indexes = [
            models.Index(fields=["phone_number"]),
            models.Index(fields=["category"]),
        ]
