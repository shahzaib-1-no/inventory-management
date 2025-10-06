from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.contrib import messages
from dashboard.forms import LoginForm, GroupForm


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


@login_required
def user_role_and_permission(request):
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
    return render(request, "dashboard/roles_and_permission.html", context)
