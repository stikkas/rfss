import mimetypes
from django.http import HttpResponse
from django.utils.translation import get_language
from django.shortcuts import get_object_or_404
from django.utils.http import urlquote

from cms.menu.models import Menu
from cms.components.pages.models import Page, Attachment
from cms.regions import get_region
from cms.forms import AttachmentForm, PageForm
from cms.url_builders import redirect
from cms.utils import is_ascii
from cms.views.utils import render
from cms.views.decorators import cms_protector


@cms_protector
def page_add(request, menu_pk):
    menu = get_object_or_404(Menu, pk=menu_pk)
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save()

            # Moderation not required for moderators or superusers
            if request.user.profile.is_moderator or request.user.is_superuser:
                page.publish()
                page.vised()

            return redirect('cms:menu', pk=menu.id)
    else:
        form = PageForm(initial={
            'menu': menu, 'region': get_region(), 'last_edit_by': request.user
        })
    return render(request, Page.tmpl_add(), {
        'menu': menu,
        'form': form,
        # TODO: LANG in template context processor
        'LANG': get_language(),
    })

@cms_protector
def page_edit(request, pk):
    page = get_object_or_404(Page, pk=pk)

    if request.POST.get('save'):
        page_form = PageForm(request.POST, instance=page)
        if page_form.is_valid():
            page = page_form.save()

            # Moderation not required for moderators or superusers
            if request.user.profile.is_moderator or request.user.is_superuser:
                page.vised()

            return redirect('cms:menu', pk=page.menu.id)
    else:
        page_form = PageForm(initial={'last_edit_by': request.user},
            instance=page)

    if request.POST.get('upload'):
        attach_form = AttachmentForm(request.POST, request.FILES)
        if attach_form.is_valid():
            attach_form.save()
    else:
        attach_form = AttachmentForm(initial={'page': page})

    return render(request, Page.tmpl_edit(), {
        'page': page,
        'page_form': page_form,
        'attach_form': attach_form,
        # TODO: LANG in template context processor
        'LANG': get_language(),
    })

@cms_protector
def page_delete(request, pk):
    page = get_object_or_404(Page, pk=pk)
    if request.method == 'POST':
        page.delete()
    return redirect('cms:menu', pk=page.menu.id)

def get_attach(request, pk):
    doc = get_object_or_404(Attachment, pk=pk)

    filename = doc.name if is_ascii(doc.name) else doc.name.encode('utf8')
    filename = urlquote(filename, ',')
    mimetype, encoding = mimetypes.guess_type(doc.name)

    response = HttpResponse(content=doc.file.read())
    if encoding is not None:
        response['Content-Encoding'] = encoding
    response['Content-Type'] = 'application/%s' % mimetype
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    response['Content-Length'] = doc.file.size

    return response

@cms_protector
def attach_delete(request, pk):
    attach = get_object_or_404(Attachment, pk=pk)
    if request.method == 'POST':
        attach.delete()
    return redirect('cms:page_edit', pk=attach.page.id)
