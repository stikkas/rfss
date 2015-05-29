import os, sys
from django.core.exceptions import ValidationError
from django.core.files import File
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils.dateformat import format
from django.utils import timezone

from cms.conf import settings
from cms.menu.models import Menu
from cms.components.pages.models import Page, Attachment, Comment, StarRating
from cms.tests.testcases import CMSTestCase


TEST_ROOT = os.path.dirname(__file__)


class PageModelTest(CMSTestCase):
    def setUp(self):
        self.menu = Menu.objects.create(region=self.region, name='Menu',
            component=ContentType.objects.get_for_model(Page))

    def test_create_page(self):
        page = Page.objects.create(menu=self.menu, region=self.region,
            name='Page', annotation='Annotation', content='Content')

        last_modified = timezone.now()
        self.assertEqual(
            format(page.last_modified, 'd.m.Y H:i'),
            format(last_modified, 'd.m.Y H:i'))
        self.assertEqual(self.menu, page.menu)
        self.assertEqual('Page', page.name)
        self.assertEqual(timezone.now().year, page.create_date.year)
        self.assertEqual(timezone.now().month, page.create_date.month)
        self.assertEqual(timezone.now().day, page.create_date.day)
        self.assertEqual(None, page.relevance_date)
        self.assertEqual('Annotation', page.annotation)
        self.assertEqual('Content', page.content)
        self.assertFalse(page.visible)
        self.assertFalse(page.full_preview)
        self.assertTrue(page.show_in_news)
        self.assertFalse(page.is_vised)
        self.assertEqual(None, page.last_edit_by)
        self.assertEqual(1, page.version)
        self.assertEqual(1, Page.objects.count())

    def test_vised_method(self):
        page = Page.objects.create(menu=self.menu, region=self.region,
            name='Page', annotation='Annotation', content='Content',
            visible=False)

        self.assertFalse(page.is_vised)
        page.vised()
        self.assertTrue(page.is_vised)


    def test_publish_method(self):
        page = Page.objects.create(menu=self.menu, region=self.region,
            name='Page', annotation='Annotation', content='Content',
            visible=False)

        page.is_vised = True
        self.assertFalse(page.visible)
        self.assertEqual(1, page.version)
        self.assertTrue(page.is_vised)
        page.publish()
        self.assertTrue(page.visible)
        self.assertEqual(1, page.version)
        self.assertTrue(page.is_vised)

    def test_unpublish_method(self):
        page = Page.objects.create(menu=self.menu, region=self.region,
            name='Page', annotation='Annotation', content='Content',
            visible=True)

        page.is_vised = True
        self.assertTrue(page.visible)
        self.assertEqual(1, page.version)
        self.assertTrue(page.is_vised)
        page.unpublish()
        self.assertFalse(page.visible)
        self.assertEqual(1, page.version)
        self.assertTrue(page.is_vised)

    def test_increasing_version(self):
        # Check behavior by default
        page = Page.objects.create(menu=self.menu, region=self.region,
            name='Name', annotation='Annotation', content='Content')
        self.assertEqual(1, page.version)
        page.save()
        self.assertEqual(2, page.version)

        # Check behavior when version initialized by hand
        page = Page.objects.create(menu=self.menu, region=self.region,
            name='Name', version=3, annotation='Annotation', content='Content')
        self.assertEqual(3, page.version)
        page.save()
        self.assertEqual(4, page.version)

        # Check behavior when version changed by hand
        page = Page.objects.create(menu=self.menu, region=self.region,
            name='Name', annotation='Annotation', content='Content')
        self.assertEqual(1, page.version)
        page.version = 5
        page.save()
        self.assertEqual(5, page.version)

    def test_inherited_component_properties(self):
        page = Page.objects.create(menu=self.menu, region=self.region,
            name='Name', annotation='Annotation', content='Content')
        settings.URL_BUILDERS = ()

        from cms.url_builders import get_url_builders
        self.assertEqual([], get_url_builders())

        page_id = page.id

        # Check links
        self.assertEqual('/manage/page/%s/edit/' % page_id,
            page.link_edit())
        self.assertEqual('/manage/page/%s/delete/' % page_id,
            page.link_delete())

        # Check templates
        self.assertEqual('cms/components/page_manage.html', Page.tmpl_manage())
        self.assertEqual('cms/components/page_add.html', Page.tmpl_add())
        self.assertEqual('cms/components/page_edit.html', Page.tmpl_edit())


