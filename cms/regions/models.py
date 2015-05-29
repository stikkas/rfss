from django.db import models
from django.utils.translation import ugettext_lazy as _


RUSSIAN_TZ = (
    ('Europe/Kaliningrad', _('Kaliningrad Time (MSK-1)')),
    ('Europe/Moscow', _('Moscow Time (MSK)')),
    ('Asia/Yekaterinburg', _('Yekaterinburg Time (MSK+2)')),
    ('Asia/Omsk', _('Omsk Time (MSK+3)')),
    ('Asia/Krasnoyarsk', _('Krasnoyarsk Time (MSK+4)')),
    ('Asia/Irkutsk', _('Irkutsk Time (MSK+5)')),
    ('Asia/Yakutsk', _('Yakutsk Time (MSK+6)')),
    ('Asia/Vladivostok', _('Vladivostok Time (MSK+7)')),
    ('Asia/Magadan', _('Magadan Time (MSK+8)')),
)


class Region(models.Model):
    code = models.SmallIntegerField(_('code'), unique=True)
    abbr = models.CharField(_('abbreviation'), max_length=6, unique=True)
    tz = models.CharField(_('time zone'), max_length=20, choices=RUSSIAN_TZ)
    name = models.CharField(_('name'), max_length=255, unique=True)
    g_name = models.CharField(_('genitive name'), max_length=255,
        blank=True, null=True)

    class Meta:
        db_table = 'cms_region'
        ordering = ['code']
        verbose_name = _('region')
        verbose_name_plural = _('regions')
        permissions = (
            ('manage_content', _('can manage content of region')),
        )

    def __unicode__(self):
        return self.name


class RegionDepended(models.Model):
    region = models.ForeignKey('Region')

    class Meta:
        abstract = True
