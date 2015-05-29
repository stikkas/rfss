from threading import local
from django.utils.importlib import import_module

from cms.conf import settings


_region = local()


class RegionNotSet(BaseException): pass


def get_region():
    try:
        if _region.value is None:
            raise AttributeError
        return _region.value
    except AttributeError:
        raise RegionNotSet('Before get region, you should set it in system '
                           'through the set_region function')

def set_region(region):
    if region is not None:
        _region.value = region

def get_region_finder():
    module_path, cls_name = settings.REGION_FINDER.rsplit('.', 1)
    module = import_module(module_path)
    return getattr(module, cls_name)()
