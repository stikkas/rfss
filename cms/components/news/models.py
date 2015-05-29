from cms.components import ComponentList
from cms.components.pages.models import Page
from cms.regions.models import RegionDepended


class News(ComponentList, RegionDepended):
    class Meta(RegionDepended.Meta):
        db_table = 'cms_com_news'

    @classmethod
    def elements(cls, menu=None):
        return Page.objects.filter(
            show_in_news=True
        ).select_related('menu').for_region().order_by('-create_date')
