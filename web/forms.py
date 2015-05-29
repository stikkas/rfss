# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from captcha.fields import CaptchaTextInput, CaptchaField

from cms.models import GENDERS
from cms.polls.models import Poll, Choice
from cms.components.pages.models import Page, Comment
from cms.letters.models import Letter, Rubric, Attach, attach_validator
from cms.forms import InlineErrorList


class RegistrationForm(forms.Form):
    username = forms.CharField(label=u'Логин', max_length=30)
    password1 = forms.CharField(label=u'Пароль',
        min_length=6, max_length=128, widget=forms.PasswordInput)
    password2 = forms.CharField(label=u'Повторите пароль',
        min_length=6, max_length=128, widget=forms.PasswordInput)
    first_name = forms.CharField(label=u'Имя', max_length=30)
    last_name = forms.CharField(label=u'Фамилия', max_length=30)
    birthday = forms.DateField(label=u'Дата рождения')
    gender = forms.ChoiceField(label=u'Пол', choices=GENDERS)
    department = forms.CharField(label=u'Судебный орган', max_length=255)
    position = forms.CharField(label=u'Должность', max_length=255)
    email = forms.EmailField(label=u'E-Mail')
    phone = forms.CharField(label=u'Телефон', max_length=50)

    def clean(self):
        fields = self.cleaned_data
        if fields.get('password1', 'p1') != fields.get('password2', 'p2'):
            raise forms.ValidationError(u'Пароли не совпадают')
        return fields

    def register(self):
        fields = self.cleaned_data

        user = User.objects.create_user(
            username=fields['username'],
            email=fields['email'],
            password=fields['password1'])
        user.first_name = fields['first_name']
        user.last_name = fields['last_name']
        user.is_active = False
        user.save()

        user.profile.birthday = fields['birthday']
        user.profile.gender = fields['gender']
        user.profile.department = fields['department']
        user.profile.position = fields['position']
        user.profile.phone = fields['phone']
        user.profile.save()


class PollForm(forms.Form):
    poll = forms.IntegerField(widget=forms.HiddenInput)
    choices = forms.TypedChoiceField(widget=forms.RadioSelect, coerce=int)

    def __init__(self, *args, **kwargs):
        if kwargs.get('initial'):
            data = kwargs.get('initial')
        else:
            data = args[0]
        super(PollForm, self).__init__(*args, **kwargs)
        poll = Poll.objects.get(pk=data['poll'])
        self.fields['choices'].choices = [(c.id, c.title)
                                          for c in poll.choices.all()]

    def save_vote(self):
        choice_pk = self.cleaned_data['choices']
        choice = Choice.objects.get(pk=choice_pk)
        if choice.poll_id == self.cleaned_data['poll']:
            choice.votes += 1
            choice.save()


class CommentForm(forms.Form):
    user = forms.IntegerField(widget=forms.HiddenInput)
    page = forms.IntegerField(widget=forms.HiddenInput)

    message = forms.CharField(widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        if not kwargs.get('error_class'):
            kwargs['error_class'] = InlineErrorList
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean(self):
        user_pk = self.cleaned_data['user']
        page_pk = self.cleaned_data['page']

        try:
            self.user_object = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            raise forms.ValidationError(u'Пользователь не найден.')

        try:
            self.page_object = Page.objects.get(pk=page_pk)
        except Page.DoesNotExist:
            raise forms.ValidationError(u'Публикация не найдена.')

        return self.cleaned_data

    def add_comment(self):
        Comment.objects.create(page=self.page_object, user=self.user_object,
            message=self.cleaned_data['message'])


class LetterForm(forms.ModelForm):
    first_name = forms.CharField(label=u'Имя', max_length=15)
    patronymic = forms.CharField(label=u'Отчество', max_length=15,
                                 required=False)
    house = forms.CharField(label=u'№ дома', max_length=10)
    flat = forms.CharField(label=u'№ квартиры / офиса', max_length=10,
                           required=False)
    rubric = forms.ChoiceField(label=u'Рубрика', required=False)
    message = forms.CharField(label=u'Текст обращения', max_length=2000,
                              widget=forms.Textarea)
    attach = forms.FileField(label=u'Приложение', validators=[attach_validator],
                             required=False)
    captcha = CaptchaField(widget=CaptchaTextInput(
        output_format=u"""
        <div class="fleft captcha-fields">%(text_field)s%(hidden_field)s</div>
        <div class="fleft captcha-img">%(image)s</div>
        <div class="fleft captcha-refresh"><button id="js-captcha-refresh">Обновить</button></div>
        """
    ))

    class Meta:
        model = Letter
        widgets = {
            'region': forms.HiddenInput,
        }
        exclude = ('filing_datetime', 'reply_by_email',)

    def __init__(self, *args, **kwargs):
        super(LetterForm, self).__init__(*args, **kwargs)
        self.fields['rubric'].choices = [(r.name, r.name)
                                         for r in Rubric.objects.all()]
        self.fields['rubric'].choices.insert(0, (None, '--------'))

    def save(self, commit=True):
        letter = super(LetterForm, self).save(commit)
        if self.cleaned_data['attach']:
            attach = self.cleaned_data['attach']
            Attach.objects.create(letter=letter,
                                  name=attach.name,
                                  content_type=attach.content_type,
                                  file=attach)
        return letter
