# -*- coding: utf-8 -*-
import urlparse
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, render as _render
from whoosh import index as whoosh_index
from whoosh.qparser.default import QueryParser, MultifieldParser
from whoosh.query.terms import Term
try:
    from mailer import send_mail
except ImportError:
    from django.core.mail import send_mail

from cms.conf import settings
from cms.polls.models import Poll
from cms.regions import get_region, set_region
from cms.regions.models import Region
from cms.menu.models import Menu
from cms.components import Comp
from cms.components.pages.models import Page, Comment, StarRating
from cms.components.person.models import Person
from cms.metrika.models import Counter
from cms.url_builders import redirect

from web.forms import RegistrationForm, PollForm, CommentForm, LetterForm


def render(request, template, context):
    english = Menu.objects.root_nodes().for_region(
        Region.objects.get(abbr='ru')).filter(name='English')[0]
    contact = Menu.objects.root_nodes().for_region().filter(name=u'Контакты')[0]
    form = AuthenticationForm(request)

    try:
        counter = Counter.object.get(region=get_region())
    except Counter.DoesNotExist:
        counter = None

    main_menu = Menu.objects.root_nodes().for_region().get(name=u'Основное меню')
    persons = Person.objects.select_related('region').filter(show_on_map=True)
    context.update({
        'persons': persons,
        'english': english,
        'contact': contact,
        'auth_form': form,
        'request': request,
        'region': get_region(),
        'regions': Region.objects.all(),
        'counter': counter,
    }),
    context.setdefault('main_menu', Menu.objects.filter(parent=main_menu))
    return _render(request, template, context)


def index(request):
    widgets = dict()

    # Fill widget ordinance
    red = Menu.objects.for_region().get(name__startswith=u'Президиума СС')
    blue = Menu.objects.for_region().get(name__startswith=u'Совета судей')
    widgets['ordinance'] = {
        'resolution': Menu.objects.for_region().get(name=u'Постановления'),
        'red': Page.objects.filter(menu=red).filter(visible=True)[:2],
        'blue': Page.objects.filter(menu=blue).filter(visible=True)[:2],
    }

    # Fill widget activity
    widgets['activity'] = Menu.objects.for_region().get(name=u'Мероприятия')

    # Fill widget honors
    widgets['honors'] = Menu.objects.for_region().get(
        name=u'Награды и поздравления')

    # Fill widget persons
    widgets['persons_menu'] = Menu.objects.for_region().get(
        name__startswith=u'Совет судей')
    widgets['persons'] = Person.objects.for_region().order_by('?')[:2]

    # Fill widget initiatives
    menu = Menu.objects.for_region().get(name=u'Инициативы')
    widgets['initiatives_menu'] = menu
    widgets['initiatives'] = Page.objects.filter(
        menu=menu
    ).filter(
        visible=True
    )[:4]

    # Fill widget legal reform
    menu = Menu.objects.for_region().get(name=u'Правовая основа')
    widgets['legal_reform_menu'] = menu
    widgets['legal_reform'] = Page.objects.filter(
        menu=menu
    ).filter(
        visible=True
    )[:3]

    # Fill widget interview
    menu = Menu.objects.for_region(
        Region.objects.get(abbr='ru')
    ).get(name=u'Интервью')
    widgets['interview_menu'] = menu
    try:
        widgets['interview'] = Page.objects.filter(
            menu=menu
        ).filter(
            visible=True
        ).order_by('?')[0]
    except IndexError:
        pass

    # Fill widgets interview
    menus = Menu.objects.filter(name=u'Анонсы мероприятий')
    try:
        widgets['events'] = Page.objects.filter(
            menu__in=menus
        ).filter(
            visible=True
        ).order_by('-create_date')[0]
    except IndexError:
        pass

    return render(request, 'index.html', {
        'index_page': True,
        'widgets': widgets,
    })

def menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)

    if menu.get_children():
        menu = menu.get_children()[0]
        return redirect('menu', pk=menu.id)

    menus = {'level2': [], 'level3': []}
    if menu.level == 2:
        for m in menu.get_siblings(include_self=True):
            if m == menu:
                m.active = True
            menus['level2'].append(m)
        menus['level3'] = menu.get_children()
    elif menu.level == 3:
        for m in menu.parent.get_siblings(include_self=True):
            if m == menu.parent:
                m.active = True
            menus['level2'].append(m)

        for m in menu.get_siblings(include_self=True):
            if m == menu:
                m.active = True
            menus['level3'].append(m)

    context = {
        'menu': menu,
        'menus': menus,
        'comp': Comp(request, menu),
    }
    main_menu = menu.get_root().get_children()
    if main_menu:
        context['main_menu'] = main_menu
    return render(request, 'menu.html', context)

