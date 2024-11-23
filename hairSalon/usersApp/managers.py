from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


class AppUserManager(BaseUserManager):
    """
    Custom manager for the AppUser model without relying on usernames.
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        This method validates the password.
        """
        if not email:
            raise ValueError("The Email field must be set")

        if not password:
            raise ValueError("Password is required")  # Ensure password is provided

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_client(self, email, password=None, **extra_fields):
        """
        Create a regular user with the given email and password.
        This method doesn't require additional validation as validation is handled in _create_user.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("role", "client")  # Default to client role
        return self._create_user(email, password, **extra_fields)

    def create_staff(self, email, password=None, **extra_fields):
        """
        Create a staff user.
        Calls _create_user which handles password validation.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("role", "staff")
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create a superuser.
        Calls _create_user which handles password validation.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")
        return self._create_user(email, password, **extra_fields)

    def create_hairdresser(self, email, password=None, **extra_fields):
        """
        Create a hairdresser user.
        Calls _create_user which handles password validation.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("role", "hairdresser")
        return self._create_user(email, password, **extra_fields)
