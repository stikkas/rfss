from django.db.models import Manager
from django.db.models.query import QuerySet

from cms.regions import get_region


class RegionQS(QuerySet):
    def for_region(self, region=None):
        return self.filter(region=region or get_region())

class RegionManager(Manager):
    def get_query_set(self):
        return RegionQS(model=self.model, using=self._db)

    def for_region(self, region=None):
        return self.get_query_set().for_region(region=region)
