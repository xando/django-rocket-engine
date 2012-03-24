# Initialize Django
from django_appengine import wsgi, path_appendine_sdk

import os
import sys

# Add parent folder to sys.path, so we can import boot.
# App Engine causes main.py to be reloaded if an exception gets raised
# on the first request of a main.py instance, so don't add project_dir multiple
# times.
project_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if project_dir not in sys.path or sys.path.index(project_dir) > 0:
    while project_dir in sys.path:
        sys.path.remove(project_dir)
    sys.path.insert(0, project_dir)

for path in sys.path[:]:
    if path != project_dir and os.path.isdir(os.path.join(path, 'django')):
        sys.path.remove(path)
        break

# Remove the standard version of Django.
if 'django' in sys.modules and sys.modules['django'].VERSION < (1, 2):
    for k in [k for k in sys.modules
              if k.startswith('django.') or k == 'django']:
        del sys.modules[k]


# from django.utils.importlib import import_module

# # load all models.py to ensure signal handling installation or index loading
# # of some apps
# for app in settings.INSTALLED_APPS:
#     try:
#         import_module('%s.models' % (app))
#     except ImportError:
#         pass
path_appendine_sdk()

from django.conf import settings
from google.appengine.ext.deferred.handler import main
from google.appengine.ext.deferred.deferred import application

if __name__ == '__main__':
    main()
