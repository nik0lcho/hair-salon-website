from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group, UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from hairSalon import settings
from hairSalon.hairDressersApp.models import Schedule, TimeSlot, AvailableDate
from hairSalon.common.models import Service
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from hairSalon.usersApp.managers import AppUserManager


class AppUser(AbstractBaseUser, PermissionsMixin):

    ROLE_ADMIN = 'admin'
    ROLE_STAFF = 'staff'
    ROLE_CLIENT = 'client'
    ROLE_HAIRDRESSER = 'hairdresser'

    ROLES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_STAFF, 'Staff'),
        (ROLE_CLIENT, 'Client'),
        (ROLE_HAIRDRESSER, 'Hairdresser'),
    ]

    # Basic fields
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    role = models.CharField(
        max_length=20,
        choices=ROLES,
        default=ROLE_CLIENT,
        help_text="Designates the role of the user.",
    )

    objects = AppUserManager()

    # Optional fields for user management
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    # Required fields for AbstractBaseUser
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # No other required fields, only email and password are needed.

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def is_client(self):
        if self.role == AppUser.ROLE_CLIENT:
            return True
        return False

    @property
    def is_hairdresser(self):
        if self.role == AppUser.ROLE_HAIRDRESSER:
            return True
        return False


class Review(models.Model):
    """
    Model representing a review for a service.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # this links to the custom user model
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.PositiveIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        default=5
    )

    # Review text content
    content = models.TextField(
        blank=True,  # Optional field for the review text
        null=True
    )

    # Date the review was created
    created_at = models.DateTimeField(auto_now_add=True)

    # Optional: whether the review has been approved for display
    approved = models.BooleanField(default=True)

    def __str__(self):
        profile = getattr(self.user, 'profile', None)

        return f"Review by {profile.first_name} {profile.last_name if profile.last_name else ''} on {self.created_at}"

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ['-created_at']


@receiver(post_save, sender=AppUser)
def assign_user_to_group(sender, instance, created, **kwargs):
    """
    Assign users to existing groups based on their role after they are created.
    If the group doesn't exist, create it automatically.
    """
    if created:

        # Role to Group mapping
        group_name = instance.role.capitalize()  # Ensure "admin", "staff", "client", "hairdresser" maps correctly

        # Check if the group exists, and create it if necessary
        group, created_group = Group.objects.get_or_create(name=group_name)

        # Add the user to the corresponding group
        instance.groups.add(group)

        if created_group:
            print(f"Group '{group_name}' was created automatically.")

        print(f"User {instance.email} assigned to group '{group_name}'.")
