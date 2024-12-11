from django.contrib.auth.hashers import make_password

from .models import AppUser
from django.contrib.auth.models import Group
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


class AppUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = AppUser
        fields = ('email', 'role', 'first_name', 'last_name', 'is_active')  # Do not include is_staff or is_superuser

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password1"]
        user.set_password(password)

        # Role-based logic for setting permissions
        role = self.cleaned_data["role"]
        if role == AppUser.ROLE_ADMIN:
            user.is_staff = True
            user.is_superuser = True
        elif role == AppUser.ROLE_STAFF:
            user.is_staff = True
            user.is_superuser = False
        elif role in [AppUser.ROLE_CLIENT, AppUser.ROLE_HAIRDRESSER]:
            user.is_staff = False
            user.is_superuser = False

        if commit:
            user.save()
        return user


class AppUserChangeForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ('email', 'role', 'first_name', 'last_name', 'is_active')  # Exclude is_staff and is_superuser

    def save(self, commit=True):
        user = super().save(commit=False)

        # Role-based logic for setting permissions when changing the role
        role = self.cleaned_data["role"]
        if role == AppUser.ROLE_ADMIN:
            user.is_staff = True
            user.is_superuser = True
        elif role == AppUser.ROLE_STAFF:
            user.is_staff = True
            user.is_superuser = False
        elif role in [AppUser.ROLE_CLIENT, AppUser.ROLE_HAIRDRESSER]:
            user.is_staff = False
            user.is_superuser = False

        group_name = role.capitalize()
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.set([group])

        if commit:
            user.save()

        return user


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(max_length=255, required=True, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        model = AppUser
        fields = ('email', 'password', 'first_name', 'last_name')

    def save(self, commit=True):
        # Create a new user instance but don't save to the database yet
        user = super().save(commit=False)

        # Hash the password before saving
        user.password = make_password(self.cleaned_data['password'])
        user.role = AppUser.ROLE_CLIENT

        # Save the user instance if commit is True
        if commit:
            user.save()

        return user


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255, required=True, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Password")

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        # Authenticate the user using email and password
        user = authenticate(email=email, password=password)

        if user is None:
            raise forms.ValidationError("Invalid email or password.")

        # Attach the authenticated user to the form data for access in the view
        cleaned_data['user'] = user
        return cleaned_data
