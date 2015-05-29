from collections import namedtuple
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from cms.menu.models import Menu
from cms.components import Comp
from cms.regions import get_region
from cms.views.utils import render
from cms.views.decorators import cms_protector


def menu_tree(menu):
    MenuLevel = namedtuple('MenuLevel', 'name, children')

    tree = [MenuLevel(_('Menus'), Menu.objects.root_nodes().for_region())]

    ancestors = menu.get_ancestors(include_self=True)
    for ancestor in ancestors[1:]:
        tree.append(MenuLevel(ancestor.parent.name,
                              ancestor.get_siblings(include_self=True)))

    if not menu.is_leaf_node():
        tree.append(MenuLevel(menu.name, menu.get_children(),))

    return tree


@cms_protector
def menu(request, pk=None):
    if not pk:
        active_menu = Menu.objects.root_nodes().filter(region=get_region())[0]
    else:
        active_menu = get_object_or_404(Menu, pk=pk)

    return render(request, 'cms/menu.html', {
        'region': get_region(),
        'active_menu': active_menu,
        'menu_tree': menu_tree(active_menu),
        'comp': Comp(request, active_menu),
    })
