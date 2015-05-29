import smtplib

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from cms.conf import settings


def send_letter(letter):
    try:
        postbox = letter.region.letter_postbox
    except ObjectDoesNotExist:
        letter.delivery_status.error_message = 'Postbox email unknown'
        letter.delivery_status.save()
        return

    mail = EmailMessage(
        subject=_('%(prefix)s[Letter from %(region)s: %(id)d] %(subject)s') % {
            'prefix': settings.EMAIL_SUBJECT_PREFIX,
            'region': letter.region.g_name,
            'id': letter.id,
            'subject': letter.subject},
        body=render_to_string('cms/letters/letter.txt', {'letter': letter}),
        to=(postbox.email,)
    )

    try:
        for attach in letter.attachments.all():
            mail.attach(attach.name, attach.file.read(), attach.content_type)
    except ObjectDoesNotExist:
        pass

    try:
        mail.send()
        letter.delivery_status.sent = True
        letter.delivery_status.error_message = None
    except (smtplib.SMTPSenderRefused,
            smtplib.SMTPRecipientsRefused,
            smtplib.SMTPAuthenticationError), e:
        letter.delivery_status.error_message = e

    letter.delivery_status.sent_at = timezone.now()
    letter.delivery_status.save()
