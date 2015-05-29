from django.conf import settings

from profile import ProfileModelTest
from regions.tests import RegionTest, URLFinderTest, DomainFinderTest
from menu.tests import MenuModelTest
from templatetags.tests import FilterCallMethodTest
from url_builders.tests import BuildersUtilsTest, RegionURLBuilderTest

if 'cms.components.pages' in settings.INSTALLED_APPS:
    from components.pages.tests import (PageModelTest, AttachmentModelTest,
        CommentModelTest, StarRatingModelTest)

if 'cms.components.person' in settings.INSTALLED_APPS:
    from components.person.tests import PersonModelTest
