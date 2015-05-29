from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Message(models.Model):
    subject = models.CharField(_('subject'), max_length=255)
    body = models.TextField(_('content'))
    create_date = models.DateTimeField(_('create date'), auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-create_date']

    def __unicode__(self):
        return self.subject


class InboxManager(models.Manager):
    def new(self):
        return self.get_query_set().filter(
            is_new=True
        ).select_related('sender')


class InboxMessage(Message):
    owner = models.ForeignKey(User, related_name='inbox_messages')
    # Call user.sent_messages.all() return all messages from sentbox other
    # users where the user is sender
    sender = models.ForeignKey(User, related_name='sent_messages')
    is_new = models.BooleanField(_('is new?'), default=True)

    objects = InboxManager()

    class Meta(Message.Meta):
        db_table = 'cms_messenger_inbox'
        verbose_name = _('inbox message')
        verbose_name_plural = _('inbox messages')

    @property
    def reply_subject(self):
        if self.subject.startswith('Re: '):
            return self.subject
        return 'Re: %s' % self.subject

    @property
    def reply_body(self):
        reply_body = self.body
        bq_tag = {'start': '[blockquote]', 'end': '[/blockquote]'}

        # Clean from old blockquote tags
        bq_start_index = self.body.find(bq_tag['start'])
        bq_end_index = self.body.rfind(bq_tag['end']) + len(bq_tag['end'])
        if bq_start_index != -1 and bq_end_index != -1:
            reply_body = self.body.replace(
                self.body[bq_start_index:bq_end_index], '')

        return '\n\n\n[blockquote]%s[/blockquote]' % reply_body


class SentboxMessage(Message):
    owner = models.ForeignKey(User, related_name='sentbox_messages')
    # Call user.recipient_messages.all() return all messages from inbox other
    # users where the user is recipients
    recipients = models.ManyToManyField(User, related_name='recipient_messages')

    class Meta(Message.Meta):
        db_table = 'cms_messenger_sentbox'
        verbose_name = _('sentbox message')
        verbose_name_plural = _('sentbox messages')


class QueueSending(models.Model):
    sentbox_message = models.OneToOneField(SentboxMessage,
        related_name='pending')
    notify_on_email = models.BooleanField(default=False)

    class Meta:
        db_table = 'cms_messenger_queue_sending'
