from django.test.client import RequestFactory

from cms.conf import settings
from cms.regions import set_region, get_region, get_region_finder, _region
from cms.regions.finder import URLFinder, DomainFinder
from cms.tests.testcases import CMSTestCase


class RegionTest(CMSTestCase):
    def test_set_region(self):
        set_region(self.region)
        region = _region.value
        self.assertEqual(self.region, region)

    def test_get_region(self):
        _region.value = self.region
        region = get_region()
        self.assertEqual(self.region, region)

    def test_get_region_finder(self):
        settings.REGION_FINDER = 'cms.regions.finder.URLFinder'
        finder = get_region_finder()
        self.assertEqual('URLFinder', finder.__class__.__name__)


class URLFinderTest(CMSTestCase):
    def test_url_finder(self):
        self.factory = RequestFactory()
        request = self.factory.get('/%s/path/to/view' % self.region.abbr)
        finder = URLFinder()
        finder.definition_region(request)
        self.assertEqual(self.region, get_region())


class DomainFinderTest(CMSTestCase):
    def test_domain_finder(self):
        self.factory = RequestFactory()
        request = self.factory.get('/')
        request.get_host = lambda: '%s.test.lh' % self.region.abbr
        finder = DomainFinder()
        finder.definition_region(request)
        self.assertEqual(self.region, get_region())
