from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid

# Create your models here.


class Supplier(models.Model):
    PAYMENT_TERMS_CHOICES = [
        ("Net 15", "Net 15 days"),
        ("Net 30", "Net 30 days"),
        ("COD", "Cash on Delivery"),
        ("Advance 50%", "Advance 50%"),
        ("Imediate", "Imediate"),
    ]

    supplier_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_terms = models.CharField(
        max_length=100, choices=PAYMENT_TERMS_CHOICES, default="Imediate"
    )
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="suppliers_created",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="suppliers_updated",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "suppliers"
        ordering = ["-created_at"]
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"
        permissions = [
            ("ledger_supplier", "Can view supplier ledger"),
        ]

    def __str__(self):
        return self.supplier_name


class Category(models.Model):
    category_name = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Enter the name of the category",
    )
    parent_category = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="sub_categories",
        null=True,
        blank=True,
        help_text="Select parent category if this is a sub-category",
    )
    is_active = models.BooleanField(
        default=True, help_text="Active categories are visible"
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="category_created",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="category_updated",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "categories"
        ordering = ["-created_at"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        indexes = [
            models.Index(fields=["category_name"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["category_name", "parent_category"],
                name="unique_category_per_parent",
            )
        ]

    def __str__(self):
        if self.parent_category:
            return f"{self.parent_category} -> {self.category_name}"
        return self.category_name

    def clean(self):
        if self.parent_category and self.parent_category == self:
            raise ValidationError("Category cannot be its own parent.")

    def save(self, *args, **kwargs):
        self.full_clean()  # runs clean() and field validations
        super().save(*args, **kwargs)


class Warehouse(models.Model):
    warehouse_name = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="warehouse_created",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="warehouse_updated",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.warehouse_name


def product_image_upload(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"products/images/{filename}"


class Product(models.Model):
    image = models.ImageField(upload_to=product_image_upload, null=True, blank=True)
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, related_name="products"
    )
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, related_name="products"
    )
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2)
    measure = models.CharField(max_length=100)
    stock = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    manufacture_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="product_created",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="product_updated",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products"
        ordering = ["-created_at"]

    def __str__(self):
        return self.product_name

    @property
    def is_expired(self):
        return self.expiry_date and self.expiry_date < timezone.now().date()

    def clean(self):

        if self.stock < 0:
            raise ValidationError({"stock": "Stock can not be negative."})

        if (
            self.expiry_date
            and self.manufacture_date
            and self.expiry_date < self.manufacture_date
        ):
            raise ValidationError(
                {"expiry_date": "Expiry date can not be less than manufacture date."}
            )

        if self.selling_price < self.purchase_price:
            raise ValidationError(
                {"selling_price": "Selling price can not be less than purchase price."}
            )

    def save(self, *args, **kwargs):
        if self.stock <= 0:
            self.is_active = False
        super().save(*args, **kwargs)
