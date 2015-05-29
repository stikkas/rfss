from django.db import models
from django.utils.html import strip_tags, strip_entities
from whoosh import index

from cms.conf import settings
from cms.components.pages.models import Page


def update_page_index(sender, instance, created, **kwargs):
    if sender is not Page:
        return

    # Raw instance may contain non unicode strings
    page = Page.objects.get(pk=instance.id)

    page_doc = {
        'id': page.id,
        'region': page.region.id,
        'name': page.name,
        'content': strip_entities(strip_tags(page.content))
    }

    ix = index.open_dir(settings.PAGE_SEARCH_INDEX)
    writer = ix.writer()
    if created:
        writer.add_document(**page_doc)
    else:
        writer.update_document(**page_doc)
    writer.commit()

models.signals.post_save.connect(update_page_index, sender=Page)
