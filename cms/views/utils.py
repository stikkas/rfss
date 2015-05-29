from django.shortcuts import render as _render
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from cms.conf import settings
from cms.regions import get_region


def render(request, template, context):
    try:
        user = User.objects.select_related('profile').get(pk=request.user.id)
        context.setdefault('user', user)
    except User.DoesNotExist:
        pass
    context.setdefault('region', get_region())
    return _render(request, template, context)

def paginate(request, elements, elements_on_page=settings.ELEMENTS_ON_PAGE):
    paginator = Paginator(elements, elements_on_page)
    page = request.GET.get('page')
    try:
        paginated = paginator.page(page)
    except PageNotAnInteger:
        paginated = paginator.page(1)
    except EmptyPage:
        paginated = paginator.page(paginator.num_pages)
    return paginated
