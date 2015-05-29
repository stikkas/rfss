from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.regions.models import Region
from cms.regions.managers import RegionManager


class Counter(models.Model):
    region = models.OneToOneField(Region, related_name='counter')

    id = models.IntegerField(_('id'), primary_key=True)
    token = models.CharField(_('token'), max_length=255)

    object = RegionManager()

    class Meta:
        db_table = 'cms_metrika_counter'
        verbose_name = _('counter')
        verbose_name_plural = _('counters')

    def __unicode__(self):
        return "%d (%s)" % (self.id, self.region.name)
