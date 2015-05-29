import abc
from django.shortcuts import get_object_or_404

from cms.conf import settings
from cms.regions import set_region
from cms.regions.models import Region


class RegionFinder(object):

    __metaclass__ = abc.ABCMeta

    def definition_region(self, request):
        set_region(self.find_region(request))

    @abc.abstractmethod
    def find_region(self, request):
        """Overridable method, which should to define strategy for getting
        region from request, and return him.
        """


class URLFinder(RegionFinder):
    def find_region(self, request):
        abbr = request.path_info.split('/')[1]
        try:
            region = Region.objects.get(abbr=abbr)
            # Clear url from additional data about of region
            request.path_info = request.path_info.replace('/%s' % abbr, '', 1)
        except Region.DoesNotExist:
            return Region.objects.get(abbr=settings.DEFAULT_REGION)
        return region


class DomainFinder(RegionFinder):
    def find_region(self, request):
        domain = self._get_domain(request)

        # If not exists sub domain, then Region default is ru
        if len(domain.split('.')) == 2:
            abbr = settings.DEFAULT_REGION
        else:
            abbr = domain.split('.', 1)[0]

        try:
            region = Region.objects.get(abbr=abbr)
        except Region.DoesNotExist:
            region = Region.objects.get(abbr=settings.DEFAULT_REGION)

        return region

    def _get_domain(self, request):
        """Django's request.get_host() returns the requested host and possibly the
        port number. Return lowercased domain.
        """
        host = request.get_host()
        if ':' in host:
            domain = host.split(':')[0]
            return domain.lower()
        else:
            return host.lower()
