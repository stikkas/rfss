from django.db import models

from cms.menu.models import Menu
from cms.regions.managers import RegionQS
from cms.url_builders import permalink
from cms.views.utils import paginate


class Comp(object):
    def __init__(self, request, menu, paginate=paginate):
        self._elements = []
        self._element = False
        self.request = request
        self.menu = menu
        self.model_class = menu.component.model_class()
        self.paginate = paginate

    @property
    def elements(self):
        if not self._elements:
            if issubclass(self.model_class, ComponentList):
                self._elements = self.model_class.get_for(menu=self.menu)
                if self.paginate:
                    self._elements = self.paginate(self.request, self._elements)
        return self._elements

    @property
    def element(self):
        if not self._element:
            if issubclass(self.model_class, ComponentSingle):
                self._element = self.model_class.get_for(menu=self.menu)
        return self._element

    @permalink
    def link_add_element(self):
        return 'cms:%s_add' % self.model_class.__name__.lower(), [self.menu.id]


class ComponentManager(models.Manager):
    def get_query_set(self):
        return RegionQS(model=self.model, using=self._db)

    def for_region(self, region=None):
        return self.get_query_set().for_region(region=region)


class Component(object):
    @classmethod
    def get_for(cls, menu):
        raise NotImplementedError

    @classmethod
    def tmpl_manage(cls):
        return 'cms/components/%s_manage.html' % cls.__name__.lower()

    @classmethod
    def tmpl_ctrl(cls):
        return 'cms/components/%s_ctrl.html' % cls.__name__.lower()

    @classmethod
    def tmpl_edit(cls):
        return 'cms/components/%s_edit.html' % cls.__name__.lower()

    @classmethod
    def tmpl_front(cls):
        return '%s_front.html' % cls.__name__.lower()


class ComponentList(models.Model, Component):
    menu = models.ForeignKey(Menu)

    objects = ComponentManager()

    class Meta:
        abstract = True

    @classmethod
    def get_for(cls, menu):
        return cls.elements(menu)

    @classmethod
    def elements(cls, menu):
        return cls.objects.filter(menu=menu)

    @permalink
    def link_edit(self):
        return 'cms:%s_edit' % self.__class__.__name__.lower(), [self.pk]

    @classmethod
    def tmpl_add(cls):
        return 'cms/components/%s_add.html' % cls.__name__.lower()

    @permalink
    def link_delete(self):
        return 'cms:%s_delete' % self.__class__.__name__.lower(), [self.pk]

    @permalink
    def link_detail(self):
        return '%s_detail' % self.__class__.__name__.lower(), [self.pk]

class ComponentSingle(models.Model, Component):
    menu = models.OneToOneField(Menu)

    objects = ComponentManager()

    class Meta:
        abstract = True

    @classmethod
    def get_for(cls, menu):
        return cls.objects.get(menu=menu)

    class Meta:
        abstract = True

    @permalink
    def link_edit(self):
        return 'cms:%s_edit' % self.__class__.__name__.lower(), [self.pk]
