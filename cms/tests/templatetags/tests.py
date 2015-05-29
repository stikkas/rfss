from django import template
from django.test import TestCase


class TagTestCase(TestCase):
    def render_template(self, text, context=None):
        t = template.Template(text)
        c = template.Context(context)
        return t.render(c)


class FilterCallMethodTest(TagTestCase):
    def setUp(self):
        class obj():
            def func(self, param):
                return "%s" % param.__class__.__name__
        self.obj = obj

    def test_call_method_with_arg(self):
        self.assertEqual('int', self.render_template(
            """{% load cms_tags %}"""
            """{{ obj|call_method:"func:2" }}""",
            {'obj': self.obj},
        ))

    def test_call_method_with_kwarg(self):
        self.assertEqual('int', self.render_template(
            """{% load cms_tags %}"""
            """{{ obj|call_method:"func:param=2" }}""",
            {'obj': self.obj},
        ))

    def test_int_param(self):
        self.assertEqual('int', self.render_template(
            """{% load cms_tags %}"""
            """{{ obj|call_method:"func:param=2" }}""",
            {'obj': self.obj},
        ))

    def test_bool_param(self):
        self.assertEqual('bool', self.render_template(
            """{% load cms_tags %}"""
            """{{ obj|call_method:"func:param=True" }}""",
            {'obj': self.obj},
        ))

    def test_str_unicode_param(self):
        # Test string with single quotes
        self.assertEqual('unicode', self.render_template(
            """{% load cms_tags %}"""
            """{{ obj|call_method:"func:param='string'" }}""",
            {'obj': self.obj},
        ))
        # Test string with double quotes
        self.assertEqual('unicode', self.render_template(
            """{% load cms_tags %}"""
            """{{ obj|call_method:'func:param="string"' }}""",
            {'obj': self.obj},
        ))
        # Without any quotes
        self.assertEqual('unicode', self.render_template(
            """{% load cms_tags %}"""
            """{{ obj|call_method:"func:param=string" }}""",
            {'obj': self.obj},
        ))

