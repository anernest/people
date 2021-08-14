'''
    People Apphook
'''
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _
from .menu import PeopleMenu

class PeopleApphook(CMSApp):
    app_name = "People"
    name = _("People Apphook")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["people.urls"]
        
    def get_menus(self, page=None, language=None, **kwargs):
        return [PeopleMenu]


apphook_pool.register(PeopleApphook)