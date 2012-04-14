import os
import re
import shutil
import shlex
import logging
import subprocess

from google.appengine.tools import appcfg
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.urlresolvers import get_callable

from ... import PROJECT_DIR, PROJECT_DIR_NAME


logger = logging.getLogger(__name__)


PRE_UPDATE_HOOK = getattr(
    settings, 'APPENGINE_PRE_UPDATE', 'appengine_hooks.pre_update'
)
POST_UPDATE_HOOK = getattr(
    settings, 'APPENGINE_POST_UPDATE', 'appengine_hooks.post_update'
)
APPENGINE_VIRTUALENV = getattr(
    settings, 'APPENGINE_VIRTUALENV', '.appengine'
)
APPENGINE_REQUIREMENTS_FILE = getattr(
    settings, 'APPENGINE_REQUIREMENTS_FILE', 'requirements.txt'
)

class Command(BaseCommand):
    """Wrapper for appcfg.py with pre-update and post-update hooks"""

    help = 'Calls appcfg.py for the current project.'
    args = '[any options that normally would be applied to appcfg.py]'

    def install_requirements(self, requirements_file):
        virtualenv = os.path.join(PROJECT_DIR, APPENGINE_VIRTUALENV)
        virtualenv_cache = os.path.join(virtualenv, 'cache')
        virtualenv_appengine_libs = os.path.join(virtualenv, 'appengine_libs')

        pip_command = os.path.join(virtualenv, 'bin', 'pip')

        if not os.path.exists(virtualenv):
            subprocess.Popen(
                shlex.split('virtualenv %s --distribute' % virtualenv),
            ).wait()

        subprocess.Popen(
            shlex.split(
                "%s install --requirement=%s --download-cache=%s --target=%s"
                % (pip_command, requirements_file,
                   virtualenv_cache, virtualenv_appengine_libs)
            ),
        ).wait()

        shutil.move(
            virtualenv_appengine_libs,
            PROJECT_DIR
        )

    def prepare_upload(self):
        requirements_file = os.path.join(
            PROJECT_DIR, APPENGINE_REQUIREMENTS_FILE
        )

        if os.path.exists(requirements_file):
            self.install_requirements(requirements_file)


    def clean_upload(self):
        virtualenv = os.path.join(PROJECT_DIR, APPENGINE_VIRTUALENV)
        virtualenv_appengine_libs = os.path.join(virtualenv, 'appengine_libs')
        appengine_libs = os.path.join(PROJECT_DIR, 'appengine_libs')
        try:
            shutil.rmtree(virtualenv_appengine_libs)
        except OSError:
            pass
        try:
            shutil.rmtree(appengine_libs)
        except OSError:
            pass

    def update(self, argv):
        self.clean_upload()
        self.prepare_upload()
        return
        try:
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

        finally:
            os.remove(file_path)
            self.clean_upload()

    def run_from_argv(self, argv):
        if len(argv) > 2 and argv[2] == 'update':
            self.update(argv)
        else:
            appcfg.main(argv[1:] + [PROJECT_DIR])
