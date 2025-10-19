from django.urls import path

from . import views

urlpatterns = [
    # Supplier Management URLs CRUD Section Start
    path("supplier/all-supplier/", views.all_supplier, name="all_supplier"),
    path("supplier/add-supplier/", views.add_supplier, name="add_supplier"),
    path(
        "ajax_supplier_list_data/",
        views.SupplierListJson.as_view(),
        name="ajax_supplier_list_data",
    ),
    path("supplier/view-supplier/<int:id>/", views.view_supplier, name="view_supplier"),
    path("supplier/edit-supplier/<int:id>/", views.edit_supplier, name="edit_supplier"),
    path(
        "supplier/delete-supplier/<int:id>/",
        views.delete_supplier,
        name="delete_supplier",
    ),
    path(
        "supplier/supplier-ledger/<int:id>/",
        views.supplier_ledger,
        name="supplier_ledger",
    ),
    path(
        "supplier/bulk_delete",
        views.bulk_delete_suppliers,
        name="bulk_delete_suppliers",
    ),
    # Supplier Management URLs CRUD Section End
    # Category Management URLs CRUD Section Start
    path("product/all-category/", views.all_category, name="all_category"),
    path("product/edit-category/<int:id>/", views.edit_category, name="edit_category"),
    path(
        "product/delete-category/<int:id>/",
        views.delete_category,
        name="delete_category",
    ),
    path("product/category-list/", views.category_list, name="category_list"),
    path(
        "ajax_category_list_data/",
        views.CategoryListJson.as_view(),
        name="ajax_category_list_data",
    ),
    path(
        "product/category-ledger/<int:id>/",
        views.category_ledger,
        name="category_ledger",
    ),
    path(
        "product/bulk_delete/",
        views.bulk_delete_categories,
        name="bulk_delete_categories",
    ),
    # Category Management URLs CRUD Section End
    # Warehouse Management URLs CRUD Section Start
    path("warehouse/warehouse/", views.warehouse, name="warehouse"),
    path(
        "warehouse/edit-warehouse/<int:id>/",
        views.edit_warehouse,
        name="edit_warehouse",
    ),
    path(
        "warehouse/delete-warehouse/<int:id>/",
        views.delete_warehouse,
        name="delete_warehouse",
    ),
    path("warehouse/warehouse-list/", views.warehouse_list, name="warehouse_list"),
    path(
        "warehouse/warehouse-view/<int:id>/",
        views.warehouse_view,
        name="warehouse_view",
    ),
    # Warehouse Management URLs CRUD Section End
    # Product Management URLs CRUD Section Start
    path("product/product-list/", views.product_list, name="product_list"),
    path("product/add-product/", views.add_product, name="add_product"),
    path("product/edit-product/<int:id>/", views.edit_product, name="edit_product"),
    path(
        "product/delete-product/<int:id>/", views.delete_product, name="delete_product"
    ),
    path(
        "ajax_product_list_data/",
        views.ProductListJson.as_view(),
        name="ajax_product_list_data",
    ),
    path("product/product-view/<int:id>/", views.view_product, name="view_product"),
    # Product Management URLs CRUD Section End
]
