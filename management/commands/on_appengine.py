from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Runs a command with access to the remote App Engine production ' \
           'server (e.g. manage.py on_appengine shell)'
    args = 'remotecommand'

    def handle(self, *args, **options):
        from ... import force_remote;
        force_remote = True
        call_command(*args)
