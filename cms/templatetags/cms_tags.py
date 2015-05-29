from datetime import datetime
from django import template
from django.template import Node
from django.template import defaulttags
from django.utils.text import normalize_newlines
from django.utils.html import escape
from django.utils.safestring import mark_safe, SafeData

from cms.url_builders import build_url


register = template.Library()


def url_builder_tag(parser, token, django_url_tag):
    url_node = django_url_tag(parser, token)
    return URLBuilderNode(url_node)

class URLBuilderNode(Node):
    def __init__(self, url_node):
        self.url_node = url_node

    def render(self, context):
        url = self.url_node.render(context)
        return build_url(url)


@register.tag('link')
def url_builder_tag_wrapper(parser, token):
    return url_builder_tag(parser, token, django_url_tag=defaulttags.url)


@register.filter
def full_name(user):
    first_name = user.first_name
    last_name = user.last_name

    if first_name and last_name:
        return '%s %s' % (last_name, first_name)
    elif first_name and not last_name:
        return first_name
    elif last_name and not first_name:
        return last_name

    return user.username

@register.filter
def short_name(user):
    first_name = user.first_name
    last_name = user.last_name

    if first_name and last_name:
        first_name = ' '.join([w[0]+'.' for w in first_name.split(' ')
                               if w.isalpha()])
        return '%s %s' % (last_name, first_name)
    elif first_name and not last_name:
        return first_name
    elif last_name and not first_name:
        return last_name

    return user.username

@register.filter
def to_datetime(value, format):
    return datetime.strptime(value, format)

@register.filter
def blockquote(value, autoescape=None):
    """Replace [blockquote][/blockquote] on <blockquote></blockquote>
    """
    autoescape = autoescape and not isinstance(value, SafeData)
    value = normalize_newlines(value)
    if autoescape:
        value = escape(value)
    body = value.replace('[blockquote]', '<blockquote>')
    body = body.replace('[/blockquote]', '</blockquote>')
    return mark_safe(body)


@register.filter
def call_method(obj, params):
    """Filter can call method with args and kwargs, but all passed params
    must be primitive types such as string, integer and boolean.
    Parameter a string can be represented as double quotes, single quotes and
    without any quotes.

    Example usage:

        {{ obj|call_method:"get_tree:include_self=True" }}

        {{ obj|call_method:"get_tree:as_str='string'" }}
        {{ obj|call_method:'get_tree:as_str="string"' }}
        {{ obj|call_method:"get_tree:as_str=string" }}

        {{ obj|call_method:"get_tree:max_depth=5" }}

    """
    args = []
    kwargs = {}

    func_name, params = params.split(':')
    params = params.split(',')
    for param in params:
        if param.count('='):
            key, value = param.split('=')
            kwargs[key] = _to_python(value)
        else:
            args.append(_to_python(param))

    return getattr(obj, func_name)(*args, **kwargs)

def _to_python(param):
    converters = (
        # Boolean
        {'is': lambda param: param == 'True' or param == 'False',
         'convert': lambda param: param == 'True'},
        # Integer
        {'is': lambda param: param.isdigit(),
         'convert': lambda param: int(param)},
        # String surrounded '
        {'is': lambda param: param.startswith("'") and param.endswith("'"),
         'convert': lambda param: param[1:-1]},
        # String surrounded "
        {'is': lambda param: param.startswith('"') and param.endswith('"'),
         'convert': lambda param: param[1:-1]},
        )

    for converter in converters:
        if converter['is'](param):
            return converter['convert'](param)
    return param
