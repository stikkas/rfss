from django.contrib.auth.models import User
from django.test import TestCase


class ProfileModelTest(TestCase):
    def test_signal_create_profile(self):
        u = User.objects.create_user(username='simple')
        try:
            u.profile
        except u.profile.DoesNotExist:
            self.assertTrue(False, 'Profile is not created automatically')
