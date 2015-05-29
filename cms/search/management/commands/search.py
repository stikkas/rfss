# -*- coding: utf-8 -*-
import os
from django.core.management.base import BaseCommand
from django.utils.html import strip_tags, strip_entities
from whoosh import index

from cms.conf import settings
from cms.components.pages.models import Page
from cms.search.schema import PAGE_SCHEMA


class Command(BaseCommand):
    help = 'Search'

    def handle(self, *args, **options):
        if 'create_index' in args:
            if not os.path.exists(settings.PAGE_SEARCH_INDEX):
                os.makedirs(settings.PAGE_SEARCH_INDEX)
            ix = index.create_in(settings.PAGE_SEARCH_INDEX, PAGE_SCHEMA)
            writer = ix.writer()
            for page in Page.objects.all():
                writer.add_document(
                    id=page.id,
                    region=page.region.id,
                    name=page.name,
                    content=strip_entities(strip_tags(page.content))
                )
            writer.commit()