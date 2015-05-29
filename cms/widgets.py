from django.forms.widgets import FileInput, CheckboxInput
from django.utils.html import escape, conditional_escape
from django.utils.translation import ugettext_lazy
from django.utils.safestring import mark_safe


FILE_INPUT_CONTRADICTION = object()

class PersonPhotoImageField(FileInput):
    initial_text = ugettext_lazy('Currently')
    input_text = ugettext_lazy('Change')
    clear_checkbox_label = ugettext_lazy('Clear')

    template_with_initial = u"""
    <table class="person-form_photo">
        <tr>
            <td>%(initial)s</td>
            <td class="person-form_photo-clear">%(clear_template)s</td>
        </tr>
    </table>
    %(input)s
    """

    template_with_clear = u"""
    <label class="checkbox input muted">
        %(clear)s %(clear_checkbox_label)s
    </label>
    """

    def clear_checkbox_name(self, name):
        """
        Given the name of the file input, return the name of the clear checkbox
        input.
        """
        return name + '-clear'

    def clear_checkbox_id(self, name):
        """
        Given the name of the clear checkbox input, return the HTML id for it.
        """
        return name + '_id'

    def render(self, name, value, attrs=None):
        subs= {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
            }
        template = u'%(input)s'
        subs['input'] = super(PersonPhotoImageField, self).render(
            name, value, attrs)

        if value and hasattr(value, "url"):
            template = self.template_with_initial
            subs['initial'] = u'<img src="%s">' % escape(value.url)
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                subs['clear_checkbox_name'] = conditional_escape(checkbox_name)
                subs['clear_checkbox_id'] = conditional_escape(checkbox_id)
                subs['clear'] = CheckboxInput().render(
                    checkbox_name, False, attrs={'id': checkbox_id})
                subs['clear_template'] = self.template_with_clear % subs

        return mark_safe(template % subs)

    def value_from_datadict(self, data, files, name):
        upload = super(PersonPhotoImageField, self).value_from_datadict(
            data, files, name)
        if not self.is_required and CheckboxInput().value_from_datadict(
            data, files, self.clear_checkbox_name(name)):
            if upload:
                # If the user contradicts themselves (uploads a new file AND
                # checks the "clear" checkbox), we return a unique marker
                # object that FileField will turn into a ValidationError.
                return FILE_INPUT_CONTRADICTION
                # False signals to clear any existing value,
                # as opposed to just None
            return False
        return upload