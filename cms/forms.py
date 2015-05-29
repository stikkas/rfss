from copy import copy
from django import forms
from django.forms.util import ErrorList
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils import dateformat
from django.utils.translation import ugettext_lazy as _
from mptt.forms import TreeNodeChoiceField

from cms.conf import settings
from cms.messenger import send_message
from cms.menu.models import Menu
from cms.models import Profile, GENDERS
from cms.components.pages.models import Page, Attachment
from cms.components.person.models import Person
from cms.templatetags.cms_tags import full_name
from cms.widgets import PersonPhotoImageField


class InlineErrorList(ErrorList):
    def __unicode__(self):
        return self.as_inline()

    def as_inline(self):
        if not self: return  u''
        return ' '.join([u'%s' % e for e in self])

class Form(forms.Form):
    def __init__(self, *args, **kwargs):
        if not kwargs.get('error_class'):
            kwargs['error_class'] = InlineErrorList
        super(Form, self).__init__(*args, **kwargs)

class ModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if not kwargs.get('error_class'):
            kwargs['error_class'] = InlineErrorList
        super(ModelForm, self).__init__(*args, **kwargs)


class AuthenticationForm(Form):
    """Code based on django.contrib.auth.forms.AuthenticationForm"""
    username = forms.CharField(label=_("Username"),
        max_length=30, widget=forms.TextInput(attrs={
            'placeholder': _('Username')
    }))
    password = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Password')
    }))

    error_messages = {
        'invalid_login': _("Please enter a correct username and password. "
                           "Note that both fields are case-sensitive."),
        'no_cookies': _("Your Web browser doesn't appear to have cookies "
                        "enabled. Cookies are required for logging in."),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'])
            elif not self.user_cache.is_active:
                raise forms.ValidationError(self.error_messages['inactive'])
        self.check_for_test_cookie()
        return self.cleaned_data

    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(self.error_messages['no_cookies'])

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class PageForm(ModelForm):
    name = forms.CharField(label=_('Title'), max_length=255)
    menu = TreeNodeChoiceField(label=_('Category'), queryset=None)
    annotation = forms.CharField(label=_('Annotation'), required=False,
        max_length=1000, widget=forms.Textarea)

    class Meta:
        model = Page
        exclude = ('vised', 'visible', 'version',)
        widgets = {'region': forms.HiddenInput,
                   'last_edit_by': forms.HiddenInput}

    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)
        self.fields['menu'].queryset = Menu.objects.for_region().filter(
            component=ContentType.objects.get_for_model(Page)
        )


class AttachmentForm(ModelForm):
    file = forms.FileField(help_text=_(
        ' Max size: %(size)d MiB. Allowed types: %(types)s.') % {
            'size': settings.ATTACHMENT_SIZE / 1024 / 1024,
            'types': ', '.join(settings.ATTACHMENT_TYPES)
        }
    )
    class Meta:
        model = Attachment
        exclude = ('name',)
        widgets = {'page': forms.HiddenInput}


class PersonForm(ModelForm):
    menu = TreeNodeChoiceField(label=_('Category'), queryset=None)

    class Meta:
        model = Person
        widgets = {'region': forms.HiddenInput, 'photo': PersonPhotoImageField}

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.fields['menu'].queryset = Menu.objects.for_region().filter(
            component=ContentType.objects.get_for_model(Person)
        )


class ProfileForm(Form):
    first_name = forms.CharField(label=_('First name'), max_length=30)
    last_name = forms.CharField(label=_('Last name'), max_length=30)
    gender = forms.ChoiceField(label=_('Gender'), choices=GENDERS)
    birthday = forms.DateField(label=_('Birthday'))
    department = forms.CharField(label=_('Department'), required=False,
        max_length=255)
    position = forms.CharField(label=_('Position'), required=False,
        max_length=255)
    phone = forms.CharField(label=_('Phone'), required=False,
        max_length=50)
    email = forms.EmailField(label=_('E-Mail'), required=False)


