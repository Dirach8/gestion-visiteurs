from django.shortcuts import redirect
from functools import wraps


def role_required(*roles):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect('connexion')

            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            if request.user.groups.filter(
                name__in=roles
            ).exists():
                return view_func(request, *args, **kwargs)

            return redirect('dashboard_agent')

        return wrapper

    return decorator