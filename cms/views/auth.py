import urlparse
from django.contrib.auth import login as auth_login, logout as auth_logout

from cms.conf import settings
from cms.forms import AuthenticationForm
from cms.url_builders import redirect
from cms.views.utils import render
from cms.views.decorators import login_required


def login(request):
    """Code based on django.contrib.auth.views.login"""
    redirect_to = request.REQUEST.get('next', '')

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            netloc = urlparse.urlparse(redirect_to)[1]

            # Use default setting if redirect_to is empty
            if not redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Heavier security check -- don't allow redirection to a different
            # host.
            elif netloc and netloc != request.get_host():
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Okay, security checks complete. Log the user in.
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return redirect(redirect_to)
    else:
        form = AuthenticationForm(request)

    request.session.set_test_cookie()

    return render(request, 'cms/login.html', {
        'form': form,
        'next': redirect_to,
    })

@login_required
def logout(request):
    auth_logout(request)
    return redirect('cms:login')
