from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from cms.regions.models import Region, RegionDepended
from cms.conf import settings
from cms.utils import upload_to


class Rubric(models.Model):
    name = models.CharField(_('rubrics'), max_length=255, unique=True)

    class Meta:
        verbose_name = _('rubric')
        verbose_name_plural = _('rubrics')

    def __unicode__(self):
        return self.name


class Letter(RegionDepended):
    COUNTRIES = (
        (_('Russia'), (
            ('RU-AD', _('Republic of Adygea'),),
            ('RU-AL', _('Altai Republic'),),
            ('RU-BA', _('Republic of Bashkortostan'),),
            ('RU-BU', _('Republic of Buryatia'),),
            ('RU-CE', _('Chechen Republic'),),
            ('RU-CU', _('Chuvash Republic'),),
            ('RU-DA', _('Republic of Dagestan'),),
            ('RU-IN', _('Republic of Ingushetia'),),
            ('RU-KB', _('Kabardino-Balkar Republic'),),
            ('RU-KL', _('Republic of Kalmykia'),),
            ('RU-KC', _('Karachay-Cherkess Republic'),),
            ('RU-KR', _('Republic of Karelia'),),
            ('RU-KK', _('Republic of Khakassia'),),
            ('RU-KO', _('Komi Republic'),),
            ('RU-ME', _('Mari El Republic'),),
            ('RU-MO', _('Republic of Mordovia'),),
            ('RU-SA', _('Sakha (Yakutia) Republic'),),
            ('RU-SE', _('Republic of North Ossetia-Alania'),),
            ('RU-TA', _('Republic of Tatarstan'),),
            ('RU-TY', _('Tuva Republic'),),
            ('RU-UD', _('Udmurt Republic'),),
            ('RU-ALT', _('Altai Krai'),),
            ('RU-KAM', _('Kamchatka Krai'),),
            ('RU-KHA', _('Khabarovsk Krai'),),
            ('RU-KDA', _('Krasnodar Krai'),),
            ('RU-KYA', _('Krasnoyarsk Krai'),),
            ('RU-PER', _('Perm Krai'),),
            ('RU-PRI', _('Primorsky Krai'),),
            ('RU-STA', _('Stavropol Krai'),),
            ('RU-ZAB', _('Zabaykalsky Krai'),),
            ('RU-AMU', _('Amur Oblast'),),
            ('RU-ARK', _('Arkhangelsk Oblast'),),
            ('RU-AST', _('Astrakhan Oblast'),),
            ('RU-BEL', _('Belgorod Oblast'),), ('RU-BRY', _('Bryansk Oblast'),),
            ('RU-CHE', _('Chelyabinsk Oblast'),),
            ('RU-IRK', _('Irkutsk Oblast'),),
            ('RU-IVA', _('Ivanovo Oblast'),),
            ('RU-KGD', _('Kaliningrad Oblast'),),
            ('RU-KLU', _('Kaluga Oblast'),),
            ('RU-KEM', _('Kemerovo Oblast'),),
            ('RU-KIR', _('Kirov Oblast'),),
            ('RU-KOS', _('Kostroma Oblast'),),
            ('RU-KGN', _('Kurgan Oblast'),),
            ('RU-KRS', _('Kursk Oblast'),),
            ('RU-LEN', _('Leningrad Oblast'),),
            ('RU-LIP', _('Lipetsk Oblast'),),
            ('RU-MAG', _('Magadan Oblast'),),
            ('RU-MOS', _('Moscow Oblast'),),
            ('RU-MUR', _('Murmansk Oblast'),),
            ('RU-NIZ', _('Nizhny Novgorod Oblast'),),
            ('RU-NGR', _('Novgorod Oblast'),),
            ('RU-NVS', _('Novosibirsk Oblast'),),
            ('RU-OMS', _('Omsk Oblast'),),
            ('RU-ORE', _('Orenburg Oblast'),),
            ('RU-ORL', _('Oryol Oblast'),),
            ('RU-PNZ', _('Penza Oblast'),),
            ('RU-PSK', _('Pskov Oblast'),),
            ('RU-ROS', _('Rostov Oblast'),),
            ('RU-RYA', _('Ryazan Oblast'),),
            ('RU-SAK', _('Sakhalin Oblast'),),
            ('RU-SAM', _('Samara Oblast'),),
            ('RU-SAR', _('Saratov Oblast'),),
            ('RU-SMO', _('Smolensk Oblast'),),
            ('RU-SVE', _('Sverdlovsk Oblast'),),
            ('RU-TAM', _('Tambov Oblast'),),
            ('RU-TOM', _('Tomsk Oblast'),),
            ('RU-TUL', _('Tula Oblast'),),
            ('RU-TVE', _('Tver Oblast'),),
            ('RU-TYU', _('Tyumen Oblast'),),
            ('RU-ULY', _('Ulyanovsk Oblast'),),
            ('RU-VLA', _('Vladimir Oblast'),),
            ('RU-VGG', _('Volgograd Oblast'),),
            ('RU-VLG', _('Vologda Oblast'),),
            ('RU-VOR', _('Voronezh Oblast'),),
            ('RU-YAR', _('Yaroslavl Oblast'),),
            ('RU-MOW', _('Moscow'),),
            ('RU-SPE', _('Saint Petersburg'),),
            ('RU-YEV', _('Jewish Autonomous Oblast'),),
            ('RU-CHU', _('Chukotka Autonomous Okrug'),),
            ('RU-KHM', _('Khanty-Mansi Autonomous Okrug'),),
            ('RU-NEN', _('Nenets Autonomous Okrug'),),
            ('RU-YAN', _('Yamalo-Nenets Autonomous Okrug'),),
            ('RU-CR', _('Republic of Crimea'),),
            ('RU-SEV', _('Sevastopol'),),
        ),),
    )

    first_name = models.CharField(_('first name'), max_length=20)
    last_name = models.CharField(_('last name'), max_length=20)
    patronymic = models.CharField(_('patronymic'), max_length=20)
    organization = models.CharField(_('organization'), max_length=120,
                                    null=True, blank=True)

    country = models.CharField(_('country / region'), max_length=7, choices=COUNTRIES)
    district = models.CharField(_('district'), max_length=30,
                                blank=True, null=True)
    settlement = models.CharField(_('city / settlement'), max_length=30)
    street = models.CharField(_('street'), max_length=30)
    house = models.CharField(_('house'), max_length=10)
    building = models.CharField(_('building'), max_length=10,
                                blank=True, null=True)
    flat = models.CharField(_('flat / office'), max_length=10,
                            blank=True, null=True)
    postcode = models.CharField(_('zip code'), max_length=10)

    phone = models.CharField(_('phone'), max_length=30)
    email = models.EmailField(_('email'))

    rubric = models.CharField(_('rubric'), max_length=255,
                              blank=True, null=True)
    subject = models.CharField(_('subject'), max_length=120)
    message = models.TextField(_('message'), max_length=2000)

    reply_by_email = models.BooleanField(_('reply by email'), default=True)
    reply_by_post = models.BooleanField(_('reply by post'), default=False)

    filing_datetime = models.DateTimeField(_('filing datetime'), auto_now_add=True)

    class Meta:
        verbose_name = _('letter')
        verbose_name_plural = _('letters')

    def __unicode__(self):
        return u'[%d: %s] %s' % (self.pk, self.rubric, self.subject)


