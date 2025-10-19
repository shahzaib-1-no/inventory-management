from django.shortcuts import render
from inventory.models import (
    Supplier,
    Category,
    Warehouse,
    Product,
)
from inventory.forms import (
    SupplierForm,
    CategoryForm,
    WarehouseForm,
    ProductForm,
)
from django.shortcuts import redirect
from django.db import transaction
from django.contrib import messages
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.utils.html import format_html, mark_safe
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from inventory_management.decorators import permission_required_message
from django.views.decorators.csrf import csrf_exempt
import logging
from django.http import JsonResponse
from django.utils.html import escape

logger = logging.getLogger(__name__)


# Supplier Management VIEWS CRUD Section Start
@login_required
@permission_required_message("inventory.view_supplier", redirect_to="dashboard")
def all_supplier(request):
    return render(request, "inventory/all_supplier.html")


@login_required
@permission_required_message("inventory.add_supplier", redirect_to="all_supplier")
def add_supplier(request):
    if request.method == "POST":
        form = SupplierForm(request.POST, request=request)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    messages.success(request, "Supplier added successfully.")
                    return redirect("all_supplier")
            except Exception as e:
                messages.error(request, f"Error: {e}")
                return redirect("add_supplier")
    else:
        form = SupplierForm(request=request)
    context = {"form": form}
    return render(request, "inventory/add_supplier.html", context)


class SupplierListJson(BaseDatatableView):
    model = Supplier
    columns = [
        "id",
        "supplier_name",
        "contact_person",
        "phone_number",
        "email",
        "status",
        "action",
    ]
    order_columns = columns
    max_display_length = 10

    # Fields to search
    search_fields = [
        "supplier_name",
        "contact_person",
        "phone_number",
        "email",
    ]

    def get_initial_queryset(self):
        logger.info("✅ AJAX request received for SupplierListJson")
        return Supplier.objects.all()

    def filter_queryset(self, qs):
        search_value = self.request.GET.get("search[value]", "").strip()
        if search_value:
            # Handle Active/Inactive search manually
            if search_value.lower() in ["active", "inactive"]:
                is_active = search_value.lower() == "active"
                qs = qs.filter(is_active=is_active)
            else:
                q = Q()
                for field in self.search_fields:
                    q |= Q(**{f"{field}__icontains": search_value})
                qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        data = []
        for index, item in enumerate(qs, start=1):
            data.append(
                {
                    "id": item.id,  # ✅ Needed for checkbox selection
                    "sno": index,
                    "supplier_name": item.supplier_name,
                    "contact_person": item.contact_person,
                    "phone_number": item.phone_number,
                    "email": item.email,
                    "status": self.render_column(item, "status"),
                    "action": self.render_column(item, "action"),
                }
            )
        return data

    def render_column(self, row, column):
        if column == "status":
            return format_html(
                '<span class="badge bg-{}-subtle text-{} border border-{}-subtle px-2 py-1">'
                '<i class="bi bi-{} me-1"></i>{}</span>',
                "success" if row.is_active else "danger",
                "success" if row.is_active else "danger",
                "success" if row.is_active else "danger",
                "check-circle-fill" if row.is_active else "x-circle-fill",
                "Active" if row.is_active else "Inactive",
            )

        if column == "action":
            return format_html(
                """
                <div class="dropdown">
                    <button class="btn btn-light btn-sm dropdown-toggle" data-bs-toggle="dropdown">
                        <i class="bi bi-three-dots"></i>
                    </button>
                    <ul class="dropdown-menu shadow">
                        <li><a class="dropdown-item" href="{}"><i class="bi bi-eye me-2"></i>View</a></li>
                        <li><a class="dropdown-item" href="{}"><i class="bi bi-pencil me-2"></i>Edit</a></li>
                        <li><a class="dropdown-item" href="{}"><i class="bi bi-journal-text me-2"></i>Ledger</a></li>
                        <li><hr class="dropdown-divider"></li>
                        <li>
                            <a href="{}" class="dropdown-item text-danger delete_supplier" data-supplier-name="{}">
                                <i class="bi bi-trash me-2"></i>Delete
                            </a>
                        </li>
                    </ul>
                </div>
                """,
                reverse("view_supplier", args=[row.id]),  # 1️⃣ View
                reverse("edit_supplier", args=[row.id]),  # 2️⃣ Edit
                reverse("supplier_ledger", args=[row.id]),  # 3️⃣ Ledger
                reverse("delete_supplier", args=[row.id]),  # 4️⃣ Delete
                row.supplier_name,
            )

        return super().render_column(row, column)


