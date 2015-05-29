from django.shortcuts import get_object_or_404

from cms.messenger.models import SentboxMessage, InboxMessage
from cms.forms import MessageForm
from cms.views.decorators import cms_protector
from cms.views.utils import paginate, render
from cms.url_builders import redirect


@cms_protector
def write_message(request, reply_mesg_pk=None):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.send_message(notify_on_email=True)
            return redirect('cms:sentbox')
    else:
        initial = {'sender': request.user.id}

        if reply_mesg_pk:
            inbox_message = get_object_or_404(InboxMessage, pk=reply_mesg_pk)
            initial['subject'] = inbox_message.reply_subject
            initial['body'] =  inbox_message.reply_body
            initial['recipients'] = [inbox_message.sender.id]

        form = MessageForm(initial=initial)
    return render(request, 'cms/messenger/write_message.html', {
        'form': form,
    })

@cms_protector
def sentbox(request):
    sentbox = SentboxMessage.objects.filter(
        owner=request.user
    ).select_related('pending')
    return render(request, 'cms/messenger/sentbox.html', {
        'sentbox': paginate(request, sentbox),
    })

@cms_protector
def sentbox_message(request, pk):
    message = get_object_or_404(SentboxMessage, pk=pk)
    return render(request, 'cms/messenger/sentbox_message.html', {
        'message': message,
    })

@cms_protector
def delete_sentbox_message(request, pk):
    message = get_object_or_404(SentboxMessage, pk=pk)
    if request.method == 'POST':
        message.delete()
    return redirect('cms:sentbox')

@cms_protector
def inbox(request):
    inbox = InboxMessage.objects.filter(
        owner=request.user
    ).select_related('sender')
    return render(request, 'cms/messenger/inbox.html', {
        'inbox': paginate(request, inbox),
    })

@cms_protector
def inbox_message(request, pk):
    message = get_object_or_404(InboxMessage, pk=pk)
    if message.is_new:
        message.is_new = False
        message.save()
    return render(request, 'cms/messenger/inbox_message.html', {
        'message': message,
    })

@cms_protector
def delete_inbox_message(request, pk):
    message = get_object_or_404(InboxMessage, pk=pk)
    if request.method == 'POST':
        message.delete()
    return redirect('cms:inbox')
