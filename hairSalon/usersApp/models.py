from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from hairSalon import settings
from hairSalon.usersApp.managers import AppUserManager

# Role choices
ROLE_CHOICES = [
    ('admin', 'Admin'),
    ('staff', 'Staff'),
    ('client', 'Client'),
    ('hairdresser', 'Hairdresser'),
]


class AppUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for authentication with roles and permissions.
    """
    email = models.EmailField(unique=True)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text="Designates whether this user should be treated as active. "
                  "Unselect this instead of deleting accounts.",
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='client',
        help_text="Designates the role of the user.",
    )

    objects = AppUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Send an email to the user.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    class Meta:
        verbose_name = "App User"
        verbose_name_plural = "App Users"


class Profile(models.Model):
    """
    Profile model for additional user information.
    """
    user = models.OneToOneField(to=AppUser, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


@receiver(post_save, sender=AppUser)
def assign_user_to_group(sender, instance, created, **kwargs):
    """
    Assign users to existing groups based on their role after they are created.
    If the group doesn't exist, create it automatically.
    """
    if created:
        # Automatically create a profile for the user
        Profile.objects.create(user=instance)

        # Role to Group mapping
        group_name = instance.role.capitalize()  # Ensure "admin", "staff", "client", "hairdresser" maps correctly

        # Check if the group exists, and create it if necessary
        group, created_group = Group.objects.get_or_create(name=group_name)

        # Add the user to the corresponding group
        instance.groups.add(group)

        if created_group:
            print(f"Group '{group_name}' was created automatically.")

        print(f"User {instance.email} assigned to group '{group_name}'.")


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

        return f"Review by {profile.first_name} {profile.last_name}"

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ['-created_at']
