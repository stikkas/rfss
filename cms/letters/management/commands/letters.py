from django.core.management.base import BaseCommand

from cms.letters.models import DeliveryStatus
from cms.letters.postman import send_letter


class Command(BaseCommand):
    help = 'Async send letters'

    def handle(self, *args, **options):
        if 'sendall' in args:
            for postman in DeliveryStatus.delivery.letters_to_send():
                send_letter(postman.letter)
