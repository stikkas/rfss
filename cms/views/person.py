from django.utils.translation import get_language
from django.shortcuts import get_object_or_404

from cms.menu.models import Menu
from cms.components.person.models import Person
from cms.regions import get_region
from cms.forms import PersonForm
from cms.url_builders import redirect
from cms.views.utils import render
from cms.views.decorators import cms_protector


@cms_protector
def person_add(request, menu_pk):
    menu = get_object_or_404(Menu, pk=menu_pk)
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cms:menu', pk=menu.id)
    else:
        form = PersonForm(initial={'menu': menu, 'region': get_region()})
    return render(request, Person.tmpl_add(), {
        'menu': menu,
        'form': form,
        # TODO: LANG in template context processor
        'LANG': get_language(),
    })

@cms_protector
def person_edit(request, pk):
    person = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            form.save()
            return redirect('cms:menu', pk=person.menu.id)
    else:
        form = PersonForm(instance=person)
    return render(request, Person.tmpl_edit(), {
        'person': person,
        'form': form,
        # TODO: LANG in template context processor
        'LANG': get_language(),
    })

@cms_protector
def person_delete(request, pk):
    person = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
        person.delete()
    return redirect('cms:menu', pk=person.menu.id)
