import os
from django.conf import settings, UserSettingsHolder


settings = UserSettingsHolder(settings)


def get(key, default):
    return getattr(settings, 'CMS_%s' % key, default)


# Settings limits for Pages attachments
settings.ATTACHMENT_TYPES = get('ATTACHMENT_TYPES',
    ('doc', 'docx', 'xls', 'xslx', 'pdf', 'rtf', 'zip',))
settings.ATTACHMENT_SIZE = get('ATTACHMENT_SIZE', 1024 * 1024 * 10)  # In bites

# Type of detecting regions
settings.REGION_FINDER = get('REGION_FINDER', 'cms.regions.finder.URLFinder')

# URL Builders for the link tag
settings.URL_BUILDERS = get('URL_BUILDERS',
    ('cms.url_builders.RegionURLBuilder',))

settings.LOGIN_URL = get('LOGIN_URL', '/manage/login/')
settings.LOGIN_REDIRECT_URL = get('LOGIN_REDIRECT_URL', 'cms:home')

settings.ELEMENTS_ON_PAGE = get('ELEMENTS_ON_PAGE', 20)

# Person thumbnail size
settings.PERSON_THUMB_SIZE = get('PERSON_THUMB_SIZE', 55)

# Location for page search index
settings.PAGE_SEARCH_INDEX = get('PAGE_SEARCH_INDEX',
    os.path.join(settings.WEB_ROOT, 'search_index', 'pages'))

# Default Region
settings.DEFAULT_REGION = get('DEFAULT_REGION', 'ru')

settings.METRIKA_API_URL = get('METRIKA_API_URL',
    'http://api-metrika.yandex.ru/')

# The Letters
settings.LETTERS_ATTACH_MAX_SIZE = get('LETTERS_ATTACH_MAX_SIZE', 1024 * 1024 * 2)
settings.LETTERS_ATTACH_CONTENT_TYPES = get('LETTERS_ATTACH_CONTENT_TYPES', (
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',

))
