import os
from django.db import models
from django.utils.translation import ugettext_lazy as _
from PIL import Image

from cms.conf import settings
from cms.components import ComponentList
from cms.regions.models import RegionDepended
from cms.utils import upload_to


def delete_file(path):
    if os.path.exists(path):
        os.remove(path)

class Person(ComponentList, RegionDepended):
    photo = models.ImageField(_('Photography'), upload_to=upload_to,
        null=True, blank=True)
    full_name = models.CharField(_('full name'), max_length=255)
    position = models.CharField(_('position'), max_length=255)
    bio = models.TextField(_('Biography'), null=True, blank=True)
    show_on_map = models.BooleanField(_('show on map'), default=False)

    class Meta(RegionDepended.Meta):
        db_table = 'cms_com_person'
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __unicode__(self):
        return self.full_name

    def photo_thumb_url(self):
        path, photo_name = os.path.split(self.photo.path)
        url_to = os.path.split(self.photo.name)[0]
        thumbnail_name = '%s-thumb%s' % os.path.splitext(photo_name)
        return settings.MEDIA_URL + url_to + '/' + thumbnail_name

    def photo_thumb_path(self):
        path, img_name = os.path.split(self.photo.path)
        return os.path.join(path, '%s-thumb%s' % os.path.splitext(img_name))

    def save(self, *args, **kwargs):
        # Flag "show_on_map" must be unique
        if self.show_on_map:
            Person.objects.filter(region=self.region).update(show_on_map=False)

        # Save photo process and model
        if self.pk:
            prev = Person.objects.get(pk=self.pk)
            prev_photo_path = None
            prev_thumb_path = None
            if prev.photo:
                prev_thumb_path = prev.photo_thumb_path()
                prev_photo_path = prev.photo.path

            super(Person, self).save(*args, **kwargs)

            if self.photo and self.photo.path != prev_photo_path:
                # If photo exist and photo is new
                if prev_photo_path:
                    delete_file(prev_photo_path)
                if prev_thumb_path:
                    delete_file(prev_thumb_path)
                self._create_photo_thumb()
            elif not self.photo and prev_photo_path:
                # If photo cleared
                if prev_photo_path:
                    delete_file(prev_photo_path)
                if prev_thumb_path:
                    delete_file(prev_thumb_path)
        else:
            super(Person, self).save(*args, **kwargs)
            if self.photo:
                self._create_photo_thumb()

    def delete(self, using=None):
        if self.photo:
            delete_file(self.photo_thumb_path())
            self.photo.delete(save=False)
        super(Person, self).delete(using=using)

    def _create_photo_thumb(self):
        image = Image.open(self.photo.path)
        width, height = image.size

        if width > height:
            delta = width - height
            left = int(delta / 2)
            upper = 0
            right = height + left
            lower = height
        else:
            delta = height - width
            left = 0
            upper = int(delta / 2)
            right = width
            lower = width + upper

        image = image.crop((left, upper, right, lower))
        image.thumbnail(
            (settings.PERSON_THUMB_SIZE, settings.PERSON_THUMB_SIZE),
            Image.ANTIALIAS)

        path, img_name = os.path.split(self.photo.path)
        thumbnail_path = os.path.join(path,
            '%s-thumb%s' % os.path.splitext(img_name))
        image.save(thumbnail_path)
