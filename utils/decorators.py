from functools import wraps
from django.core.exceptions import PermissionDenied


def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied("You must be logged in.")

            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            user_groups = request.user.groups.values_list('name', flat=True)
            if not any(role in user_groups for role in allowed_roles):
                raise PermissionDenied("Access denied.")

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
