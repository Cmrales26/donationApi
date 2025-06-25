from django.db import models


# Create your models here.
class Task(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    delivery_date = models.DateField()
    order = models.PositiveIntegerField(blank=True, null=True)

    campaign = models.ForeignKey(
        "campaign.Campaign", on_delete=models.CASCADE, related_name="tasks"
    )

    beneficiary = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="tasks"
    )

    class Meta:
        ordering = ["order"]
