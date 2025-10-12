from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def permission_required_message(perm, redirect_to):
    """
    Custom decorator that checks user permission.
    If user lacks permission, shows SweetAlert-compatible error message
    and redirects to given URL name.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.has_perm(perm):
                messages.error(
                    request, "You do not have permission to perform this action."
                )
                return redirect(redirect_to)
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
