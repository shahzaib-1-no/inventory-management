from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.


# ---------------------------
# 🔹 User
# ---------------------------
def user_get_absolute_url(self):
    return reverse("user_detail", kwargs={"id": self.pk})


User.add_to_class("get_absolute_url", user_get_absolute_url)


# ---------------------------
# 🔹 Custom Manager
# ---------------------------
class NotificationManager(models.Manager):
    def unread(self):
        return self.filter(is_read=False)

    def read(self):
        return self.filter(is_read=True)

    def for_user(self, user):
        if user.is_superuser:
            return self.all()
        return self.filter(user=user) | self.filter(user__isnull=True)


# ---------------------------
# 🔹 Main Model
# ---------------------------
class Notification(models.Model):
    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "is_read"]),
            models.Index(fields=["notification_type"]),
            models.Index(fields=["category"]),
            models.Index(fields=["created_at"]),
        ]

    # ---------------------------
    # 🔸 Choices
    # ---------------------------
    CATEGORY_CHOICES = [
        ("user", "User"),
        ("product", "Product"),
        ("order", "Order"),
        ("supplier", "Supplier"),
        ("system", "System"),
    ]

    NOTIFICATION_CHOICES = [
        # User-related
        ("user_registered", "New User Registered"),
        ("user_profile_updated", "User Profile Updated"),
        ("user_password_updated", "User Password Updated"),
        ("user_deleted", "User Deleted"),
        # Group-related
        ("group_created", "New Group Created"),
        ("group_updated", "Group Updated"),
        ("group_deleted", "Group Deleted"),
        # Product / Inventory
        ("low_stock", "Product Stock is Low"),
        ("out_of_stock", "Product Out of Stock"),
        ("stock_updated", "Stock Quantity Updated"),
        # Order
        ("new_order", "New Order Received"),
        ("order_shipped", "Order Shipped"),
        ("order_delivered", "Order Delivered"),
        # Supplier
        ("supplier_added", "New Supplier Added"),
        ("supplier_payment_due", "Supplier Payment Due"),
        # System
        ("system_error", "System Error"),
        ("backup_completed", "Backup Completed"),
    ]
    # ---------------------------
    # 🔸 Fields
    # ---------------------------
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="system"
    )
    notification_type = models.CharField(max_length=55, choices=NOTIFICATION_CHOICES)
    message = models.TextField()
    sent_at = models.DateTimeField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    # Generic relation
    content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, null=True, blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object = GenericForeignKey("content_type", "object_id")
    # Custom Manager
    objects = NotificationManager()

    # ---------------------------
    # 🔸 Helper Methods
    # ---------------------------
    def mark_as_read(self):
        self.is_read = True
        self.save(update_fields=["is_read", "updated_at"])

    def mark_as_unread(self):
        self.is_read = False
        self.save(update_fields=["is_read", "updated_at"])

    def __str__(self):
        return (
            f"[{self.category.upper()}] {self.notification_type} → {self.message[:50]}"
        )