@login_required
@permission_required_message("inventory.view_supplier", redirect_to="all_supplier")
def view_supplier(request, id):
    try:
        supplier = get_object_or_404(Supplier, id=id)
        context = {"supplier": supplier}
        return render(request, "inventory/view_supplier.html", context)
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect("all_supplier")


@login_required
@permission_required_message("inventory.edit_supplier", redirect_to="all_supplier")
def edit_supplier(request, id):
    try:
        supplier = get_object_or_404(Supplier, id=id)
        if request.method == "POST":
            form = SupplierForm(request.POST, instance=supplier)
            if form.is_valid():
                try:
                    with transaction.atomic():
                        form.save()
                        messages.success(request, "Supplier updated successfully.")
                        return redirect("all_supplier")
                except Exception as e:
                    messages.error(request, f"Error: {e}")
                    return redirect("add_supplier", id=id)
        else:
            form = SupplierForm(instance=supplier)
        context = {
            "form": form,
            "is_edit": True,
        }
        return render(request, "inventory/add_supplier.html", context)
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect("all_supplier")


@login_required
@permission_required_message("inventory.delete_supplier", redirect_to="all_supplier")
def delete_supplier(request, id):
    try:
        supplier = get_object_or_404(Supplier, id=id)
        supplier.delete()
        messages.success(
            request, f"Supplier {supplier.supplier_name} deleted successfully."
        )
        return redirect("all_supplier")
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect("all_supplier")


@login_required
@permission_required_message("inventory.ledger_supplier", redirect_to="all_supplier")
def supplier_ledger(request, id):
    try:
        supplier = get_object_or_404(Supplier, id=id)
        context = {"supplier": supplier}
        return render(request, "inventory/supplier_ledger.html", context)
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect("all_supplier")


