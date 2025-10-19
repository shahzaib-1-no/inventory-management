def global_permissions(request):
    """
    Ye context processor har template mai user permissions provide karega
    across all apps (like accounts, inventory, sales, etc.)
    """
    if not request.user.is_authenticated:
        return {}

    return {
        # Auth app
        "can_view_user": request.user.has_perm("auth.view_user"),
        "can_add_user": request.user.has_perm("auth.add_user"),
        "can_view_userrole": request.user.has_perm("atuh.view_userrole"),
        "can_add_userrole": request.user.has_perm("auth.add_userrole"),
        # Dashboard app
        "can_view_product": request.user.has_perm("inventory.view_product"),
        "can_add_product": request.user.has_perm("inventory.add_product"),
        "can_view_category": request.user.has_perm("inventory.view_category"),
        "can_add_category": request.user.has_perm("inventory.add_category"),
        "can_view_warehouse": request.user.has_perm("inventory.view_warehouse"),
        "can_add_warehouse": request.user.has_perm("inventory.add_warehouse"),
        "can_edit_warehouse": request.user.has_perm("inventory.edit_warehouse"),
        "can_view_supplier": request.user.has_perm("inventory.view_supplier"),
        "can_add_supplier": request.user.has_perm("inventory.add_supplier"),
        "Can view supplier ledger": request.user.has_perm("inventory.ledger_supplier"),
    }
