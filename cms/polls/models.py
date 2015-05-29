from django.db import models
from django.utils.translation import ugettext_lazy as _


class Poll(models.Model):
    question = models.CharField(_('question'), max_length=255)
    create_date = models.DateField(_('create date'), auto_now_add=True)
    is_active = models.BooleanField(_('is active?'), default=True)

    class Meta:
        db_table = 'cms_polls'

    def __unicode__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll, related_name='choices')
    title = models.CharField(_('title'), max_length=255)
    votes = models.IntegerField(_('votes'), default=0)

    class Meta:
        db_table = 'cms_poll_choices'

    def __unicode__(self):
        return self.title
