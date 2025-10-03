from django import forms
from django.contrib.auth.models import Group, Permission

class LoginForm(forms.Form):
    username= forms.CharField(widget=forms.TextInput, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    remember = forms.BooleanField(label='Remember me', required=False)
    
    def clean(self):
        cleaned_data = super().clean()
        username= cleaned_data.get('username')
        password = cleaned_data.get('password')
        remember = cleaned_data.get('remember')
        
        return cleaned_data

class GroupForm(forms.ModelForm):
    # Fetch all permissions dynamically from auth_permission
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.filter(content_type__app_label='dashboard', content_type__model='product'),  # fetch permissions for product app
        required=False,
        help_text="Select permissions for this role"
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']