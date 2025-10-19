from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as user_login
from django.contrib.auth import logout as user_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.db import transaction
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.html import format_html
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from dashboard.forms import (
    EditGroupForm,
    EditUserForm,
    GroupForm,
    LoginForm,
    RegisterForm,
)
from dashboard.models import Notification
from inventory_management.decorators import permission_required_message


@login_required
def dashboard(request):
    return render(request, "dashboard/dashboard.html")


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            remember = form.cleaned_data.get("remember")
            user = authenticate(username=username, password=password)
            if user is not None:
                user_login(request, user)
                # remember me logic: session expiry set karein
                if not remember:
                    request.session.set_expiry(0)  # browser close hone pe logout
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid username or password")
                # form.add_error(None, "Invalid username or password")
        else:
            print("Form is not valid:", form.errors)
    else:
        form = LoginForm()
    context = {"form": form}
    return render(request, "dashboard/auth/login.html", context)


def logout(request):
    user_logout(request)
    messages.success(request, "You have been logged out")
    return redirect("login")


@login_required
def add_group(request):
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.save()
            messages.success(request, "Group added successfully")
            return redirect("dashboard")
        else:
            messages.error(request, "Group not added")
    else:
        form = GroupForm()
    context = {"form": form}
    return render(request, "dashboard/add_group.html", context)


### Notification Section ###
@login_required
def notification_redirect_view(request, pk):
    print(f"notification: {pk}")
    try:
        notification = get_object_or_404(Notification, pk=pk)
        notification.is_read = True
        notification.save()
        return redirect(notification.related_object.get_absolute_url())
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect("admin_dashboard")


### Notification Section End ###


# Roles & Permissions Views Section Start
@login_required
@permission_required_message("auth.view_user", redirect_to="dashboard")
def user_role_and_permission(request):
    groups = Group.objects.all().prefetch_related("permissions")

    roles = []
    for group in groups:
        roles.append(
            {
                "name": group.name,
                "permissions": [perm.codename for perm in group.permissions.all()],
            }
        )
    roles_list = Group.objects.annotate(user_count=Count("user"))
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.save()
            form.save_m2m()
            messages.success(request, "Group added successfully")
            return redirect("dashboard")
        else:
            messages.error(request, "Group not added")
    else:
        form = GroupForm()
    context = {
        "form": form,
        "roles": roles,
        "roles_list": roles_list,
    }
    return render(
        request,
        "dashboard/permission_management/roles_and_permission.html",
        context,
    )


@login_required
@permission_required_message("auth.delete_user", redirect_to="user_role_and_permission")
def delete_role(request, id):
    role = get_object_or_404(Group, id=id)
    if role.user_set.exists():
        messages.error(request, "Role cannot be deleted as it is assigned to users")
        return redirect("user_role_and_permission")
    else:
        role.delete()
        messages.success(request, f"Role '{role.name}' deleted successfully.")
    return redirect("user_role_and_permission")


@login_required
@permission_required_message("auth.change_user", redirect_to="user_role_and_permission")
def edit_role(request, id):
    role = get_object_or_404(Group, id=id)
    if request.method == "POST":
        form = EditGroupForm(request.POST, instance=role)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    messages.success(
                        request, f"Role '{role.name}' updated successfully."
                    )
                    return redirect("user_role_and_permission")
            except Exception as e:
                messages.error(request, f"Error: {e}")
    else:
        form = EditGroupForm(instance=role)
    context = {
        "form": form,
    }
    return render(request, "dashboard/permission_management/edit_group.html", context)


