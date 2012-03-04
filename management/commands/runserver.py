from django.core.management.base import BaseCommand
from google.appengine.tools import dev_appserver_main

from ... import PROJECT_DIR

class Command(BaseCommand):

    def run_from_argv(self, argv):
        dev_appserver_main.PrintUsageExit = lambda x: ""
        dev_appserver_main.main(['runserver', PROJECT_DIR] + argv[2:] + ['--port=8000'])
