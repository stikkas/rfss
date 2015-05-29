from django import template
from django.core.urlresolvers import reverse

from cms.conf import settings
from cms.url_builders import build_url, get_url_builders, redirect
from cms.url_builders import RegionURLBuilder
from cms.tests.testcases import CMSTestCase

from cms.tests.url_builders.models import Tester


class URLBuilder(object):
    def processing(self, url):
        return '/%s%s' % ('test', url)

class BuildersUtilsTest(CMSTestCase):
    urls = 'cms.tests.url_builders.urls'

    def setUp(self):
        settings.URL_BUILDERS = ('cms.tests.url_builders.tests.URLBuilder',)

    def test_get_url_builders(self):
        builders = get_url_builders()
        self.assertEqual(1, len(builders))
        self.assertEqual('URLBuilder', builders[0].__class__.__name__)

    def test_build_url(self):
        url = '/path/to/'
        self.assertEqual('/test/path/to/', build_url(url))

    def test_redirect(self):
        # Redirect by view's name
        response = redirect('check_link')
        self.assertEqual('/test/check_link/', response['Location'])

        # Redirect by a simple link
        response = redirect('/check_link/')
        self.assertEqual('/test/check_link/', response['Location'])

        # Redirect by model instance
        response = redirect(Tester())
        self.assertEqual('/test/check_link/', response['Location'])

    def test_permalink(self):
        model = Tester()
        self.assertEqual('/test/link/1/', model.check_link())


class RegionURLBuilderTest(CMSTestCase):
    urls = 'cms.tests.url_builders.urls'

    def setUp(self):
        settings.URL_BUILDERS = ('cms.url_builders.RegionURLBuilder',)

    def render_template(self, text):
        t = template.Template(text)
        c = template.Context()
        return t.render(c)

    def test_render_link_tag(self):
        self.assertEqual('/test/check_link/', self.render_template(
            '{% load cms_tags %}'
            '{% link check_link %}'
        ))

    def test_processing_method(self):
        url = reverse('check_link')
        builder = RegionURLBuilder()
        self.assertEqual('/test/check_link/', builder.processing(url))
