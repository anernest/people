'''
    People Menu
'''
from menus.base import Menu, NavigationNode
from menus.menu_pool import menu_pool
from django.utils.translation import ugettext_lazy as _

class PeopleMenu(Menu):

    name = _("People Menu")

    def get_nodes(self, request):
        nodes = []
        n = NavigationNode(_('People'), "/people/", 1, attr={'visible_for_anonymous': False})
        n2 = NavigationNode(_('Education'), "/people/education", 2, attr={'visible_for_anonymous': False})
        nodes.append(n)
        nodes.append(n2)
        return nodes

menu_pool.register_menu(PeopleMenu)