@login_required
@csrf_exempt
def bulk_delete_suppliers(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                ids = request.POST.getlist("ids[]")
                undeletable = []

                for supplier_id in ids:
                    supplier = Supplier.objects.get(id=supplier_id)
                    # check if supplier linked with any product
                    if Product.objects.filter(supplier=supplier).exists():
                        undeletable.append(supplier.supplier_name)
                    else:
                        supplier.delete()

                if undeletable:
                    return JsonResponse(
                        {
                            "status": "partial",
                            "message": f"Some suppliers not deleted (linked with products): {', '.join(undeletable)}",
                        }
                    )

                return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": f"error - {str(e)}"}, status=400)

    return JsonResponse({"status": "error"}, status=400)


# Supplier Management VIEWS CRUD Section End


# Category Management VIEWS CRUD Section Start
@login_required
@permission_required_message("inventory.all_category", redirect_to="dashboard")
def all_category(request):
    category_data = Category.objects.all().order_by("-id")[:5]
    if request.method == "POST":
        form = CategoryForm(request.POST, request=request)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    messages.success(request, "Category added successfully.")
                    return redirect("all_category")
            except Exception as e:
                messages.error(request, f"Error: {e}")
                return redirect("all_category")
    else:
        form = CategoryForm(request=request)
    context = {
        "form": form,
        "category_data": category_data,
    }
    return render(request, "inventory/category/all_category.html", context)


@login_required
@permission_required_message("inventory.edit_category", redirect_to="all_category")
def edit_category(request, id):
    try:
        cat = get_object_or_404(Category, id=id)
        if request.method == "POST":
            form = CategoryForm(request.POST, instance=cat)
            if form.is_valid():
                try:
                    with transaction.atomic():
                        form.save()
                        messages.success(request, "Category updated successfully.")
                        return redirect("all_category")
                except Exception as e:
                    messages.error(request, f"Error: {e}")
                    return redirect("all_category")
        else:
            form = CategoryForm(instance=cat)
        context = {
            "form": form,
            "is_edit": True,
        }
        return render(request, "inventory/category/all_category.html", context)
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect("all_category")


@login_required
@permission_required_message("inventory.delete_category", redirect_to="all_category")
def delete_category(request, id):
    try:
        cat = get_object_or_404(Category, id=id)
        product = Product.objects.filter(category=cat)
        # Get previous URL
        previous_url = request.META.get("HTTP_REFERER", reverse("all_category"))
        if product.exists():
            messages.error(request, "Category is used by Product, can't delete.")
        else:
            cat.delete()
            messages.success(
                request, f"Category {cat.category_name} deleted successfully."
            )
        return redirect(previous_url)
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect("all_category")


@login_required
@permission_required_message("inventory.category_list", redirect_to="all_category")
def category_list(request):
    print(f"HTML page Category hit hua hai.")
    return render(request, "inventory/category/category_list.html")


class CategoryListJson(BaseDatatableView):
    print("✅ JSON page Category hit hua hai.")
    model = Category
    columns = ["Sno", "Category", "Sub-Category", "Status", "Action"]
    order_columns = [
        "id",
        "category_name",
        "sub_categories__category_name",
        "is_active",
    ]
    max_display_length = 10
    search_fields = ["category_name", "sub_categories__category_name", "is_active"]

    # ------------------- Query Optimization -------------------
    def get_initial_queryset(self):
        return Category.objects.filter(parent_category__isnull=True).prefetch_related(
            "sub_categories"
        )

    # ------------------- Search Filter -------------------
    def filter_queryset(self, qs):
        search_value = self.request.GET.get("search[value]", None)
        if search_value:
            q = Q()
            for field in self.search_fields:
                q |= Q(**{f"{field}__icontains": search_value})
            qs = qs.filter(q)
        return qs.distinct()

    # ------------------- Data Preparation -------------------
    def prepare_results(self, qs):
        data = []
        for index, item in enumerate(qs, start=1):
            sub_cats = item.sub_categories.all()
            collapse_id = f"subcat-{item.id}"

            # Sub-category list
            if sub_cats.exists():
                subcat_list = ""
                for sub in sub_cats:
                    sub_name = escape(sub.category_name)
                    badge_class = (
                        "bg-success-subtle text-success border border-success-subtle"
                        if sub.is_active
                        else "bg-danger-subtle text-danger border border-danger-subtle"
                    )
                    icon = (
                        "bi-check-circle-fill" if sub.is_active else "bi-x-circle-fill"
                    )
                    subcat_list += format_html(
                        """
                        <li class="list-group-item py-1">
                            <span class="badge {} px-3 py-2 fs-8">
                                <i class="bi {} me-1"></i>{}
                            </span>
                        </li>
                        """,
                        badge_class,
                        icon,
                        sub_name,
                    )
            else:
                subcat_list = """
                    <li class="list-group-item py-1 text-muted">
                        No Sub-Categories
                    </li>
                """

            # Collapse button + sub-list
            sub_category_html = format_html(
                """
                <button class="btn btn-outline-primary btn-sm w-20 text-start"
                        data-bs-toggle="collapse"
                        data-bs-target="#{id}"
                        aria-expanded="false"
                        aria-controls="{id}">
                    <i class="bi bi-list-ul me-1"></i> Show Sub-Categories
                </button>
                <ul class="collapse list-group list-group-flush mt-2" id="{id}">
                    {list}
                </ul>
                """,
                id=collapse_id,
                list=mark_safe(subcat_list),
            )

            # ✅ Added "id" here (important for checkbox)
            data.append(
                {
                    "id": item.id,  # <-- REQUIRED for checkbox value
                    "Sno": index,
                    "Category": format_html(
                        "{} <span class='badge bg-secondary-subtle text-secondary ms-1'>{}</span>",
                        escape(item.category_name),
                        sub_cats.count(),
                    ),
                    "Sub-Category": sub_category_html,
                    "Status": self.render_column(item, "Status"),
                    "Action": self.render_column(item, "Action"),
                }
            )
        return data

    # ------------------- Column Renderer -------------------
    def render_column(self, row, column):
        if column == "Status":
            if row.is_active:
                return format_html(
                    '<span class="badge bg-success-subtle text-success border border-success-subtle px-2 py-1">'
                    '<i class="bi bi-check-circle-fill me-1"></i>Active</span>'
                )
            return format_html(
                '<span class="badge bg-danger-subtle text-danger border border-danger-subtle px-2 py-1">'
                '<i class="bi bi-x-circle-fill me-1"></i>Inactive</span>'
            )

        if column == "Action":
            return format_html(
                """
                <div class="dropdown">
                    <button class="btn btn-light btn-sm dropdown-toggle" data-bs-toggle="dropdown">
                        <i class="bi bi-three-dots"></i>
                    </button>
                    <ul class="dropdown-menu shadow">
                        <li>
                            <a class="dropdown-item" href="{}">
                                <i class="bi bi-journal-text me-2"></i>Ledger
                            </a>
                        </li>
                        <li>
                            <a class="dropdown-item" href="{}">
                                <i class="bi bi-pencil me-2"></i>Edit
                            </a>
                        </li>
                        <li><hr class="dropdown-divider"></li>
                        <li>
                            <a href="{}" class="dropdown-item text-danger delete_category"
                            data-category-name="{}">
                                <i class="bi bi-trash me-2"></i>Delete
                            </a>
                        </li>
                    </ul>
                </div>
                """,
                reverse_lazy("category_ledger", args=[row.id]),
                reverse_lazy("edit_category", args=[row.id]),
                reverse_lazy("delete_category", args=[row.id]),
                escape(row.category_name),
            )

        return super().render_column(row, column)


def category_ledger(request, id):
    try:
        previous_url = request.META.get("HTTP_REFERER", reverse("all_category"))
        parent = get_object_or_404(Category, id=id)
        sub_category = parent.sub_categories.all()
        print(f"parent {parent.category_name} is active {parent.is_active}")
        print(f"Total Sub-Category {sub_category.count()}")
        for sub in sub_category:
            print(f"Sub-Category {sub.category_name} is active {sub.is_active}")
        products = Product.objects.filter(category__in=sub_category)
        print(f"Products {products.count()}")
        context = {
            "parent": parent,
            "sub_categories": sub_category,
            "products": products,
        }
        return render(request, "inventory/category/category_ledger.html", context)

    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect(previous_url)


@login_required
@csrf_exempt
def bulk_delete_categories(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                ids = request.POST.getlist("ids[]")
                undeletable = []

                for category_id in ids:
                    category = Category.objects.get(id=category_id)

                    # 🔹 Get all subcategories
                    subcategories = category.sub_categories.all()

                    # 🔹 Check agar parent ya uski koi subcategory kisi product se linked hai
                    has_products = (
                        Product.objects.filter(category=category).exists()
                        or Product.objects.filter(category__in=subcategories).exists()
                    )

                    if has_products:
                        undeletable.append(category.category_name)
                    else:
                        category.delete()

                # 🔹 Partial delete response (agar kuch delete nahi hue)
                if undeletable:
                    return JsonResponse(
                        {
                            "status": "partial",
                            "message": f"Some categories not deleted (linked with products): {', '.join(undeletable)}",
                        }
                    )

                # 🔹 All deleted successfully
                return JsonResponse({"status": "success"})

        except Exception as e:
            return JsonResponse({"status": f"error - {str(e)}"}, status=400)

    return JsonResponse({"status": "error"}, status=400)


# Category Management VIEWS CRUD Section End


# Warehouse Management VIEWS CRUD Section Start
@login_required
@permission_required_message("inventory.warehouse", redirect_to="dashboard")
def warehouse(request):
    if request.method == "POST":
        form = WarehouseForm(request.POST, request=request)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Warehouse added successfully.")
                return redirect("warehouse_list")
            except:
                return redirect("warehouse")
    else:
        form = WarehouseForm()
    context = {"form": form}
    return render(request, "inventory/warehouse/warehouse.html", context)


@login_required
@permission_required_message("inventory.edit_warehouse", redirect_to="warehouse")
def edit_warehouse(request, id):
    try:
        warehouse = get_object_or_404(Warehouse, id=id)
        if request.method == "POST":
            form = WarehouseForm(request.POST, instance=warehouse, request=request)
            if form.is_valid():
                try:
                    with transaction.atomic():
                        form.save()
                        messages.success(request, "Warehouse updated successfully.")
                        return redirect("warehouse_list")
                except Exception as e:
                    messages.error(request, f"Error: {e}")
                    return redirect("warehouse")
        else:
            form = WarehouseForm(instance=warehouse)
        context = {
            "form": form,
            "is_edit": True,
        }
        return render(request, "inventory/warehouse/warehouse.html", context)
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect("warehouse")


@login_required
@permission_required_message("inventory.delete_warehouse", redirect_to="warehouse")
def delete_warehouse(request, id):
    try:
        warehouse = get_object_or_404(Warehouse, id=id)
        warehouse.delete()
        messages.success(
            request, f"Warehouse {warehouse.warehouse_name} deleted successfully."
        )
        return redirect("warehouse_list")
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect("warehouse_list")


@login_required
@permission_required_message("inventory.warehouse_list", redirect_to="dashboard")
def warehouse_list(request):
    data = Warehouse.objects.all().order_by("-id")

    context = {
        "warehouse": data,
    }
    return render(request, "inventory/warehouse/warehouse_list.html", context)


@login_required
@permission_required_message("inventory.warehouse_view", redirect_to="warehouse_list")
def warehouse_view(request, id):
    try:
        warehouse = get_object_or_404(Warehouse, id=id)
        context = {"warehouse": warehouse}
        return render(request, "inventory/warehouse/warehouse_view.html", context)
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect("warehouse_list")


# Warehouse Management VIEWS CRUD Section End


# Product Management VIEWS CRUD Section Start
@login_required
@permission_required_message("inventory.view_product", redirect_to="dashboard")
def product_list(request):
    product = Product.objects.first()
    print(f"Product {product.is_active}")
    print(f"Product created by {product.created_by}")
    return render(request, "inventory/product/product_list.html")


class ProductListJson(BaseDatatableView):
    logger.info("AJAX request received")
    model = Product
    columns = [
        "Sno",
        "Image",
        "Name",
        "Warehouse",
        "Selling Price",
        "Measure",
        "Stock",
        "Status",
    ]
    order_columns = [
        "id",  # Sno
        "image",  # Image
        "product_name",  # Name
        "warehouse__name",  # Warehouse
        "selling_price",  # Selling Price
        "measure",  # Measure
        "stock",  # Stock
        "is_active",  # Status
    ]
    max_display_length = 10
    search_fields = [
        "product_name",
        "selling_price",
        "measure",
        "stock",
        "is_active",
    ]

    def filter_queryset(self, qs):
        search_value = self.request.GET.get("search[value]", None)
        if search_value:
            q = Q()
            for field in self.search_fields:
                q |= Q(**{f"{field}__icontains": search_value})
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        data = []
        for index, item in enumerate(qs, start=1):
            data.append(
                {
                    "Sno": index,
                    "Image": self.render_column(item, "Image"),
                    "Name": item.product_name,
                    "Warehouse": (
                        item.warehouse.warehouse_name if item.warehouse else ""
                    ),
                    "Selling Price": item.selling_price,
                    "Measure": item.measure,
                    "Stock": item.stock,
                    "Status": self.render_column(item, "Status"),
                    "Action": self.render_column(item, "Action"),
                }
            )
        return data

    def render_column(self, row, column):
        if column == "Status":
            if row.is_active:
                return format_html(
                    '<span class="badge bg-success-subtle text-success border border-success-subtle px-2 py-1"><i class="bi bi-check-circle-fill me-1"></i>Active</span>'
                )
            else:
                return format_html(
                    '<span class="badge bg-danger-subtle text-danger border border-danger-subtle px-2 py-1"><i class="bi bi-x-circle-fill me-1"></i>Inactive</span>'
                )

        if column == "Image":
            if row.image:
                return format_html(
                    '<img src="{}" class="img-fluid rounded" alt="Product Image">',
                    row.image.url,
                )
            return ""
        if column == "Action":
            return format_html(
                """
                <div class="dropdown">
                    <button class="btn btn-light btn-sm dropdown-toggle" data-bs-toggle="dropdown">
                        <i class="bi bi-three-dots"></i>
                    </button>
                    <ul class="dropdown-menu shadow">
                        <li>
                            <a class="dropdown-item" href="{}">
                                <i class="bi bi-pencil me-2"></i>Edit
                            </a>
                        </li>
                        <li>
                            <a class="dropdown-item" href="{}">
                                <i class="bi bi-eye me-2"></i>View
                            </a>
                        </li>
                        <li><hr class="dropdown-divider"></li>
                        <li>
                            <a href="{}" class="dropdown-item text-danger delete_product"
                            data-product-name="{}">
                                <i class="bi bi-trash me-2"></i>Delete
                            </a>
                        </li>
                    </ul>
                </div>
                """,
                reverse_lazy("edit_product", args=[row.id]),  #  Edit
                reverse_lazy("view_product", args=[row.id]),  #  View
                reverse_lazy("delete_product", args=[row.id]),  #  Delete URL
                row.product_name,  #  For SweetAlert
            )
        return super().render_column(row, column)


@login_required
@permission_required_message("inventory.add_product", redirect_to="product_list")
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    messages.success(request, "Product added successfully.")
                    return redirect("product_list")
            except Exception as e:
                messages.error(request, f"Error: {e}")
                return redirect("add_product")
    else:
        form = ProductForm(request=request)
    context = {"form": form}
    return render(request, "inventory/product/add_product.html", context)


@login_required
@permission_required_message("inventory.edit_product", redirect_to="product_list")
def edit_product(request, id):
    try:
        product = get_object_or_404(Product, id=id)
        if request.method == "POST":
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                try:
                    print(f"Product {form.cleaned_data.get('is_active')} updated")

                    with transaction.atomic():
                        form.save()
                        messages.success(request, "Product updated successfully.")
                        return redirect("product_list")
                except Exception as e:
                    messages.error(request, f"Error: {e}")
                    return redirect("add_product", id=id)
        else:
            form = ProductForm(instance=product)
        context = {
            "form": form,
            "is_edit": True,
        }
        return render(request, "inventory/product/add_product.html", context)
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect("product_list")


@login_required
@permission_required_message("inventory.delete_product", redirect_to="product_list")
def delete_product(request, id):
    try:
        product = get_object_or_404(Product, id=id)
        product.image.delete(save=False)
        product.delete()
        messages.success(
            request, f"Product {product.product_name} deleted successfully."
        )
        return redirect("product_list")
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect("product_list")


@login_required
@permission_required_message("inventory.view_product", redirect_to="product_list")
def view_product(request, id):
    try:
        product = get_object_or_404(Product, id=id)
        context = {"product": product}
        return render(request, "inventory/product/view_product.html", context)
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect("product_list")


# Product Management VIEWS CRUD Section End
