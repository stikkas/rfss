from django.contrib.auth.models import User
from django.db.models.query import Q
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404

from cms.components.pages.models import Page, Comment
from cms.url_builders import redirect
from cms.forms import MessageForm
from cms.views.utils import paginate, render
from cms.views.decorators import cms_protector


@cms_protector
def moderate_new_users(request):
    new_users = User.objects.filter(
        is_staff=False).filter(is_superuser=False
    ).filter(
        is_active=False
    ).prefetch_related(
        'profile'
    ).filter(profile__is_manager=False).filter(profile__is_moderator=False)
    return render(request, 'cms/moderate_new_users.html', {
        'new_users': new_users,
    })

def moderate_new_user_confirm(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.is_active = True
        user.save()
    return redirect('cms:moderate_new_users')

def moderate_new_user_reject(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
    return redirect('cms:moderate_new_users')

@cms_protector
def moderate_pages(request):
    pages = Page.objects.filter(
        Q(visible=False) | Q(is_vised=False)
    ).select_related(
        'region'
    ).prefetch_related(
        'last_edit_by'
    ).prefetch_related('menu').order_by('is_vised')
    return render(request, 'cms/moderate.html', {
        'pages': paginate(request, pages),
    })

@cms_protector
def moderate_page(request, page_pk):
    page = get_object_or_404(Page, pk=page_pk)
    page.vised()
    return render(request, 'cms/moderate_page.html', {
        'page': page,
    })

@cms_protector
def moderate_page_publish(request, page_pk):
    page = get_object_or_404(Page, pk=page_pk)
    page.publish()
    return redirect('cms:moderate_pages')

@cms_protector
def moderate_page_unpublish(request, page_pk):
    page = get_object_or_404(Page, pk=page_pk)
    page.unpublish()
    return redirect('cms:moderate_pages')

@cms_protector
def moderate_write_comment(request, page_pk):
    page = get_object_or_404(Page, pk=page_pk)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.send_message(notify_on_email=True)
            return redirect('cms:moderate_pages')
    else:
        initial = {
            'sender': request.user.id,
            'recipients': [page.last_edit_by_id],
            'subject': '%s: %s' % (_('Comment to'), page.name)
        }
        form = MessageForm(initial=initial)
    return render(request, 'cms/moderate_write_comment.html', {
        'page': page,
        'form': form,
    })

@cms_protector
def moderate_comments(request):
    comments = Comment.objects.filter(
        visible=False
    ).select_related('page', 'user').prefetch_related('page__region')
    return render(request, 'cms/moderate_comments.html', {
        'comments': paginate(request, comments),
    })

@cms_protector
def moderate_comment_publish(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        comment.publish()
    return redirect('cms:moderate_comments')

@cms_protector
def moderate_comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        comment.delete()
    return redirect('cms:moderate_comments')