def page_detail(request, pk):
    page = Page.objects.get(pk=pk)
    menu = page.menu
    comments = Comment.objects.filter(page=page).filter(
        visible=True).select_related('user')

    if menu.get_children():
        menu = menu.get_children()[0]

    menus = {'level2': [], 'level3': []}
    if menu.level == 2:
        for m in menu.get_siblings(include_self=True):
            if m == menu:
                m.active = True
            menus['level2'].append(m)
        menus['level3'] = menu.get_children()
    elif menu.level == 3:
        for m in menu.parent.get_siblings(include_self=True):
            if m == menu.parent:
                m.active = True
            menus['level2'].append(m)

        for m in menu.get_siblings(include_self=True):
            if m == menu:
                m.active = True
            menus['level3'].append(m)

    if page.keywords:
        # Open index dir
        ix = whoosh_index.open_dir(settings.PAGE_SEARCH_INDEX)
        # Make parser
        parser = MultifieldParser(['content', 'name'], schema=ix.schema)
        # Configure filter
        filter = Term('region', page.region.id)
        # Make query string
        qstr = page.keywords.replace('+', ' AND ').replace(' -', ' NOT ').replace(' | ', ' OR ')
        # Parse query string
        query = parser.parse(qstr)
        # And... search in index!
        with ix.searcher() as searcher:
            hits = ix.searcher().search(query, filter=filter, limit=None)
            similar_pages = Page.objects.filter(
                pk__in=[h.get('id') for h in hits if h.get('id') != page.id]
            ).order_by('?')[:5]

    context = {
        'page': page,
        'comments': comments,
        'menus': menus,
        'menu': menu,
        'similar_pages': locals().get('similar_pages')
    }

    # Comments
    if request.method == 'POST' and request.POST.get('submit_comment'):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid() and request.user.is_authenticated():
            comment_form.add_comment()
            context['comment_success'] = True
            # Clear form
            initial = {'user': request.user.id, 'page': page.id}
            comment_form = CommentForm(initial=initial)
    else:
        initial = {'user': request.user.id, 'page': page.id}
        comment_form = CommentForm(initial=initial)

    try:
        context['star_rating'] = StarRating.objects.get(page=page)
    except StarRating.DoesNotExist:
        context['star_rating'] = StarRating.objects.create(page=page)

    context['comment_form'] = comment_form

    return render(request, 'page_detail.html', context)


def star_rating_vote(request, pk):
    star_rating = get_object_or_404(StarRating, pk=pk)
    data = {'total': star_rating.total, 'votes': star_rating.votes}

    if request.get_signed_cookie('star_rating-%d' % star_rating.id, False):
        data['message'] = u'Вы уже ставили оценку.'
        return HttpResponse(json.dumps(data),
                            content_type='application/javascript')

    if request.method == 'POST' and request.POST.get('rate'):
        rate = int(request.POST['rate'])
        if rate in range(1, 6):
            if request.user.is_authenticated():
                star_rating.vote_user(rate)
            else:
                star_rating.vote_anonymous(rate)
            data = {'total': star_rating.total,
                    'votes': star_rating.votes,
                    'message': u'Вы поставили %d. Спасибо за оценку.' % rate}

    response = HttpResponse(json.dumps(data),
                        content_type='application/javascript')
    response.set_signed_cookie('star_rating-%d' % star_rating.id,
                               'voted', max_age=365*24*60*60)
    return response

def page_comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.is_authenticated() and comment.user == request.user:
        comment.delete()
    return redirect('page_detail', pk=comment.page.id)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())

    redirect_to = request.REQUEST.get('next', '')
    netloc = urlparse.urlparse(redirect_to)[1]

    # Use default setting if redirect_to is empty
    if not redirect_to:
        redirect_to = settings.LOGIN_REDIRECT_URL

    # Heavier security check -- don't allow redirection to a different
    # host.
    elif netloc and netloc != request.get_host():
        redirect_to = 'index'

    return redirect(redirect_to)

def logout(request):
    auth_logout(request)

    redirect_to = request.REQUEST.get('next', '')
    netloc = urlparse.urlparse(redirect_to)[1]

    # Use default setting if redirect_to is empty
    if not redirect_to:
        redirect_to = settings.LOGIN_REDIRECT_URL

    # Heavier security check -- don't allow redirection to a different
    # host.
    elif netloc and netloc != request.get_host():
        redirect_to = 'index'

    return redirect(redirect_to)

def registration(request):
    if request.user.is_authenticated():
        return redirect('index')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.register()
            success = True
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {
        'success': locals().get('success'),
        'form': form,
    })

