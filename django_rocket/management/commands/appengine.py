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
        virtualenv_appengine_src = os.path.join(virtualenv, 'src')

        appengine_libs = os.path.join(PROJECT_DIR, 'appengine_libs')
        appengine_requirements = os.path.join(virtualenv, 'requirements.txt')
        appengine_requirements_editable = os.path.join(virtualenv, 'requirements_editable.txt')

        pip_command = os.path.join(virtualenv, 'bin', 'pip')

        if not os.path.exists(virtualenv):
            subprocess.Popen(
                shlex.split('virtualenv %s' % virtualenv),
            ).wait()

        with open(requirements_file) as f:
            editable = lambda x: re.match('^\s*\-e(ditable)?.+$', x) != None

            file_content = f.readlines()

            appengine_requirements_content="".join(
                [line for line in file_content if not editable(line)]
            )
            if appengine_requirements_content:
                open(appengine_requirements, 'w').write(
                    appengine_requirements_content
                )


            appengine_requirements_editable_content = "".join(
                [line for line in file_content if editable(line)]
            )
            if appengine_requirements_editable_content:
                open(appengine_requirements_editable, 'w').write(
                    appengine_requirements_editable_content
                )

        if not os.path.exists(appengine_libs):
            os.mkdir(appengine_libs)

        if os.path.exists(appengine_requirements):
            subprocess.Popen(
                shlex.split(
                    "%s install --requirement=%s --download-cache=%s --target=%s"
                    % (pip_command, appengine_requirements,
                       virtualenv_cache, virtualenv_appengine_libs)
                ),
            ).wait()

            for package in os.listdir(virtualenv_appengine_libs):
                shutil.move(
                    os.path.join(virtualenv_appengine_libs, package),
                    os.path.join(appengine_libs, package)
                )

            os.remove(appengine_requirements)

        if os.path.exists(appengine_requirements_editable):
            subprocess.Popen(
                shlex.split(
                    "%s install --requirement=%s --download-cache=%s"
                    % (pip_command, appengine_requirements_editable,
                       virtualenv_cache)
                ),
            ).wait()

            for package in os.listdir(virtualenv_appengine_src):
                shutil.move(
                    os.path.join(virtualenv_appengine_src, package),
                    os.path.join(appengine_libs, package)
                )

            os.remove(appengine_requirements_editable)

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

        try:
            self.prepare_upload()

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