@login_required
@csrf_exempt
def bulk_group_delete(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                ids = request.POST.getlist("ids[]")
                # filter groups jinke paas koi user assigned na ho
                deletable_groups = (
                    Group.objects.filter(id__in=ids)
                    .annotate(user_count=Count("user"))
                    .filter(user_count=0)
                )
                deletable_ids = list(deletable_groups.values_list("id", flat=True))
                deletable_groups.delete()
                return JsonResponse({"status": "success", "deleted_ids": deletable_ids})
        except Exception as e:
            return JsonResponse({"status": f"error - {str(e)}"}, status=400)
    return JsonResponse({"status": "error"}, status=400)


# Roles & Permissions Views Section End


# VIEWS USER MANAGEMENT SECTION START
@login_required
@permission_required_message("auth.add_user", redirect_to="all_user")
def add_user(request):
    """
    View to add a new user (staff or admin).
    Only accessible by users with 'add_user' permission.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                messages.success(request, "User added successfully.")
                return redirect(reverse_lazy("all_user"))
            except Exception as e:
                messages.error(request, f"Error: {e}")
    else:
        form = RegisterForm()

    context = {"form": form}
    return render(request, "dashboard/user_management/add_user.html", context)


@login_required
@permission_required_message("auth.view_user", redirect_to="dashboard")
def all_user(request):
    users = (
        User.objects.filter(is_superuser=False)
        .prefetch_related("groups")
        .order_by("-id")
    )
    context = {"users": users}
    return render(request, "dashboard/user_management/all_user.html")


@login_required
@permission_required_message("auth.delete_user", redirect_to="all_user")
def delete_user(request, id):
    try:
        with transaction.atomic():
            user = get_object_or_404(User, id=id)
            user.delete()
            messages.success(request, f"User {user.username} deleted successfully.")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect("all_user")


@login_required
@permission_required_message("auth.change_user", redirect_to="all_user")
def edit_user(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == "POST":
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    messages.success(
                        request, f"User {user.username} updated successfully."
                    )
                    return redirect("all_user")
            except Exception as e:
                messages.error(request, f"Error: {e}")
    else:
        form = EditUserForm(instance=user)
    context = {
        "form": form,
        "is_edit": True,
        "user_obj": user,
    }
    return render(request, "dashboard/user_management/edit_user.html", context)


@login_required
@permission_required_message("auth.view_user", redirect_to="all_user")
def user_detail(request, id):
    user = get_object_or_404(User, id=id)
    context = {"user": user}
    return render(request, "dashboard/user_management/user_detail.html", context)


class UserListJson(BaseDatatableView):
    model = User
    columns = ["id", "username", "first_name", "email", "role"]
    order_columns = ["id", "username", "first_name", "email", "role"]
    max_display_length = 10
    search_fields = ["username", "first_name", "email", "groups__name"]

    def filter_queryset(self, qs):
        # exclude superusers
        qs = qs.filter(is_superuser=False)

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
            checkbox = format_html(
                '<input type="checkbox" class="user-checkbox" value="{}">', item.id
            )
            data.append(
                {
                    "id": item.id,
                    "Checkbox": checkbox,
                    "SnO": index,
                    "Username": item.username,
                    "First Name": item.first_name,
                    "Email": item.email,
                    "Role": item.groups.first().name if item.groups.exists() else "",
                    "Actions": self.render_column(item, "action"),
                }
            )
        return data

    def render_column(self, row, column):
        if column == "action":
            return format_html(
                """
                <a href="{}" class="btn btn-sm btn-outline-primary me-1">
                    <i class="bi bi-pencil"></i>
                </a>
                <a href="{}" class="btn btn-sm btn-outline-danger delete_user" data-username="{}">
                    <i class="bi bi-trash"></i>
                </a>
                """,
                reverse_lazy("edit_user", args=[row.id]),
                reverse_lazy("delete_user", args=[row.id]),
                row.username,
            )
        return super().render_column(row, column)


@login_required
@csrf_exempt
def bulk_delete_users(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                ids = request.POST.getlist("ids[]")  # multiple IDs
                # delete all users except superusers
                User.objects.filter(id__in=ids, is_superuser=False).delete()
                return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error - " + str(e)}, status=400)
    return JsonResponse({"status": "error"}, status=400)


# VIEWS USER MANAGEMENT SECTION END
