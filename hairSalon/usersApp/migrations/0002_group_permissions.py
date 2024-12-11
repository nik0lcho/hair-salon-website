from django.db import migrations


def create_group_with_permissions(apps, schema_editor):
    # Get the models dynamically to ensure migrations work across environments
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    # Create a group
    group_name = "Staff"
    group, created = Group.objects.get_or_create(name=group_name)

    # Permissions from different apps
    permissions = [
        ("common", "add_service"),
        ("common", "change_service"),
        ("common", "delete_service"),
        ("common", "view_service"),

        ("hairDressersApp", "view_appointment"),
        ("hairDressersApp", "view_schedule"),
        ("hairDressersApp", "view_timeslot"),

        ("usersApp", "view_appuser"),
        ("usersApp", "view_review"),
    ]

    for app_label, codename in permissions:
        try:
            perm = Permission.objects.get(codename=codename, content_type__app_label=app_label)
            group.permissions.add(perm)
        except Permission.DoesNotExist:
            print(f"Permission '{codename}' in app '{app_label}' does not exist. Skipping.")


class Migration(migrations.Migration):

    dependencies = [
        ("admin", "0003_logentry_add_action_flag_choices"),
        ("auth", "0012_alter_user_first_name_max_length"),  # Latest migration for auth app
        ("common", "0001_initial"),  # Latest migration for common app
        ("contenttypes", "0002_remove_content_type_name"),  # ContentType app's latest migration
        ("hairDressersApp", "0002_initial"),  # Latest migration for hairDressersApp
        ("sessions", "0001_initial"),  # Sessions app's latest migration
        ("usersApp", "0001_initial"),  # Latest migration for usersApp
    ]

    operations = [
        migrations.RunPython(create_group_with_permissions),
    ]
