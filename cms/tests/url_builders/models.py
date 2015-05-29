from django.db import models

from cms.url_builders import permalink


class Tester(models.Model):
    @models.permalink
    def get_absolute_url(self):
        return 'check_link',

    @permalink
    def check_link(self):
        return 'link', [1]