class MessageForm(Form):
    sender = forms.IntegerField(widget=forms.HiddenInput)
    subject = forms.CharField(label=_('Subject'), max_length=255)
    recipients = forms.TypedMultipleChoiceField(label=_('Recipients'),
        coerce=int)
    body = forms.CharField(label=_('Body'), widget=forms.Textarea)

    error_messages = {
        'not_found_sender': _('Not found sender.'),
        'not_found_recipients': _('Not all recipients are found')
    }

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['recipients'].choices = (
            (_('Admins'),
             [(p.user.id, full_name(p.user),) for p in Profile.objects.filter(
                 user__is_superuser=True).select_related('user')]
            ),
            (_('Moderators'),
             [(p.user.id, full_name(p.user),) for p in Profile.objects.filter(
                 is_moderator=True
             ).filter(
                 user__is_superuser=False).select_related('user')]
            ),
            (_('Managers'),
             [(p.user.id, full_name(p.user),) for p in Profile.objects.filter(
                 is_manager=True
             ).filter(
                 user__is_superuser=False
             ).filter(is_moderator=False).select_related('user')]
            ),
        )

    def clean(self):
        field = self.cleaned_data
        self.message = {
            'subject': field.get('subject'),
            'body': field.get('body')
        }

        try:
            self.message['sender'] = User.objects.get(pk=field.get('sender'))
        except User.DoesNotExist:
            raise forms.ValidationError(self.error_messages['not_found_sender'])

        recipients = field.get('recipients')
        if len(recipients) != User.objects.filter(pk__in=recipients).count():
            raise forms.ValidationError(
                self.error_messages['not_found_recipients'])
        self.message['recipients'] = recipients

        return self.cleaned_data

    def send_message(self, notify_on_email=not settings.DEBUG):
        send_message(notify_on_email=notify_on_email, **self.message)


SEARCH_IN = (
    ('name', _('In Title'),),
    ('content', _('In Content'),),
)

class SearchForm(Form):
    q = forms.CharField(label=_('Query'), required=False,
        max_length=50, widget=forms.TextInput(
            attrs={'placeholder': _('Query')
        }))
    menu = TreeNodeChoiceField(label=_('Category'), required=False,
        queryset=None
    )
    search_in = forms.ChoiceField(choices=SEARCH_IN, required=False)
    date_start = forms.DateField(required=False, widget=forms.DateInput(
        format='d.m.Y', attrs={'placeholder': _('Date From'),
    }))
    date_end = forms.DateField(required=False, widget=forms.DateInput(
        format='d.m.Y', attrs={'placeholder': _('Date To'),
    }))

    def __init__(self, *args, **kwargs):
        data = copy(args[0] if not kwargs.get('data') else kwargs['data'])
        if data.get('menu'):
            try:
                menu = Menu.objects.get(pk=data['menu'])
                if menu.component.model_class() != Page:
                    data['menu'] = None
            except Menu.DoesNotExist:
                data.pop('menu')
        if data.get('search_in'):
            if data['search_in'] not in [choice[0] for choice in SEARCH_IN]:
                data['search_in'] = SEARCH_IN[0][0]

        super(SearchForm, self).__init__(data, *args, **kwargs)
        self.fields['menu'].queryset = Menu.objects.for_region().filter(
            component=ContentType.objects.get_for_model(Page)
        )

    def clean_menu(self):
        menu = self.cleaned_data['menu']
        if not menu:
            menu = Menu.objects.root_nodes().for_region()[0]
        return menu

    def clean_search_in(self):
        if not self.cleaned_data['search_in']:
            self.cleaned_data['search_in'] = SEARCH_IN[0][0]
        return self.cleaned_data['search_in']


    def url_GET_params(self):
        date_start = dateformat.format(
            self.cleaned_data['date_start'], 'd.m.Y'
        ) if self.cleaned_data['date_start'] else ''

        date_end = dateformat.format(
            self.cleaned_data['date_end'], 'd.m.Y'
        ) if self.cleaned_data['date_end'] else ''

        params = [
            '%s=%s' % ('q', self.cleaned_data['q']),
            '%s=%s' % ('menu', self.cleaned_data['menu'].id),
            '%s=%s' % ('search_in', self.cleaned_data['search_in']),
            '%s=%s' % ('date_start', date_start),
            '%s=%s' % ('date_end', date_end),
        ]
        return '&' + '&'.join(params)
