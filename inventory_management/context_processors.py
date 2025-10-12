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
    }
