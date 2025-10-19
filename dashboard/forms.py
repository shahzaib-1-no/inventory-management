from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    remember = forms.BooleanField(label="Remember me", required=False)

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data.get("username")
        cleaned_data.get("password")
        cleaned_data.get("remember")

        return cleaned_data


class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.filter(
            content_type__app_label__in=["auth", "group", "inventory"],
            content_type__model__in=[
                "user",
                "permission",
                "supplier",
                "category",
                "warehouse",
                "product",
            ],
        ),  # .exclude(codename="change_user")
        required=False,
        help_text="Select permissions for this role",
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-control form-select",  # Bootstrap style for multi-select
                "size": "8",  # visible options height (optional)
            }
        ),
    )

    class Meta:
        model = Group
        fields = ["name", "permissions"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",  # Bootstrap text input
                    "placeholder": "Enter Role Name",  # helpful placeholder
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["permissions"].label_from_instance = (
            lambda obj: f"{obj.content_type.model} | {obj.name}"
        )

        for field_name, field in self.fields.items():
            if not field.widget.attrs.get("class"):
                field.widget.attrs["class"] = "form-control"


class RegisterForm(forms.ModelForm):
    """
    Form for registering new users (staff).
    Includes password confirmation, Bootstrap styling, and secure password handling.
    """

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter password",
            }
        ),
        label="Password",
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm password",
            }
        ),
        label="Confirm Password",
    )
    role = forms.ModelChoiceField(
        queryset=Group.objects.all().order_by("-id"),
        widget=forms.Select(
            attrs={
                "class": "form-control form-select",
            }
        ),
        label="Role",
        empty_label="--- Select Role ---",
        required=False,
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "role", "email", "password"]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Username",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "First name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Last name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email address",
                }
            ),
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already registered.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
            roles = self.cleaned_data.get("role")
            if roles:
                user.groups.set([roles])
        return user


class EditUserForm(forms.ModelForm):
    """
    Form for editing existing users (staff/admin).
    Password optional, role can be updated.
    """

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter new password"}
        ),
        label="Password",
        help_text="Leave blank to keep current password",
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm new password"}
        ),
        label="Confirm Password",
    )
    role = forms.ModelChoiceField(
        queryset=Group.objects.all().order_by("-id"),
        widget=forms.Select(attrs={"class": "form-control form-select"}),
        empty_label="-- Select Role --",
        label="Role",
        required=False,
        help_text="Leave blank to keep current Role",
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "role", "password"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "First name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Last name"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email address"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Only check passwords if entered
        if password or confirm_password:
            if password != confirm_password:
                self.add_error("confirm_password", "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")

        if password:
            user.password = make_password(password)

        if commit:
            user.save()
            role = self.cleaned_data.get("role")
            if role:
                user.groups.set([role])
            else:
                pass
        return user


class EditGroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.filter(
            content_type__app_label__in=["auth", "group", "inventory"],
            content_type__model__in=[
                "user",
                "permission",
                "product",
                "category",
                "warehouse",
                "supplier",
            ],
        ),
        required=False,
        help_text="Select permissions for this role",
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-control form-select",  # Bootstrap style for multi-select
                "size": "8",  # visible options height (optional)
            }
        ),
    )

    class Meta:
        model = Group
        fields = ["name", "permissions"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",  # Bootstrap text input
                    "placeholder": "Enter Role Name",  # helpful placeholder
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["permissions"].label_from_instance = (
            lambda obj: f"{obj.content_type.model} | {obj.name}"
        )

        for field_name, field in self.fields.items():
            if not field.widget.attrs.get("class"):
                field.widget.attrs["class"] = "form-control"

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")

        # verification for instance (update case) is must be excluded.
        existing_group = Group.objects.filter(name=name).exclude(pk=self.instance.pk)
        if existing_group.exists():
            raise forms.ValidationError("This role name is already registered.")

        return cleaned_data

    def save(self, commit=True):
        group = super().save(commit=False)
        group.name = self.cleaned_data["name"]
        if commit:
            group.save()
            group.permissions.set(self.cleaned_data["permissions"])
        return group
