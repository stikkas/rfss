from django.contrib import admin

from cms.metrika.models import Counter

class MetrikaAdmin(admin.ModelAdmin):
    pass


admin.site.register(Counter, MetrikaAdmin)
