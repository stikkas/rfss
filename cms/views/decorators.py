from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.contrib.auth.decorators import login_required as _login_required

from cms.conf import settings
from cms.regions import get_region
from cms.url_builders import build_url


def login_required(function, redirect_field_name='next',
                   login_url=build_url(settings.LOGIN_URL)):
    return _login_required(function, redirect_field_name, login_url)


def cms_protector(func):
    def wrapper(request, *args, **kwargs):
        try:
            if request.user.has_perm('regions.manage_content', get_region()):
                return func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        except ObjectDoesNotExist:
            return login_required(func)(request, *args, **kwargs)
    return wrapper
