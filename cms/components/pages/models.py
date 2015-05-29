from django.core.exceptions import ValidationError
from django.core.files import File
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from cms.conf import settings
from cms.components import ComponentList
from cms.components.pages.fields import RatingField
from cms.regions.models import RegionDepended
from cms.utils import upload_to


class Page(ComponentList, RegionDepended):
    # Big size of attribute max_length is compatibility
    # for migration from old system
    name = models.CharField(_('name'), max_length=500)

    create_date = models.DateField(_('create date'), default=timezone.now())
    relevance_date = models.DateField(_('relevance date'),
        blank=True, null=True)

    keywords = models.CharField(_('keywords'), max_length=120,
        blank=True, null=True)

    # Field annotation for compatibility with old system data,
    # perhaps it will be removed in future
    annotation = models.TextField(_('annotation'), max_length=1000,
        null=True, blank=True)
    content = models.TextField(_('content'))

    visible = models.BooleanField(_('visible'), default=False)
    # Display content in preview mode
    full_preview = models.BooleanField(_('full preview'), default=False)
    show_in_news = models.BooleanField(_('show in news'), default=True)

    # Moderator saw this page before that this page will be published?
    is_vised = models.BooleanField(_('vised'), default=False)

    version = models.PositiveIntegerField(_('version'), default=1)

    last_edit_by = models.ForeignKey(User, related_name='edited_pages',
        null=True)
    last_modified = models.DateTimeField(_('last modified'), auto_now=True)

    class Meta(RegionDepended.Meta):
        db_table = 'cms_com_pages'
        ordering = ('-create_date',)
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')

    def __unicode__(self):
        return self.name

    def publish(self):
        if not self.visible:
            self.visible = True
            super(Page, self).save()

    def unpublish(self):
        if self.visible:
            self.visible = False
            super(Page, self).save()

    def vised(self):
        if not self.is_vised:
            self.is_vised = True
            super(Page, self).save()

    def save(self, increase_version=True, *args, **kwargs):
        # Notify moderator
        if self.is_vised:
            self.is_vised = False

        if self.pk is not None and increase_version:
            orig = Page.objects.get(pk=self.pk)
            if orig.version == self.version:
                self.version += 1

        super(Page, self).save(*args, **kwargs)


def allowed_attachment_type(file_name):
    """Check limits on file types by checking file extension of
    attachment
    """
    ext = file_name.split('.')[-1]
    return ext in settings.ATTACHMENT_TYPES

def allowed_attachment_size(file_size):
    """Check limits on max size of attachment"""
    return file_size <= settings.ATTACHMENT_SIZE

def validate_type(value):
    error_msg = _("Type .%s is invalid.")
    name = getattr(value, 'name', value)
    if not allowed_attachment_type(name):
        raise ValidationError(error_msg % name.split('.')[-1], 'invalid_type')

def validate_size(value):
    error_msg = _("Attachment file size is invalid (%.2f MiB).")
    if not allowed_attachment_size(value.file.size):
        raise ValidationError(error_msg % (value.size / 1024.0 / 1024.0),
            'invalid_size')

class Attachment(models.Model):
    page = models.ForeignKey(Page, related_name='attachments')
    name = models.CharField(_('name'), max_length=510)
    file = models.FileField(_('file'), upload_to=upload_to,
        validators=[validate_type, validate_size])

    class Meta:
        db_table = 'cms_com_pages_attachment'
        verbose_name = _('attachment')
        verbose_name_plural = _('attachments')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Add name from a file name, if name not set directly.
        # This check should be first, because next two checks depends from it
        if not self.name:
            self.name = self.file.name

        # This checks need if the file came not from a form
        # or not from a zip file
        validate_type(self.name)
        validate_size(self.file)

        # Unpack zip archive and save unpacked files,
        # not save current zip file
        if self.name.lower()[-3:] == 'zip':
            return self._unpack_zip()

        super(Attachment, self).save(*args, **kwargs)

    def _unpack_zip(self):
        from tempfile import NamedTemporaryFile
        from zipfile import ZipFile

        # Open a zip file
        with ZipFile(self.file) as zip:  # NOTICE: work in python 2.7+
            # Get list of files from zip archive
            for attach in zip.namelist():
                # Skip directories, without any raise Exception
                if attach.endswith('/'):
                    continue
                # Skip not allowed file types, without any raise Excpetion
                if not allowed_attachment_type(attach):
                    continue

                # Create a temporary file for unpacking from a zip archive,
                # because zip.open(attach) return not a fit file object
                # for django File
                with NamedTemporaryFile() as temp:
                    # Write data from file in zip to a temp file
                    with zip.open(attach) as f:
                        temp.write(f.read())

                    # For support zipped files in windows, MacOS or Linux
                    try:
                        path = attach.decode('utf-8')
                    except UnicodeDecodeError:
                        path = attach.decode('cp866')
                    except UnicodeEncodeError:
                        path = attach

                    # Get file name from path
                    name = path.split('/')[-1]

                    # Skip files, which have size more than max allowed size
                    if not allowed_attachment_size(File(temp).size):
                        continue

                    Attachment.objects.create(
                        page=self.page, name=name, file=File(temp))

    def delete(self, *args, **kwargs):
        self.file.delete(save=False)
        super(Attachment, self).delete(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments')
    page = models.ForeignKey(Page, related_name='comments')

    message = models.TextField(_('message'))
    last_modified = models.DateTimeField(_('last modified'), auto_now_add=True)

    is_changed = models.BooleanField(_('is changed?'), default=False)

    visible = models.BooleanField(_('visible'), default=False)

    class Meta:
        db_table = 'cms_com_page_comments'
        ordering = ('last_modified',)
        verbose_name = _('page comment')
        verbose_name_plural = _('page comments')

    def publish(self):
        if not self.visible:
            self.visible = True
            super(Comment, self).save()

    def unpublish(self):
        if self.visible:
            self.visible = False
            super(Comment, self).save()

    def edit(self, *args, **kwargs):
        self.is_changed = True
        super(Comment, self).save(*args, **kwargs)


class StarRating(models.Model):
    page = models.OneToOneField(Page, related_name='star_rating')
    user_votes = RatingField()
    anonymous_votes = RatingField()

    class Meta:
        db_table = 'cms_com_page_star_rating'

    def vote_anonymous(self, rate):
        rate = int(rate)
        self.anonymous_votes[rate] += 1
        self.save()

    def vote_user(self, rate):
        rate = int(rate)
        self.user_votes[rate] += 1
        self.save()

    @property
    def votes(self):
        return sum(self.user_votes.values() + self.anonymous_votes.values())

    @property
    def total(self):
        user_votes = [pair[0] * pair[1] for pair in self.user_votes.items()]
        anonymous_votes = [pair[0] * pair[1]
                           for pair in self.anonymous_votes.items()]
        return sum(user_votes + anonymous_votes)


def create_star_rating(sender, instance, **kwargs):
    if sender is not Page: return
    StarRating.objects.get_or_create(page_id=instance.id)

models.signals.post_save.connect(create_star_rating, sender=Page)