class AttachmentModelTest(CMSTestCase):
    def setUp(self):
        menu = Menu.objects.create(region=self.region, name='Menu',
            component=ContentType.objects.get_for_model(Page))

        self.page = Page.objects.create(menu=menu, region=self.region,
            name='Page for test attachments',
            annotation='This place for annotation',
            content='This place for content')

        self.attach = open(__file__, 'rb')

        self.allowed_ext = settings.ATTACHMENT_TYPES[0]

    def tearDown(self):
        self.attach.close()

    def test_python_version_compatibility(self):
        # In code uses new futures python 2.7
        self.assertEqual('2.7', sys.version[:3])

    def test_create_attachment(self):
        attach_name = 'word.%s' % self.allowed_ext

        with self.settings(MEDIA_ROOT=self.TEST_MEDIA_ROOT):
            f = File(self.attach)
            f.name = attach_name
            attach = Attachment.objects.create(page=self.page, file=f)
            self.assertTrue(os.path.exists(attach.file.path))

    def test_delete_attachment(self):
        attach_name = 'word.%s' % self.allowed_ext
        with self.settings(MEDIA_ROOT=self.TEST_MEDIA_ROOT):
            f = File(self.attach)
            f.name = attach_name
            attach = Attachment.objects.create(page=self.page, file=f)
            attach_file_path = attach.file.path
            attach.delete()
            self.assertFalse(os.path.exists(attach_file_path))

    def test_filling_name_field(self):
        f = File(self.attach)
        f.name = 'from_file.%s' % self.allowed_ext

        # Check fill the name field from file name
        attach = Attachment.objects.create(page=self.page, file=f)
        self.assertEqual(f.name, attach.name)

        attach = Attachment.objects.create(page=self.page, file=f,
            name='custom_name.doc')
        self.assertEqual('custom_name.doc', attach.name)

    def test_attachment_limit_size(self):
        try:
            f = File(self.attach)
            f.name = 'word.%s' % self.allowed_ext
            f.size = settings.ATTACHMENT_SIZE + 1
            Attachment.objects.create(page=self.page, file=f)
        except ValidationError as e:
            self.assertEqual(e.code, 'invalid_size')
        else:
            self.assertTrue(False, 'Exception not raised')

    def test_attachment_limit_on_file_types(self):
        try:
            f = File(self.attach)
            f.name = 'test.py'
            Attachment.objects.create(page=self.page, file=f)
        except ValidationError as e:
            self.assertEqual(e.code, 'invalid_type')
        else:
            self.assertTrue(False, 'Exception not raised')

    def test_upload_zip_archive(self):
        with self.settings(MEDIA_ROOT=self.TEST_MEDIA_ROOT):
            with open(os.path.join(TEST_ROOT, 'example_attach.zip'), 'rb') as f:
                Attachment.objects.create(page=self.page, file=File(f))

        self.assertEqual(3, Attachment.objects.count())

        names = [n['name'] for n in Attachment.objects.all().values('name')]
        self.assertIn('a.doc', names)
        self.assertIn('b.doc', names)
        self.assertIn('c.doc', names)


class CommentModelTest(CMSTestCase):
    def setUp(self):
        menu = Menu.objects.create(region=self.region, name='Menu',
            component=ContentType.objects.get_for_model(Page))

        self.page = Page.objects.create(menu=menu, region=self.region,
            name='Page for test attachments',
            annotation='This place for annotation',
            content='This place for content')

        self.user = User.objects.create_user(username='commentator')

    def test_create_comment(self):
        comment = Comment.objects.create(user=self.user, page=self.page,
            message='Message')

        self.assertFalse(comment.is_changed)
        self.assertFalse(comment.visible)
        last_modified = timezone.now()
        self.assertEqual(
            format(comment.last_modified, 'd.m.Y H:i'),
            format(last_modified, 'd.m.Y H:i'))

    def test_edit_comment(self):
        comment = Comment.objects.create(user=self.user, page=self.page,
            message='Message')

        self.assertFalse(comment.is_changed)
        self.assertFalse(comment.visible)
        last_modified = timezone.now()
        self.assertEqual(
            format(comment.last_modified, 'd.m.Y H:i'),
            format(last_modified, 'd.m.Y H:i'))

        comment.save()
        self.assertFalse(comment.is_changed)

        comment.edit()
        self.assertTrue(comment.is_changed)

    def test_publish_comment(self):
        comment = Comment.objects.create(user=self.user, page=self.page,
            message='Message')

        self.assertFalse(comment.visible)
        self.assertFalse(comment.is_changed)
        comment.publish()
        self.assertTrue(comment.visible)
        self.assertFalse(comment.is_changed)

    def test_unpublish_comment(self):
        comment = Comment.objects.create(user=self.user, page=self.page,
            message='Message', visible=True)

        self.assertTrue(comment.visible)
        self.assertFalse(comment.is_changed)
        comment.unpublish()
        self.assertFalse(comment.visible)
        self.assertFalse(comment.is_changed)


class StarRatingModelTest(CMSTestCase):
    def setUp(self):
        menu = Menu.objects.create(region=self.region, name='Menu',
            component=ContentType.objects.get_for_model(Page))

        # Also creating StarRating through signals
        self.page = Page.objects.create(menu=menu, region=self.region,
            name='Page for test attachments',
            annotation='This place for annotation',
            content='This place for content')

    def test_create_star_rating(self):
        star_rating = self.page.star_rating

        default = {1:0, 2:0, 3:0, 4:0, 5:0}
        self.assertTrue(star_rating.user_votes, default)
        self.assertTrue(star_rating.anonymous_votes, default)

    def test_voting(self):
        star_rating = self.page.star_rating

        self.assertEqual(0, star_rating.user_votes[1])
        star_rating.vote_user(1)
        self.assertEqual(1, star_rating.user_votes[1])

        self.assertEqual(0, star_rating.anonymous_votes[2])
        star_rating.vote_anonymous(2)
        self.assertEqual(1, star_rating.anonymous_votes[2])

    def test_votes_property(self):
        star_rating = self.page.star_rating

        self.assertEqual(0, star_rating.votes)
        star_rating.vote_user(5)
        star_rating.vote_anonymous(5)
        star_rating.vote_user(5)
        self.assertEqual(3, star_rating.votes)

    def test_total_property(self):
        star_rating = self.page.star_rating

        self.assertEqual(0, star_rating.total)
        star_rating.vote_user(5)
        star_rating.vote_anonymous(2)
        star_rating.vote_user(1)
        self.assertEqual(8, star_rating.total)
