from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db import models


GENDERS = (
    ('M', _('Men')),
    ('W', _('Woman')),
)

class Profile(models.Model):
    user = models.OneToOneField(User)

    birthday = models.DateField(_('birthday'),
        blank=True, null=True)
    gender = models.CharField(_('gender'),
        max_length=1, choices=GENDERS, blank=True, null=True)
    department = models.CharField(_('department'),
        max_length=255, blank=True, null=True)
    position = models.CharField(_('position'),
        max_length=255, blank=True, null=True)
    phone = models.CharField(_('phone'),
        max_length=50, blank=True, null=True)

    is_manager = models.BooleanField(_('is manager?'), default=False)
    is_moderator = models.BooleanField(_('is moderator?'), default=False)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            Profile.objects.get(user=instance)
        except Profile.DoesNotExist:
            Profile.objects.create(user=instance)

models.signals.post_save.connect(create_user_profile, sender=User)
