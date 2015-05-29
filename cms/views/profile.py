from django.utils.translation import get_language
from django.shortcuts import get_object_or_404

from cms.models import Profile
from cms.forms import ProfileForm
from cms.url_builders import redirect
from cms.views.utils import render
from cms.views.decorators import cms_protector


@cms_protector
def profile(request, user_pk):
    profile = get_object_or_404(Profile, user_id=user_pk)
    return render(request, 'cms/profile.html', {
        'profile': profile
    })

@cms_protector
def edit_profile(request, user_pk):
    profile = get_object_or_404(Profile, user_id=user_pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            field =form.cleaned_data

            profile.user.first_name = field['first_name']
            profile.user.last_name = field['last_name']
            profile.user.email = field['email']
            profile.user.save()

            profile.gender = field['gender']
            profile.birthday = field['birthday']
            profile.department = field['department']
            profile.position = field['position']
            profile.phone = field['phone']
            profile.save()

            return redirect('cms:profile', user_pk=user_pk)
    else:
        initial = {}
        initial.update(profile.user.__dict__)
        initial.update(profile.__dict__)
        form = ProfileForm(initial=initial)
    return render(request, 'cms/edit_profile.html', {
        'profile': profile,
        'form': form,
        'LANG': get_language()
    })
