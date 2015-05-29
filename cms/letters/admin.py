from django.contrib import admin

from cms.letters.models import Rubric, PostBox


class RubricAdmin(admin.ModelAdmin):
    pass


class PostBoxAdmin(admin.ModelAdmin):
    pass


admin.site.register(Rubric, RubricAdmin)
admin.site.register(PostBox, PostBoxAdmin)
