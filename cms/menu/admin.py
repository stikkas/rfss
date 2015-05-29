from django.contrib import admin

from cms.menu.models import Menu


class MenuAdmin(admin.ModelAdmin):
    pass


admin.site.register(Menu, MenuAdmin)
