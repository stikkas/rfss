import os
from django.core.files import File
from django.contrib.contenttypes.models import ContentType
from PIL import Image

from cms.conf import settings
from cms.menu.models import Menu
from cms.components.person.models import Person
from cms.tests.testcases import CMSTestCase


TEST_ROOT = os.path.dirname(__file__)


class PersonModelTest(CMSTestCase):
    def setUp(self):
        self.menu = Menu.objects.create(region=self.region, name='Menu',
            component=ContentType.objects.get_for_model(Person))
        self.img1 = open(os.path.join(TEST_ROOT, 'example_photo1.jpg'), 'rb')
        self.img2 = open(os.path.join(TEST_ROOT, 'example_photo2.jpg'), 'rb')

    def tearDown(self):
        self.img1.close()
        self.img2.close()

    def test_create_person_by_default(self):
        person = Person.objects.create(region=self.region, menu=self.menu,
            full_name="First Last", position='None',
            bio='Long Biography should be here')

        self.assertEqual('First Last', person.full_name)
        self.assertEqual('None', person.position)
        self.assertEqual('Long Biography should be here', person.bio)
        self.assertFalse(person.show_on_map)
        self.assertEqual(None, person.photo)
        error_msg = 'The \'photo\' attribute has no file associated with it.'
        with self.assertRaisesMessage(ValueError, error_msg):
            person.photo_thumb_path()
        with self.assertRaisesMessage(ValueError, error_msg):
            person.photo_thumb_url()

    def test_unique_show_on_map_field(self):
        person1 = Person.objects.create(region=self.region, menu=self.menu,
            full_name="First Last", position='None', show_on_map=True,
            bio='Long Biography should be here')

        person2 = Person.objects.create(region=self.region, menu=self.menu,
            full_name="Last First", position='None',
            bio='Short Biography should be here')

        self.assertEqual(1, Person.objects.filter(show_on_map=True).count())
        self.assertEqual(person1, Person.objects.filter(show_on_map=True)[0])
        person2.show_on_map = True
        person2.save()
        self.assertEqual(1, Person.objects.filter(show_on_map=True).count())
        self.assertEqual(person2, Person.objects.filter(show_on_map=True)[0])

    def test_create_photo_thumb(self):
        with self.settings(MEDIA_ROOT=self.TEST_MEDIA_ROOT):
            person = Person.objects.create(region=self.region, menu=self.menu,
                photo=File(self.img1), full_name="First Last", position='None',
                bio='Long Biography should be here')

            # Check path
            self.assertEqual(
                os.path.split(person.photo.path)[0],
                os.path.split(person.photo_thumb_path())[0])

            # Check name
            photo_name = os.path.split(person.photo.path)[1]
            self.assertEqual(
                '%s-thumb%s' % os.path.splitext(photo_name),
                os.path.split(person.photo_thumb_path())[1])

            # Check size
            thumb_img = Image.open(person.photo_thumb_path())
            self.assertEqual(
                (settings.PERSON_THUMB_SIZE, settings.PERSON_THUMB_SIZE),
                thumb_img.size)

    def test_update_existing_photo(self):
        with self.settings(MEDIA_ROOT=self.TEST_MEDIA_ROOT):
            person = Person.objects.create(region=self.region, menu=self.menu,
                photo=File(self.img1), full_name="First Last", position='None',
                bio='Long Biography should be here')

            old_thumb_path = person.photo_thumb_path()
            old_photo_path = person.photo.path

            person.photo = File(self.img2)
            person.save()

            self.assertFalse(os.path.exists(old_thumb_path))
            self.assertFalse(os.path.exists(old_photo_path))

    def test_update_empty_photo_field(self):
        with self.settings(MEDIA_ROOT=self.TEST_MEDIA_ROOT):
            person = Person.objects.create(region=self.region, menu=self.menu,
                full_name="First Last", position='None',
                bio='Long Biography should be here')

            person.photo = File(self.img1)
            person.save()

            p = Person.objects.get(pk=person.pk)
            self.assertTrue(os.path.exists(p.photo.path))

    def test_save_not_changed_photo(self):
        with self.settings(MEDIA_ROOT=self.TEST_MEDIA_ROOT):
            person = Person.objects.create(region=self.region, menu=self.menu,
                photo=File(self.img1), full_name="First Last", position='None',
                bio='Long Biography should be here')

            orig_thumb_path = person.photo_thumb_path()
            orig_photo_path = person.photo.path

            person.full_name = 'Something change'
            person.save()

            self.assertEqual(orig_photo_path, person.photo.path)
            self.assertEqual(orig_thumb_path, person.photo_thumb_path())

            self.assertTrue(os.path.exists(person.photo.path))
            self.assertTrue(os.path.exists(person.photo_thumb_path()))

    def test_clear_photo(self):
        with self.settings(MEDIA_ROOT=self.TEST_MEDIA_ROOT):
            person = Person.objects.create(region=self.region, menu=self.menu,
                photo=File(self.img1), full_name="First Last", position='None',
                bio='Long Biography should be here')

            orig_thumb_path = person.photo_thumb_path()
            orig_photo_path = person.photo.path

            self.assertTrue(os.path.exists(orig_photo_path))
            self.assertTrue(os.path.exists(orig_thumb_path))

            person.photo = None
            person.save()

            self.assertFalse(person.photo)
            self.assertFalse(os.path.exists(orig_photo_path))
            self.assertFalse(os.path.exists(orig_thumb_path))

    def test_delete_photo(self):
        with self.settings(MEDIA_ROOT=self.TEST_MEDIA_ROOT):
            person = Person.objects.create(region=self.region, menu=self.menu,
                photo=File(self.img1), full_name="First Last", position='None',
                bio='Long Biography should be here')

            thumb_path = person.photo_thumb_path()
            photo_path = person.photo.path

            person.delete()

            self.assertFalse(os.path.exists(thumb_path))
            self.assertFalse(os.path.exists(photo_path))
