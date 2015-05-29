from django.core.management.base import BaseCommand

from cms.messenger import deliver_message
from cms.messenger.models import QueueSending


class Command(BaseCommand):
    help = 'Messenger'

    def handle(self, *args, **options):
        if 'deliver' in args:
            for queue in QueueSending.objects.all():
                deliver_message(
                    sentbox_message=queue.sentbox_message,
                    notify_on_email=queue.notify_on_email)
                queue.delete()
