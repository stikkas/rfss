from django.http import Http404
from django.template import TemplateDoesNotExist

from cms.views.utils import render
from cms.views.decorators import cms_protector


@cms_protector
def help(request, tmpl_name):
    try:
        return render(request, 'cms/help/%s.html' % tmpl_name, {
            'tmpl': tmpl_name,
        })
    except TemplateDoesNotExist:
        raise Http404