def attach_validator(attach):
    def bytes_to_mb(b):
        return b / 1024.0 / 1024.0

    if attach.size > settings.LETTERS_ATTACH_MAX_SIZE:
        size_files = (bytes_to_mb(settings.LETTERS_ATTACH_MAX_SIZE),
                      bytes_to_mb(attach.size))
        raise ValidationError(_('Exceeded the maximum file size of %(size).2f MB: '
                                '(current %(size).2f MB)') % {'size': size_files})
    if attach.content_type not in settings.LETTERS_ATTACH_CONTENT_TYPES:
        ext = attach.name.split('.')[-1]
        raise ValidationError(_('Invalid file type: %(ext)s') % {'ext': ext})


class Attach(models.Model):
    letter = models.ForeignKey(Letter, related_name='attachments')
    name = models.CharField(_('name'), max_length=255)
    content_type = models.CharField('content type', max_length=255)
    file = models.FileField(_('file'), upload_to=upload_to,
                            validators=[attach_validator])


class DeliveryStatusManager(models.Manager):
    def failed_letters(self):
        return self.filter(error_message__is_null=False, sent=False)

    def letters_to_send(self):
        return self.filter(sent_at=None)


class DeliveryStatus(models.Model):
    letter = models.OneToOneField(Letter, related_name='delivery_status')
    sent = models.BooleanField(_('is sent?'), default=False)
    error_message = models.CharField(_('error message'), max_length=255,
                                     blank=True, null=True)
    last_attempt = models.DateTimeField(_('last attempt'), null=True)
    sent_at = models.DateTimeField(_('sent at'), null=True)

    object = models.Manager()
    delivery = DeliveryStatusManager()

    def save(self, *args, **kwargs):
        if self.pk:
            self.last_attempt = timezone.now()
        return super(DeliveryStatus, self).save(*args, **kwargs)


class PostBox(models.Model):
    region = models.OneToOneField(Region, related_name='letter_postbox')
    email = models.EmailField(_('email'))

    class Meta:
        verbose_name = _('post box')
        verbose_name_plural = _('post boxes')

    def __unicode__(self):
        return u'%s [%s]' % (self.region.name, self.email)


def create_delivery_status(sender, instance, **kwargs):
    if sender is Letter and kwargs['created']:
        DeliveryStatus.object.create(letter=instance)

models.signals.post_save.connect(create_delivery_status, sender=Letter)
