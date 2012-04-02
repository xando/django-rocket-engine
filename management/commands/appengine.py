import os

from ... import PROJECT_DIR, PROJECT_DIR_NAME

from google.appengine.tools import appcfg

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.urlresolvers import get_callable


PRE_UPDATE_HOOK = getattr(settings, 'APPENGINE_PRE_UPDATE',
                          'appengine_hooks.pre_update')

POST_UPDATE_HOOK = getattr(settings, 'APPENGINE_POST_UPDATE',
                           'appengine_hooks.post_update')

class Command(BaseCommand):
    """Wrapper for appcfg.py with pre-update and post-update hooks"""

    help = 'Calls appcfg.py for the current project.'
    args = '[any options that normally would be applied to appcfg.py]'

    def run_from_argv(self, argv):
        if len(argv) > 2 and argv[2] == 'update':
            file_path = os.path.join(PROJECT_DIR,"_gae_module_name.py")
            hook_module = open(file_path, "w+")
            hook_module.write("PROJECT_DIR_NAME='%s'\n" % PROJECT_DIR_NAME)
            hook_module.close()

            try:
                get_callable(PRE_UPDATE_HOOK)()
            except (AttributeError, ImportError):
                pass

            appcfg.main(argv[1:] + [PROJECT_DIR])

            try:
                get_callable(POST_UPDATE_HOOK)()
            except (AttributeError, ImportError):
                pass

            os.remove(file_path)
        else:
            appcfg.main(argv[1:] + [PROJECT_DIR])