def search(request):
    # Init the query string
    q = request.GET.get('q')

    # Where search content or title?
    search_in = request.GET.get('search_in', 'content')
    if search_in not in ('content', 'name',):
        search_in = 'content'
        # No need show a publication content if q is empty
    if not q:
        search_in = 'name'

    # Init the region search param
    region_id = request.GET.get('region_search', get_region().id)
    try:
        region = Region.objects.get(pk=region_id)
    except Region.DoesNotExist:
        region = Region.objects.get(pk=get_region().id)

    # Init the category search param
    menu_search = request.GET.get('menu_search', 0)
    try:
        menu = Menu.objects.get(pk=menu_search)
        if menu.region != region:
            # Change region and find similar category
            request.session['region_id'] = region.id
            menu = Menu.objects.root_nodes().filter(
                region=region).get(name=menu.name)
    except Menu.DoesNotExist:
        menu = Menu.objects.root_nodes().filter(region=region)[0]

    from datetime import datetime

    # Init date_start and date_end search params
    date_start = request.GET.get('date_start', '')
    date_end = request.GET.get('date_end', '')
    try:
        if date_start:
            date_start = datetime.strptime(date_start, '%d.%m.%Y')
    except ValueError:
        date_start = ''
    try:
        if date_end:
            date_end = datetime.strptime(date_end, '%d.%m.%Y')
    except ValueError:
        date_end = ''


    # Search in index
    hits = None
    if q is not None:
        # Open index dir
        ix = whoosh_index.open_dir(settings.PAGE_SEARCH_INDEX)

        # Make parser
        parser = QueryParser(search_in, schema=ix.schema)

        # Configure filter
        filter = Term('region', region.id)

        # Make query string
        qstr = q.replace('+', ' AND ').replace(' -', ' NOT ').replace(' | ', ' OR ')

        # Parse query string
        query = parser.parse(qstr)

        # And... search in index!
        hits = ix.searcher().search(query, filter=filter, limit=None)


    pages = Page.objects.filter(region=region).filter(visible=True)

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


    from django.utils.html import strip_tags, strip_entities
    from cms.views.utils import paginate

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
        pages = paginate(request, pages, 20)

        # Highlight results
        for hit in hits:
            for page in pages:
                if page.id == hit['id']:
                    if search_in == 'name':
                        page.name = hit.highlights('name',
                            text=strip_entities(strip_tags(page.name)))
                    if search_in == 'content':
                        page.content = hit.highlights('content',
                            text=strip_entities(strip_tags(page.content)))

        if 'ix' in locals():
            ix.close()

    if date_start:
        date_start = '%s.%s.%s' % (date_start.day, date_start.month, date_start.year)
    if date_end:
        date_end = '%s.%s.%s' % (date_end.day, date_end.month, date_end.year)

    return render(request, 'search.html', {
        'q': q,
        'menu_search': menu.id,
        'region_search': region.id,
        'search_in': search_in,
        'date_start': date_start,
        'date_end': date_end,
        'pages': pages,
        'hits_count': hits_count
    })

def polls(request):
    polls = Poll.objects.filter(is_active=True)
    return render(request, 'polls.html', {
        'polls': polls,
    })

def poll(request, pk):
    p = get_object_or_404(Poll, pk=pk)
    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            form.save_vote()
            return redirect('poll_results', pk=p.id)
    else:
        form = PollForm(initial={'poll': p.id})
    return render(request, 'poll.html', {
        'poll': p,
        'form': form,
    })

def poll_results(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    return render(request, 'poll_results.html', {
        'poll': poll,
    })

def change_region(request, pk):
    region = Region.objects.get(pk=pk)

    if 'DomainFinder' in settings.REGION_FINDER:
        domain = request.get_host().split(':')

        abbr = region.abbr if region.abbr != settings.DEFAULT_REGION else ''

        domain_parts = domain[0].split('.')
        domain_parts.reverse()
        domain_parts = domain_parts[:2] + [abbr] if abbr else domain_parts[:2]
        domain_parts.reverse()
        domain[0] = '.'.join(domain_parts)

        # Given port
        if len(domain) == 2:
            url = 'http://%s:%s' % (domain[0], domain[1])
        else:
            url = 'http://%s' % (domain[0])

        return HttpResponseRedirect(url)
    else:
        set_region(region)
        return redirect('index')


def letters(request):
    return render(request, 'letters.html', {})


def letters_rules(request):
    return render(request, 'letters_rules.html', {})


def letters_form(request):
    success = False
    if request.method == 'POST':
        form = LetterForm(request.POST, request.FILES)
        if form.is_valid():
            letter = form.save()
            success = True
            if letter.email:
                send_mail(
                    subject=u'%s%s' % (settings.EMAIL_SUBJECT_PREFIX,
                                       u'Обращения граждан'),
                    message=render_to_string('letter_notify_success.txt',
                                             {'letter': letter}),
                    recipient_list=[letter.email],
                    from_email=settings.DEFAULT_FROM_EMAIL,
                )
    else:
        form = LetterForm(initial={
            'region': get_region().id,
            'reply_by_email': True
        })
    return render(request, 'letters_form.html', {
        'form': form,
        'success': success
    })
