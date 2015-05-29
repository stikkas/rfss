import os
import shutil
from django.test import TestCase

from cms.conf import settings
from cms.regions.models import Region
from cms.regions import _region, set_region, get_region


class CMSTestCase(TestCase):
    def _pre_setup(self):
        super(CMSTestCase, self)._pre_setup()
        self._region_setup()
        self._backup_app_settings()
        self.TEST_MEDIA_ROOT = os.path.join(settings.MEDIA_ROOT, 'tests')

    def _post_teardown(self):
        super(CMSTestCase, self)._post_teardown()
        self._region_cleanup()
        self._restore_app_settings()
        if os.path.exists(self.TEST_MEDIA_ROOT):
            shutil.rmtree(self.TEST_MEDIA_ROOT)

    def _region_setup(self):
        self.region = Region.objects.create(code=1000, abbr='test',
            name='Test', tz='Europe/Moscow')
        set_region(self.region)

    def _region_cleanup(self):
        _region.value = None

    def set_region(self, region):
        set_region(region)

    def get_region(self):
        return get_region()

    def _backup_app_settings(self):
        self._bak_app_settings = settings

    def _restore_app_settings(self):
        settings = self._bak_app_settings
