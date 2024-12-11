from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group
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

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    role = models.CharField(
        max_length=20,
        choices=ROLES,
        default=ROLE_CLIENT,
        help_text="Designates the role of the user.",
    )

    objects = AppUserManager()

    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.PositiveIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        default=5
    )

    content = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
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
    if created:

        group_name = instance.role.capitalize()

        group, created_group = Group.objects.get_or_create(name=group_name)

        instance.groups.add(group)

        if created_group:
            print(f"Group '{group_name}' was created automatically.")

        print(f"User {instance.email} assigned to group '{group_name}'.")
