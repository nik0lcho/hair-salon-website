from django import forms
from .models import AppUser


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

        if commit:
            user.save()
        return user
