import os

from django.conf import settings, Settings
from django.utils import importlib

from django.core.management.base import BaseCommand
from django.core.management import execute_from_command_line

import django_rocket

class Command(BaseCommand):
    help = 'Runs a command with access to the remote App Engine production ' \
           'server (e.g. manage.py on_appengine shell)'
    args = 'remotecommand'

    def reload_settings(self):
        django_rocket.on_appengine = True
        settings_module = os.environ["DJANGO_SETTINGS_MODULE"]

        mod = importlib.import_module(settings_module)
        reload(mod)
        settings._wrapped = Settings(settings_module)

    def run_from_argv(self, argv):
        self.reload_settings()

        execute_from_command_line(argv[:1] + argv[2:])
