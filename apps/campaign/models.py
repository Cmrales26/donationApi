from django.db import models


# Create your models here.
class Campaign(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("closed", "Closed"),
        ("canceled", "Canceled"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    create_by = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="campaign_creator",
        blank=True,
        null=True,
    )
    updated_by = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="campaign_updater",
        blank=True,
        null=True,
    )
