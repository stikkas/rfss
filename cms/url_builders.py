from django.core import urlresolvers
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.utils.importlib import import_module

from cms.conf import settings
from cms.regions import get_region


def build_url(url):
    for builder in get_url_builders():
        url = builder.processing(url)
    return url

def permalink(func):
    def wrapper(self):
        link, args = func(self)
        return build_url(urlresolvers.reverse(link, args=args))
    return wrapper

def redirect(to, *args, **kwargs):
    """Code based on django.shortcuts.redirect"""
    if kwargs.pop('permanent', False):
        redirect_class = HttpResponsePermanentRedirect
    else:
        redirect_class = HttpResponseRedirect

    # If it's a model, use get_absolute_url()
    if hasattr(to, 'get_absolute_url'):
        url = build_url(to.get_absolute_url())
        return redirect_class(url)

    # Next try a reverse URL resolution.
    try:
        url = build_url(urlresolvers.reverse(to, args=args, kwargs=kwargs))
        return redirect_class(url)
    except urlresolvers.NoReverseMatch:
        # If this is a callable, re-raise.
        if callable(to):
            raise
            # If this doesn't "feel" like a URL, re-raise.
        if '/' not in to and '.' not in to:
            raise

    # Finally, fall back and assume it's a URL
    return redirect_class(build_url(to))

def get_url_builders():
    """Get and return url builders instances from settings"""
    builders = []
    for builder in settings.URL_BUILDERS:
        module_path, cls_name = builder.rsplit('.', 1)
        module = import_module(module_path)
        builders.append(getattr(module, cls_name)())
    return builders


class RegionURLBuilder(object):
    """This URL Builder required for Region URLFinder"""
    def processing(self, url):
        if 'URLFinder' in settings.REGION_FINDER:
            region = get_region()
            url = '/%s%s' % (region.abbr, url)
        return url
