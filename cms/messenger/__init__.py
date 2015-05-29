from cms.conf import settings
from cms.messenger.models import InboxMessage, SentboxMessage, QueueSending
try:
    if not 'mailer' in settings.INSTALLED_APPS:
        raise ImportError
    from mailer import send_mail
except ImportError:
    from django.core.mail import send_mail


def send_message(sender, recipients, subject, body, notify_on_email):
    sentbox_message = SentboxMessage.objects.create(
        owner=sender, subject=subject, body=body)
    sentbox_message.recipients.add(*recipients)

    if settings.DEBUG:
        deliver_message(sentbox_message, notify_on_email)
    else:
        QueueSending.objects.create(
            sentbox_message=sentbox_message, notify_on_email=notify_on_email)


def deliver_message(sentbox_message, notify_on_email):
    for user in sentbox_message.recipients.all():
        InboxMessage.objects.create(
            owner=user, sender=sentbox_message.owner,
            subject=sentbox_message.subject, body=sentbox_message.body)

    if notify_on_email:
        emails = [u.email for u in sentbox_message.recipients.all() if u.email]
        subject = '%s %s' % (settings.EMAIL_SUBJECT_PREFIX,
                             sentbox_message.subject)
        send_mail(recipient_list=emails, from_email=settings.DEFAULT_FROM_EMAIL,
            subject=subject, message=sentbox_message.body,
            fail_silently=True)
