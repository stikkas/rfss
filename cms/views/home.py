from cms.url_builders import redirect
from cms.views.decorators import cms_protector


@cms_protector
def home(request):
    return redirect('cms:menu')
