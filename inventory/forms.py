from django import forms
from inventory.models import Supplier, Category, Warehouse, Product
from decimal import Decimal, ROUND_HALF_UP


class SupplierForm(forms.ModelForm):
    PAYMENT_TERMS_CHOICES = [
        ("Net 15", "Net 15 days"),
        ("Net 30", "Net 30 days"),
        ("COD", "Cash on Delivery"),
        ("Advance 50%", "Advance 50%"),
        ("Imediate", "Imediate"),
    ]

    class Meta:
        model = Supplier
        fields = [
            "supplier_name",
            "contact_person",
            "phone_number",
            "email",
            "address",
            "city",
            "opening_balance",
            "payment_terms",
            "is_active",
            "notes",
        ]
        widgets = {
            "supplier_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Supplier Name"}
            ),
            "contact_person": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Contact Person"}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Phone Number"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email Address"}
            ),
            "address": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Address"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "City"}
            ),
            "opening_balance": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Opening Balance"}
            ),
            "is_active": forms.RadioSelect(
                attrs={"class": "form-check-input "},
                choices=[
                    (True, "Active"),
                    (False, "Inactive"),
                ],
            ),
            "notes": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Notes"}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)  # request capture for save()
        super().__init__(*args, **kwargs)
        self.fields["payment_terms"].widget = forms.Select(
            choices=[("", "-- Select Payment Terms --")] + self.PAYMENT_TERMS_CHOICES,
            attrs={"class": "form-control"},
        )

    def clean_supplier_name(self):
        supplier_name = self.cleaned_data.get("supplier_name")

        # exclude current instance (update case)
        qs = Supplier.objects.filter(supplier_name__iexact=supplier_name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("This supplier name is already registered.")
        return supplier_name

    def clean_payment_terms(self):
        payment_terms = self.cleaned_data.get("payment_terms")
        valid_choices = [choice[0] for choice in self.PAYMENT_TERMS_CHOICES]
        if payment_terms and payment_terms not in valid_choices:
            raise forms.ValidationError("Invalid payment terms selected.")
        return payment_terms

    def save(self, commit=True):
        supplier = super().save(commit=False)
        if self.request and self.request.user.is_authenticated:
            supplier.created_by = self.request.user
            supplier.updated_by = self.request.user
        if commit:
            supplier.save()
        return supplier


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            "category_name",
            "parent_category",
            "is_active",
        ]
        widgets = {
            "category_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Category Name"}
            ),
            "parent_category": forms.Select(attrs={"class": "form-select"}),
            "is_active": forms.Select(
                attrs={"class": "form-select"},
                choices=[(True, "Active"), (False, "Inactive")],
            ),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        # Only top-level categories (parent_category is None) can be chosen
        top_categories = Category.objects.filter(parent_category__isnull=True)
        CATEGORY_CHOICES = [(c.id, c.category_name) for c in top_categories]
        self.fields["parent_category"].choices = [
            ("", "-- Select Parent Category --")
        ] + CATEGORY_CHOICES

    def clean_category_name(self):
        category_name = self.cleaned_data.get("category_name")
        qs = Category.objects.filter(category_name__iexact=category_name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This category name is already registered.")
        return category_name

    def clean_parent_category(self):
        parent_category = self.cleaned_data.get("parent_category")
        if parent_category and parent_category == self.instance:
            raise forms.ValidationError("Category cannot be its own parent.")
        # Ensure parent category is top-level
        if parent_category and parent_category.parent_category is not None:
            raise forms.ValidationError("Cannot select a child category as parent.")
        return parent_category

    def save(self, commit=True):
        category = super().save(commit=False)
        if self.request and self.request.user.is_authenticated:
            if not self.instance.pk:  # Only set created_by when new
                category.created_by = self.request.user
            category.updated_by = self.request.user
        if commit:
            category.save()
        return category


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = [
            "warehouse_name",
            "address",
            "city",
            "is_active",
            "notes",
        ]
        widgets = {
            "warehouse_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Warehouse Name"}
            ),
            "address": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Address"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "City"}
            ),
            "is_active": forms.Select(
                attrs={"class": "form-select"},
                choices=[(True, "Active"), (False, "Inactive")],
            ),
            "notes": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Notes"}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def clean_warehouse_name(self):
        warehouse_name = self.cleaned_data.get("warehouse_name")
        qs = Warehouse.objects.filter(warehouse_name__iexact=warehouse_name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This warehouse name is already registered.")
        return warehouse_name

    def save(self, commit=True):
        print(">>> Save method called", self.request.user)
        warehouse = super().save(commit=False)

        if self.request and self.request.user.is_authenticated:
            if not warehouse.pk:  # new object
                warehouse.created_by = self.request.user
            warehouse.updated_by = self.request.user
        if commit:
            warehouse.save()
        return warehouse


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "image",
            "product_name",
            "category",
            "supplier",
            "warehouse",
            "purchase_price",
            "selling_price",
            "tax_rate",
            "measure",
            "stock",
            "is_active",
            "notes",
        ]
        widgets = {
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "product_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Product Name"}
            ),
            "category": forms.Select(attrs={"class": "form-select"}),
            "supplier": forms.Select(attrs={"class": "form-select"}),
            "warehouse": forms.Select(attrs={"class": "form-select"}),
            "purchase_price": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Purchase Price"}
            ),
            "selling_price": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Selling Price"}
            ),
            "tax_rate": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Tax Rate"}
            ),
            "measure": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Measure"}
            ),
            "stock": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Stock"}
            ),
            "is_active": forms.Select(
                attrs={"class": "form-select"},
                choices=[(True, "Active"), (False, "Inactive")],
            ),
            "notes": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Notes"}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self.fields["warehouse"].queryset = Warehouse.objects.filter(is_active=True)
        self.fields["supplier"].queryset = Supplier.objects.filter(is_active=True)
        self.fields["category"].queryset = Category.objects.filter(
            is_active=True, parent_category__isnull=False
        )

    def clean(self):
        cleaned_data = super().clean()
        stock = cleaned_data.get("stock")
        purchase_price = cleaned_data.get("purchase_price")
        selling_price = cleaned_data.get("selling_price")
        tax_rate = cleaned_data.get("tax_rate")

        # Stock validation
        if stock is None or stock <= 0:
            raise forms.ValidationError("Stock cannot be negative or zero.")

        # Purchase vs selling price validation
        if purchase_price is not None and selling_price is not None:
            if selling_price < purchase_price:
                raise forms.ValidationError(
                    "Selling price cannot be less than purchase price."
                )

            #  Apply tax if exists
            if tax_rate is not None:
                tax_amount = (purchase_price * tax_rate) / 100
                selling_price += tax_amount

            # Round to 2 decimals
            selling_price = Decimal(selling_price).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            cleaned_data["selling_price"] = selling_price

        return cleaned_data

    def save(self, commit=True):
        product = super().save(commit=False)
        if self.request and self.request.user.is_authenticated:
            if not product.pk:
                product.created_by = self.request.user
            product.updated_by = self.request.user
        if commit:
            product.save()
        return product
