# -*- coding: utf-8 -*-
from whoosh.analysis import default_pattern
from whoosh.analysis import LowercaseFilter, RegexTokenizer
from whoosh.analysis import PyStemmerFilter, StopFilter
from whoosh.compat import text_type


STOP_WORDS = frozenset(
    (u'а', u'без', u'более', u'бы', u'был', u'была', u'были',
     u'было', u'быть', u'в', u'вам', u'вас', u'весь', u'во', u'вот',
     u'все', u'всего', u'всех', u'вы', u'где', u'да', u'даже', u'для',
     u'до', u'его', u'ее', u'если', u'есть', u'еще', u'же', u'за', u'здесь',
     u'и', u'из', u'или', u'им', u'их', u'к', u'как', u'ко', u'когда',
     u'кто', u'ли', u'либо', u'мне', u'может', u'мы', u'на', u'надо', u'наш',
     u'не', u'него', u'нее', u'нет', u'ни', u'них', u'но', u'ну', u'о', u'об',
     u'однако', u'он', u'она', u'они', u'оно', u'от', u'очень', u'по', u'под',
     u'при', u'с', u'со', u'так', u'также', u'такой', u'там', u'те', u'тем',
     u'то', u'того', u'тоже', u'той', u'только', u'том', u'ты', u'у', u'уже',
     u'хотя', u'чего', u'чей', u'чем', u'что', u'чтобы', u'чье', u'чья', u'эта',
     u'эти', u'это', u'я')
)

def StemmingAnalyzer(expression=default_pattern, stoplist=STOP_WORDS,
                     minsize=2, maxsize=None, gaps=False, lang='russian',
                     ignore=None, cachesize=50000):
    """Composes a RegexTokenizer with a lower case filter, an optional stop
    filter, and a stemming filter.
=
    >>> ana = StemmingAnalyzer()
    >>> [token.text for token in ana("Testing is testing and testing")]
    ["test", "test", "test"]

    :param expression: The regular expression pattern to use to extract tokens.
    :param stoplist: A list of stop words. Set this to None to disable
        the stop word filter.
    :param minsize: Words smaller than this are removed from the stream.
    :param maxsize: Words longer that this are removed from the stream.
    :param gaps: If True, the tokenizer *splits* on the expression, rather
        than matching on the expression.
    :param ignore: a set of words to not stem.
    :param cachesize: the maximum number of stemmed words to cache. The larger
        this number, the faster stemming will be but the more memory it will
        use.
    """

    ret = RegexTokenizer(expression=expression, gaps=gaps)
    chain = ret | LowercaseFilter()
    if stoplist is not None:
        chain = chain | StopFilter(stoplist=stoplist, minsize=minsize,
            maxsize=maxsize)
    return chain | PyStemmerFilter(lang=lang, ignore=ignore,
        cachesize=cachesize)
StemmingAnalyzer.__inittypes__ = dict(expression=text_type, gaps=bool,
    stoplist=list, minsize=int, maxsize=int)
