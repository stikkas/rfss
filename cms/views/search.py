from django.utils.html import strip_tags, strip_entities
from django.utils.translation import get_language
from whoosh import index as whoosh_index
from whoosh.highlight import HtmlFormatter
from whoosh.qparser import QueryParser
from whoosh.query.terms import Term


from cms.conf import settings
from cms.regions import get_region
from cms.forms import SearchForm
from cms.components.pages.models import Page
from cms.views.utils import paginate, render
from cms.views.decorators import cms_protector


@cms_protector
def search(request):
    form = SearchForm(request.GET)
    form.full_clean()

    # Init the query string
    q = form.cleaned_data['q']

    # Where search content or title?
    search_in = form.cleaned_data['search_in']

    # Init the category search param
    menu = form.cleaned_data['menu']

    # Init date_start and date_end search params
    date_start = form.cleaned_data['date_start']
    date_end = form.cleaned_data['date_end']

    # Search in index
    hits = None
    if q is not None:
        # Open index dir
        ix = whoosh_index.open_dir(settings.PAGE_SEARCH_INDEX)

        # Make parser
        parser = QueryParser(search_in, schema=ix.schema)

        # Configure filter
        filter = Term('region', get_region().id)

        # Make query string
        qstr = q.replace('+', ' AND ').replace(' -', ' NOT ').replace(' | ', ' OR ')

        # Parse query string
        query = parser.parse(qstr)

        # And... search in index!
        hits = ix.searcher().search(query, filter=filter, limit=None)
        hits.formatter = HtmlFormatter(tagname='span', classname='text-error')


    pages = Page.objects.for_region().select_related('menu')

    # Apply filter of category
    pages = pages.filter(
        menu__in=menu.get_descendants(include_self=True))


    # Apply filter of date range
    if date_start and date_end:
        pages = pages.filter(
            create_date__gte=date_start
        ).filter(
            create_date__lte=date_end)
    elif date_start and not date_end:
        pages = pages.filter(create_date__gte=date_start)
    elif not date_start and date_end:
        pages = pages.filter(create_date__lte=date_end)


    # If not the q param
    if hits is None and not hits:
        # Total count
        hits_count = pages.count()

        # Numbered
        for num, page in enumerate(pages):
            page.num = num + 1

        # Paginate it
        pages = paginate(request, pages, 20)
    else:
        # Merge hits and filtered publications
        pages = pages.filter(pk__in=[h.get('id') for h in hits])

        # Numbered
        for num, page in enumerate(pages):
            page.num = num + 1

        # Total count
        hits_count = pages.count()
        # Paginate it
        pages = paginate(request, pages)

        # Highlight results
        for hit in hits:
            for page in pages:
                if page.id == hit['id']:
                    if search_in == 'name':
                        page.name_hit = hit.highlights('name',
                            text=strip_entities(strip_tags(page.name)))
                    if search_in == 'content':
                        page.content = hit.highlights('content',
                            text=strip_entities(strip_tags(page.content)),
                            top=5)

        if 'ix' in locals():
            ix.close()

    return render(request, 'cms/search.html', {
        'LANG': get_language(),
        'url_GET_params': form.url_GET_params(),
        'q': q,
        'search_in': search_in,
        'menu': menu,
        'pages': pages,
        'hits_count': hits_count,
        'form': form,
    })
