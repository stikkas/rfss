from django.contrib import admin

from cms.polls.models import Poll, Choice


class ChoiceInline(admin.StackedInline):
    fieldsets = [
        (None, {'fields': ['title']}),
        ('Votes', {'fields': ['votes'], 'classes': ['collapse']})
    ]
    model = Choice
    extra = 0

class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question', 'is_active']}),
    ]
    inlines = [ChoiceInline]


admin.site.register(Poll, PollAdmin)
