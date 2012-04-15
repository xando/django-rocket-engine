Settings
========


DATABASES
---------

django_rocket comes  with pre-defined backend Google  CloudSQL wrapper
which prevents of using your production database during development:

.. code-block:: python

    DATABASES = {
        'default': {
            'ENGINE': 'django_rocket.db.backends.cloudsql',
            'INSTANCE': 'instance:name',
            'NAME': 'database_name',
        }
    }

To distinguish  between production  and development,  library provides
helper method which could applied in settings.py:

.. code-block:: python

    # settings.py
    from django_rocket import on_appengine

    ...

    if on_appengine:
        DATABASES = {
            'default': {
                'ENGINE': 'django_rocket.db.backends.cloudsql',
                'INSTANCE': 'instance:name',
                'NAME': 'database_name',
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'development.db'
            }
        }


DEFAULT_FILE_STORAGE
--------------------

`Google   Cloud  Storage   <https://developers.google.com/storage/>`_
file backend. To  enable   storage  go   to  `Google   Api  Console
<https://code.google.com/apis/console>`_::

    DEFAULT_FILE_STORAGE = 'django_rocket.storage.CloudStorage'

APPENGINE_BUCKET
----------------

`Google   Cloud  Storage   <https://developers.google.com/storage/>`_
bucket  name.    To  enable   storage  go   to  `Google   Api  Console
<https://code.google.com/apis/console>`_.  Settings dedicated  to work
with 'django_rocket.storage.CloudStorage' as a DEFAULT_FILE_STORAGE.

Default::

    APPENGINE_BUCKET = None

Example::

    DEFAULT_FILE_STORAGE = 'django_rocket.storage.CloudStorage'
    APPENGINE_BUCKET = 'my-bucket'


APPENGINE_PRE_UPDATE
--------------------

Callable that will be applied before sending application to Google AppEngine.

Default::

    APPENGINE_PRE_UPDATE = 'appengine_hooks.pre_update'

APPENGINE_POST_UPDATE
---------------------

Callable that will be applied after sending application to Google AppEngine.

Default::

    APPENGINE_POST_UPDATE = 'appengine_hooks.post_update'

Example of appengine_hooks.py file::

    from django.core.management import call_command

    def pre_update():
        call_command('collectstatic')

    def post_update():
        call_command('on_appengine', 'syncdb')

        # If south is being used
       	call_command('on_appengine', 'migrate')

