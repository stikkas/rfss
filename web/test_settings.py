from settings import *

# Instead migration will be used syncdb
if 'south' in INSTALLED_APPS:
    SOUTH_TESTS_MIGRATE = False

# Create databases in memory for speed up tests
for db in DATABASES:
    DATABASES[db] = {'ENGINE': 'django.db.backends.sqlite3'}

# Turn off search indexing signal
try:
    apps = list(INSTALLED_APPS)
    apps.remove('cms.search')
    INSTALLED_APPS = tuple(apps)
except ValueError:
    pass
