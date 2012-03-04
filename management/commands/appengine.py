import os

from ... import PROJECT_DIR, PROJECT_DIR_NAME

from google.appengine.tools import appcfg

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

PRE_UPDATE_COMMANDS = getattr(settings, 'PRE_UPDATE_COMMANDS', ())
POST_UPDATE_COMMANDS = getattr(settings, 'POST_UPDATE_COMMANDS', ())

class Command(BaseCommand):
    """Wrapper for appcfg.py with pre-update and post-update hooks"""

    help = 'Calls appcfg.py for the current project.'
    args = '[any options that normally would be applied to appcfg.py]'

    def call_command(self, command):
        if isinstance(command, basestring):
            call_command(command)
        if isinstance(command, tuple) or isinstance(command, list):
            call_command(*command)

    def run_from_argv(self, argv):
        if len(argv) > 2 and argv[2] == 'update':
            file_path = os.path.join(PROJECT_DIR,"_gae_module_name.py")
            hook_module = open(file_path, "w+")
            hook_module.write("PROJECT_DIR_NAME='%s'\n" % PROJECT_DIR_NAME)
            hook_module.close()

            for command in PRE_UPDATE_COMMANDS:
                self.call_command(command)

            appcfg.main(argv[1:] + [PROJECT_DIR])

            for command in POST_UPDATE_COMMANDS:
                self.call_command(command)

            os.remove(file_path)
        else:
            appcfg.main(argv[1:] + [PROJECT_DIR])
