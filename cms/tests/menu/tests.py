from django.contrib.contenttypes.models import ContentType

from cms.menu.models import Menu
from cms.components.pages.models import Page
from cms.tests.testcases import CMSTestCase


class MenuModelTest(CMSTestCase):
    def test_sort_order(self):
        menu_names = 'CBA'
        for sort_order, name in enumerate(menu_names):
            Menu.objects.create(name=name, region=self.region,
                sort_order=sort_order,
                component=ContentType.objects.get_for_model(Page))
        menus = Menu.objects.all()
        self.assertEqual('C', menus[0].name)
        self.assertEqual('B', menus[1].name)
        self.assertEqual('A', menus[2].name)

    def test_sort_order_by_name(self):
        menu_names = 'CBA'
        for name in menu_names:
            Menu.objects.create(name=name, region=self.region,
                component=ContentType.objects.get_for_model(Page))
        menus = Menu.objects.all()
        self.assertEqual('A', menus[0].name)
        self.assertEqual('B', menus[1].name)
        self.assertEqual('C', menus[2].name)
