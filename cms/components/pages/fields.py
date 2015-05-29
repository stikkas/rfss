from django.db import models
from south.modelsinspector import add_introspection_rules

add_introspection_rules([], ["^cms\.components\.pages\.fields\.RatingField"])


class RatingField(models.CharField):

    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        max_length = 255
        default = '1:0,2:0,3:0,4:0,5:0'
        kwargs.update({'max_length': max_length, 'default': default})
        super(RatingField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        value = super(RatingField, self).to_python(value)
        return dict([map(int, rate.split(':')) for rate in value.split(',')])

    def get_prep_value(self, value):
        if isinstance(value, basestring):
            return value
        return ','.join(['%d:%d' % (k, v) for k, v in value.viewitems()])
